#!/usr/bin/env python3
import os
import sys
import glob
import shutil
import subprocess

import fsyn
import testers
from colors import colors

HELP_HINT = "try: ./audit.py --help or -h to see manual"
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def print_error(msg: str) -> None:
    print(f"{colors.RED}{colors.BOLD}{msg}{colors.RESET}\n")


def check_syntax(path: str) -> None:
    if os.path.isfile(path):
        files = [path]
    else:
        files = glob.glob(os.path.join(path, "**", "*.c"), recursive=True)

    if not files:
        print(f"{colors.YELLOW}no .c files found{colors.RESET}")
        return

    if shutil.which("cc") is None:
        print_error("error: 'cc' compiler not found")
        return

    cmd = ["cc", "-Wall", "-Wextra", "-Werror", "-fsyntax-only", *files]
    out = subprocess.run(cmd, capture_output=True, text=True)

    if out.returncode == 0:
        print(f"{colors.GREEN}<EVERYTHING IS OKEY!>{colors.RESET}")
    else:
        print(out.stderr)


def norm_file(path: str) -> tuple:
    """Run norminette on one .c/.h file. Returns (files_checked, errors)."""
    if path.endswith(".c"):
        return 1, 1 if fsyn.run_norm_CF(path) == 0 else 0
    if path.endswith(".h"):
        return 1, 1 if fsyn.run_norm_HF(path) == 0 else 0
    return 0, 0


def norm_dir(dir_path: str) -> tuple:
    """Norminette on a folder and its direct sub-folders. Returns (files, errors)."""
    files_count = 0
    errors = 0

    print(f"{colors.GREEN}{colors.BOLD}MAIN_DIR: {dir_path}{colors.RESET}\n")
    with os.scandir(dir_path) as entries:
        for entry in sorted(entries, key=lambda e: e.name):
            if entry.is_file():
                f, e = norm_file(entry.path)
                files_count += f
                errors += e
            elif entry.is_dir():
                print(f"{colors.YELLOW}|----|>{colors.RESET} "
                      f"{colors.BLUE}{colors.BOLD}{entry.name}{colors.RESET}")
                with os.scandir(entry.path) as sub_entries:
                    for sub in sorted(sub_entries, key=lambda e: e.name):
                        if sub.is_file():
                            f, e = norm_file(sub.path)
                            files_count += f
                            errors += e
    return files_count, errors


def print_summary(files_count: int, errors: int) -> None:
    print(f"{colors.YELLOW}{colors.BOLD}{files_count} files checked, {errors} Errors!{colors.RESET}")


def show_help() -> None:
    usage_path = os.path.join(BASE_DIR, "usage.txt")
    try:
        with open(usage_path, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print_error(f"usage.txt not found in {BASE_DIR}")


def main() -> int:
    argv = sys.argv

    if len(argv) <= 1:
        print_error(HELP_HINT)
        return 1

    option = argv[1]

    # ---- help
    if len(argv) == 2 and option in ("--help", "-h"):
        show_help()
        return 0

    # ---- single file
    if len(argv) == 3 and option in ("-f", "--file"):
        file_path = argv[2]
        files_count, errors = 0, 0
        if os.path.isfile(file_path) and file_path.endswith((".c", ".h")):
            print(f"\n{colors.BLUE}{colors.BOLD}-----|>{file_path}{colors.RESET}")
            files_count, errors = norm_file(file_path)
        else:
            print_error(f"{file_path} is not C file or Header file!")
            return 1
        print_summary(files_count, errors)
        return 1 if errors else 0

    # ---- norminette on a directory
    if len(argv) == 3 and option in ("-d", "--dir"):
        dir_path = argv[2]
        if not os.path.isdir(dir_path):
            print_error(f"['{dir_path}' not found!] {HELP_HINT}")
            return 1
        files_count, errors = norm_dir(dir_path)
        print_summary(files_count, errors)
        return 1 if errors else 0

    # ---- syntax check
    if len(argv) == 3 and option in ("-s", "--syntax"):
        path = argv[2]
        if os.path.isdir(path) or os.path.isfile(path):
            check_syntax(path)
            return 0
        print_error(f"['{path}' not found!] {HELP_HINT}")
        return 1

    # ---- syntax + norminette
    if len(argv) == 3 and option in ("-l", "--check-all"):
        path = argv[2]
        if not os.path.isdir(path):
            print_error(f"['{path}' not found!] {HELP_HINT}")
            return 1
        print(f"{colors.GRAY}{colors.BOLD}--|>.CHECK SYNTAX...{colors.RESET}\n")
        check_syntax(path)

        print(f"\n{colors.GRAY}{colors.BOLD}--|>.CHECK NORMINETTE...{colors.RESET}")
        files_count, errors = norm_dir(path)
        print_summary(files_count, errors)
        return 1 if errors else 0

    if len(argv) >= 3 and option in ("--libft", "--printf", "--gnl"):
        name = option[2:]
        path = argv[2]
        tests = argv[3:]
        if tests and tests[0] == "--only":
            tests = tests[1:]
        return testers.run_tester(name, path, tests)

    print_error(HELP_HINT)
    return 1


if __name__ == "__main__":
    sys.exit(main())