#!/usr/bin/env python3
# Copyright akettunen 2026

import os
import sys
import platform
import shutil

CYAN = "\033[38;2;38;97;156m"
RESET = "\033[0m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"

LOGO = (
    r"   /\ /\ ",
    r"  /  \  \ ",
    r" /    \  \ ",
    r"/      \  \ ",
)


def get_os():
    if sys.platform != "linux":
        return platform.system()

    try:
        os_id = ""
        pretty_name = "Alpine Linux"

        with open("/etc/os-release", encoding="utf-8") as f:
            for line in f:
                if line.startswith("ID="):
                    os_id = line.split("=", 1)[1].strip().strip('"').lower()
                elif line.startswith("PRETTY_NAME="):
                    pretty_name = line.split("=", 1)[1].strip().strip('"')

        if os_id != "alpine":
            return "Your OS is not Alpine Linux!"

        return pretty_name

    except OSError:
        return "Unknown"


def get_memory():
    if sys.platform == "win32":
        try:
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("length", ctypes.c_ulong),
                    ("memory_load", ctypes.c_ulong),
                    ("total_phys", ctypes.c_ulonglong),
                    ("avail_phys", ctypes.c_ulonglong),
                    ("total_page", ctypes.c_ulonglong),
                    ("avail_page", ctypes.c_ulonglong),
                    ("total_virtual", ctypes.c_ulonglong),
                    ("avail_virtual", ctypes.c_ulonglong),
                    ("avail_extended", ctypes.c_ulonglong),
                ]

            status = MemoryStatus()
            status.length = ctypes.sizeof(status)

            if ctypes.windll.kernel32.GlobalMemoryStatusEx(
                ctypes.byref(status)
            ):
                return f"{status.total_phys / 1073741824:.2f} GB"

        except (AttributeError, OSError):
            pass

        return "Unknown"

    try:
        with open("/proc/meminfo", encoding="ascii") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    return f"{kb / 1048576:.2f} GB"

    except (OSError, ValueError, IndexError):
        pass

    return "Unknown"


def get_disk():
    try:
        path = (
            os.environ.get("SystemDrive", "C:") + "\\"
            if os.name == "nt"
            else "/"
        )
        total = shutil.disk_usage(path).total
        return f"{total / 1073741824:.2f} GB"

    except OSError:
        return "Unknown"


def main():
    if "--issue" in sys.argv:
        print(f"{YELLOW}If you have an issue with minalpine, contact me:{RESET}")
        print(f"{MAGENTA}Discord: @ak0101101{RESET}")
        print(f"{WHITE}GitHub: https://github.com/akx25/minalpine/issues{RESET}")
        return

    info = (
        ("host", platform.node() or "unknown"),
        ("os", get_os()),
        ("memory", get_memory()),
        ("disk", get_disk()),
    )

    for i, (label, value) in enumerate(info):
        left = LOGO[i] if i < len(LOGO) else ""
        print(f"{CYAN}{left:<12}{RESET}  {CYAN}{label}:{RESET} {value}")


if __name__ == "__main__":
    main()
