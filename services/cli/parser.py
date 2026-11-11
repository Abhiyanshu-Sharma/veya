import ctypes

def parse_command(command):

        shell32 = ctypes.WinDLL("shell32", use_last_error=True)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        command_line_to_argv = shell32.CommandLineToArgvW
        command_line_to_argv.argtypes = [
            ctypes.c_wchar_p,
            ctypes.POINTER(ctypes.c_int)
        ]
        command_line_to_argv.restype = ctypes.POINTER(ctypes.c_wchar_p)

        local_free = kernel32.LocalFree
        local_free.argtypes = [ctypes.c_void_p]
        local_free.restype = ctypes.c_void_p

        argc = ctypes.c_int()

        argv = command_line_to_argv(
            command,
            ctypes.byref(argc)
        )

        if not argv:
            raise ctypes.WinError(ctypes.get_last_error())

        try:
            return [
                argv[index]
                for index in range(argc.value)
            ]

        finally:
            local_free(ctypes.cast(argv, ctypes.c_void_p))