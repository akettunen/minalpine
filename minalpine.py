# Copyright akettunen 2026
import sys
import platform
import argparse
import os
import shutil


def is_alpine():
    """Check whether the current OS is Alpine Linux."""
    try:
        with open("/etc/os-release", "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("ID="):
                    os_id = line.split("=", 1)[1].strip().strip('"').lower()
                    return os_id == "alpine"
    except OSError:
        pass

    return False


def color(text, code):
    """Print colored text using ANSI escape codes."""
    return f"\033[{code}m{text}\033[0m"


parser = argparse.ArgumentParser(
    description=color(
        "minalpine - a system information tool for Alpine Linux.",
        "36",
    )
)

parser.add_argument(
    "--issue",
    action="store_true",
    help="Contact @ak0101101 on Discord or visit "
         "https://github.com/akx25/minalpine/issues",
)

args = parser.parse_args()

if args.issue:
    print(color("If you have an issue with minalpine, contact me:", "33"))
    print(color("Discord: @ak0101101", "35"))
    print(color("GitHub: https://github.com/akx25/minalpine/issues", "37"))
    sys.exit(0)


def get_host():
    return platform.node() or "unknown"


def get_os():
    if not is_alpine():
        return color("Your OS is not Alpine Linux!", "33")

    try:
        with open("/etc/os-release", "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=", 1)[1].strip().strip('"')
    except OSError:
        pass

    return "Alpine Linux"


def get_memory():
    """Get total RAM from /proc/meminfo."""
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    return f"{kb / (1024 ** 2):.2f} GB"
    except (OSError, ValueError, IndexError):
        pass

    return "Unknown"


def get_disk():
    """Get total disk space on the root filesystem."""
    try:
        total, _, _ = shutil.disk_usage("/")
        return f"{total / (1024 ** 3):.2f} GB"
    except OSError:
        return "Unknown"



# Logo
logo = [
    r"   /\ /\ ",
    r"  /  \  \ ",
    r" /    \  \ ",
    r"/      \  \ ",
]

info = [
    f"host:   {get_host()}",
    f"os:     {get_os()}",
    f"memory: {get_memory()}",
    f"disk:   {get_disk()}",
]


CYAN = "\033[38;2;38;97;156m"
RESET = "\033[0m"

for i in range(max(len(logo), len(info))):
    left = logo[i] if i < len(logo) else ""

    if i < len(info):
        label, value = info[i].split(":", 1)
        right = f"{CYAN}{label}:{RESET}{value}"
    else:
        right = ""

    print(f"{CYAN}{left:<12}{RESET}  {right}")
