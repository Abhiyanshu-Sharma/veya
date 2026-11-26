import base64
from datetime import datetime, timezone
import re
import requests
from services.token_store import get_token  # adjust if token_store is in another subfolder


class RepoSummaryService:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self._cache = {}

    def _headers(self):
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "Veya-Desktop-App",
        }
        token = get_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def inspect_repository(self, repo, force_refresh=False):
        full_name = repo.get("full_name")
        if not full_name:
            owner = repo.get("owner", {}).get("login", "")
            name = repo.get("name", "")
            full_name = f"{owner}/{name}".strip("/")

        if not force_refresh and full_name in self._cache:
            return self._cache[full_name]

        default_branch = repo.get("default_branch") or "main"
        headers = self._headers()

        # 1. Fetch recursive file tree
        tree_items = []
        tree_url = f"{self.BASE_URL}/repos/{full_name}/git/trees/{default_branch}?recursive=1"
        try:
            tree_resp = requests.get(tree_url, headers=headers, timeout=10)
            if tree_resp.status_code == 200:
                tree_items = tree_resp.json().get("tree", [])
        except requests.RequestException:
            pass

        # 2. Fetch README
        readme_text = ""
        readme_url = f"{self.BASE_URL}/repos/{full_name}/readme"
        try:
            readme_resp = requests.get(readme_url, headers=headers, timeout=10)
            if readme_resp.status_code == 200:
                encoded = readme_resp.json().get("content", "")
                if encoded:
                    readme_text = base64.b64decode(encoded).decode("utf-8", errors="ignore")
        except requests.RequestException:
            pass

        # 3. Fetch primary manifest if present (helps detect project kind accurately)
        manifest_names = (
            "requirements.txt",
            "pyproject.toml",
            "package.json",
            "Cargo.toml",
            "pubspec.yaml",
            "pom.xml",
        )
        paths = [item.get("path", "") for item in tree_items if item.get("type") == "blob"]
        manifest_content = ""
        found_manifest = ""
        for candidate in manifest_names:
            if candidate in paths:
                found_manifest = candidate
                content_url = f"{self.BASE_URL}/repos/{full_name}/contents/{candidate}"
                try:
                    c_resp = requests.get(content_url, headers=headers, timeout=10)
                    if c_resp.status_code == 200:
                        encoded = c_resp.json().get("content", "")
                        if encoded:
                            manifest_content = base64.b64decode(encoded).decode("utf-8", errors="ignore")
                except requests.RequestException:
                    pass
                break

        inspection = {
            "repo": repo,
            "full_name": full_name,
            "tree_items": tree_items,
            "paths": paths,
            "readme_text": readme_text,
            "manifest_name": found_manifest,
            "manifest_content": manifest_content,
        }
        self._cache[full_name] = inspection
        return inspection

    def generate_simple_summary(self, repo):
        data = self.inspect_repository(repo)
        name = repo.get("name", "This repository")
        language = repo.get("language") or ""
        description = (repo.get("description") or "").strip()
        is_private = repo.get("private", False)
        paths = data["paths"]
        readme_text = data["readme_text"]
        manifest_content = data["manifest_content"].lower()

        project_kind = self._classify_project_kind(language, paths, manifest_content, readme_text)
        clean_overview, feature_sentences = self._parse_readme_human(readme_text)

        # --- Paragraph 1: Natural Identity & Purpose ---
        visibility_word = "private " if is_private else ""
        intro = f"{name} is a {visibility_word}{project_kind}"

        purpose = self._pick_best_purpose(description, clean_overview, name)
        if purpose:
            p1 = f"{intro} {purpose}"
        else:
            top_dirs = self._get_top_folders(paths)
            if top_dirs:
                folder_phrase = self._join_natural(top_dirs[:3])
                p1 = f"{intro} organized around core components like {folder_phrase}."
            else:
                p1 = f"{intro} hosted on GitHub."

        # --- Paragraph 2: What It Actually Does (if features found) ---
        p2 = ""
        if feature_sentences:
            if len(feature_sentences) == 1:
                p2 = f"In practice, it {self._lowercase_first(feature_sentences[0])}"
            else:
                first_two = [self._lowercase_first(s).rstrip(".") for s in feature_sentences[:2]]
                p2 = f"In practice, it {first_two[0]}, and it also {first_two[1]}."
                if len(feature_sentences) >= 3:
                    third = self._lowercase_first(feature_sentences[2]).rstrip(".")
                    p2 += f" Beyond that, it {third}."

        # --- Paragraph 3: Scale, Structure & Activity Feel ---
        file_count = len(paths)
        scale_phrase = self._describe_scale(file_count)
        activity_phrase = self._describe_activity(repo.get("updated_at"))
        readiness_notes = []
        if readme_text.strip():
            readiness_notes.append("documentation")
        if data["manifest_name"]:
            readiness_notes.append("dependency tracking")
        if any("test" in p.lower() for p in paths):
            readiness_notes.append("automated tests")

        p3_parts = []
        if file_count > 0:
            p3_parts.append(f"Looking at the codebase, it's structured as {scale_phrase}")
        else:
            p3_parts.append("It's currently a fresh or lightweight repository")

        if readiness_notes:
            p3_parts.append(f"with {self._join_natural(readiness_notes)} in place")

        p3 = " ".join(p3_parts).rstrip(".") + "."
        if activity_phrase:
            p3 += f" {activity_phrase}"

        paragraphs = [p1]
        if p2:
            paragraphs.append(p2)
        paragraphs.append(p3)

        return {
            "title": name,
            "subtitle": f"{project_kind.capitalize()}  •  {'Private' if is_private else 'Public'} Repository",
            "body": "\n\n".join(paragraphs),
        }

    # --- Helper Methods ---

    def _classify_project_kind(self, language, paths, manifest, readme):
        lang_prefix = f"{language} " if language else ""
        lower_paths = " ".join(paths).lower()
        combined = f"{manifest} {readme.lower()}"

        if any(k in combined for k in ("pyside6", "pyqt", "tkinter", "customtkinter", "electron", "tauri")) or (
            "ui/" in lower_paths and "main.py" in lower_paths
        ):
            return f"{lang_prefix}desktop application".strip()
        if any(k in manifest for k in ("react", "vue", "next", "svelte", "angular", "vite")):
            return f"{lang_prefix}web application".strip()
        if any(k in manifest for k in ("fastapi", "flask", "django", "express", "nestjs", "spring")):
            return f"{lang_prefix}backend web service".strip()
        if any(k in lower_paths for k in ("pubspec.yaml", "android/", "ios/", "flutter")):
            return f"{lang_prefix}mobile application".strip()
        if any(k in manifest for k in ("opencv", "torch", "tensorflow", "scikit-learn", "pandas")):
            return f"{lang_prefix}data and computer vision project".strip()
        if any(k in combined for k in ("argparse", "typer", "click", "command-line tool", "cli tool")):
            return f"{lang_prefix}command-line tool".strip()
        if any(p.endswith(".html") for p in paths):
            return f"{lang_prefix}web project".strip()
        if language:
            return f"{language} project"
        return "software project"

    def _parse_readme_human(self, readme_text):
        if not readme_text.strip():
            return "", []

        # Remove fenced code blocks
        cleaned = re.sub(r"```[\s\S]*?```", "", readme_text)
        # Remove HTML tags
        cleaned = re.sub(r"<[^>]+>", " ", cleaned)
        # Remove markdown images ![alt](url)
        cleaned = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", cleaned)
        # Convert markdown links [text](url) -> text
        cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)

        lines = [line.strip() for line in cleaned.splitlines()]
        paragraphs = []
        bullets = []
        current_para = []
        in_install_section = False

        skip_headings = ("install", "setup", "getting started", "license", "contributing", "usage", "prerequisites")

        for line in lines:
            if not line:
                if current_para:
                    paragraphs.append(" ".join(current_para))
                    current_para = []
                continue

            if line.startswith("#"):
                if current_para:
                    paragraphs.append(" ".join(current_para))
                    current_para = []
                heading_text = line.lstrip("#").strip().lower()
                in_install_section = any(k in heading_text for k in skip_headings)
                continue

            if in_install_section:
                continue

            # Bullet points
            if re.match(r"^[-*•]\s+", line):
                bullet_text = re.sub(r"^[-*•]\s+", "", line)
                bullet_text = re.sub(r"[*_`]", "", bullet_text).strip()
                # Skip CLI commands or tiny fragments
                if len(bullet_text.split()) >= 4 and not bullet_text.startswith(("pip ", "npm ", "git ", "python ")):
                    if not bullet_text.endswith("."):
                        bullet_text += "."
                    bullets.append(bullet_text)
                continue

            # Regular prose line
            plain_line = re.sub(r"[*_`]", "", line).strip()
            if len(plain_line.split()) >= 5 and not plain_line.startswith(("http", "pip ", "npm ", "git ")):
                current_para.append(plain_line)

        if current_para:
            paragraphs.append(" ".join(current_para))

        overview = paragraphs[0] if paragraphs else ""
        return overview, bullets[:3]

    def _pick_best_purpose(self, description, readme_overview, repo_name):
        candidate = description or readme_overview
        if not candidate:
            return ""

        first_sentence = re.split(r"(?<=[.!?])\s+", candidate.strip())[0].strip()
        # Strip redundant trailing "built with Python" / "in Python"
        first_sentence = re.sub(r"\s+(built with|written in|using)\s+[A-Za-z0-9+#.]+\.?$", "", first_sentence, flags=re.IGNORECASE).strip()
        if not first_sentence.endswith("."):
            first_sentence += "."

        pattern = rf"^{re.escape(repo_name)}\s+(is\s+(a|an)\s+[^.,]+)"
        if re.match(pattern, first_sentence, flags=re.IGNORECASE):
            sentences = re.split(r"(?<=[.!?])\s+", readme_overview.strip())
            if len(sentences) > 1 and len(sentences[1].split()) >= 5:
                s2 = sentences[1].strip()
                return s2 if s2.endswith(".") else s2 + "."
            return ""

        lower = first_sentence[0].lower() + first_sentence[1:]
        if lower.startswith(("a ", "an ", "the ")):
            return f"designed as {lower}"
        if lower.startswith(("to ", "for ")):
            return f"built {lower}"
        if lower.startswith(("provides ", "helps ", "allows ", "enables ", "simplifies ", "manages ", "automates ")):
            return f"that {lower}"
        return f"focused on {lower}"

    def _describe_scale(self, file_count):
        if file_count <= 8:
            return f"a compact, lightweight codebase ({file_count} files)"
        if file_count <= 35:
            return f"a clean, focused project ({file_count} files)"
        if file_count <= 100:
            return f"a well-structured, medium-sized application ({file_count} files)"
        return f"a large, multi-module codebase ({file_count} files)"

    def _describe_activity(self, updated_at):
        if not updated_at:
            return ""
        try:
            updated_dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            days_ago = (datetime.now(timezone.utc) - updated_dt).days
            if days_ago <= 7:
                return "It's actively maintained, with updates pushed within the last week."
            if days_ago <= 30:
                return "It has seen recent updates over the past month."
            if days_ago <= 180:
                return f"It's a steady project, last updated around {max(1, days_ago // 30)} month(s) ago."
            return "It appears to be a completed or older project that hasn't been modified recently."
        except ValueError:
            return ""

    def _get_top_folders(self, paths):
        folders = []
        for p in paths:
            if "/" in p:
                top = p.split("/")[0]
                if not top.startswith(".") and top not in folders:
                    folders.append(top)
        return folders

    def _join_natural(self, items):
        if not items:
            return ""
        if len(items) == 1:
            return items[0]
        if len(items) == 2:
            return f"{items[0]} and {items[1]}"
        return f"{', '.join(items[:-1])}, and {items[-1]}"

    def _lowercase_first(self, text):
        if not text:
            return ""

        # Handle "Title Label: description..." bullets (e.g., "CLI Workspace: Integrated terminal...")
        if ":" in text:
            label, rest = text.split(":", 1)
            label = label.strip()
            rest = rest.strip()
            if rest and len(label.split()) <= 4:
                # Preserve acronyms like CLI, GUI, API
                clean_label = " ".join(w if w.isupper() else w.lower() for w in label.split())
                article = "an" if clean_label[0].lower() in "aeiou" else "a"
                return f"features {article} {clean_label} with {rest[0].lower() + rest[1:]}"

        words = text.split()
        first_word = words[0]
        first_lower = first_word.lower()
        verb_starters = {
            "manage", "switch", "customize", "create", "build", "track",
            "view", "inspect", "generate", "sync", "run", "support",
            "handle", "export", "import", "search", "filter", "monitor",
        }
        if first_lower in verb_starters:
            return f"lets you {first_lower} {' '.join(words[1:])}"
        if first_word.isupper():
            return text
        return text[0].lower() + text[1:]