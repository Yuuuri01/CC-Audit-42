#!/usr/bin/env python3

import os
import sys
import subprocess
from colors import colors

"""part norminette C_files and header_files"""
def run_norm_CF(file_path) ->int:
    try:
        cmd: list = ["norminette", file_path]
        out: subprocess.CompletedProcess[str] = subprocess.run(cmd, capture_output=True, text=True)
        if out.returncode == 0:
            print(f"    {colors.GREEN}{colors.BOLD}.{out.stdout}{colors.RESET}")
            return 1
        else:
            print(f"    {colors.RED}{colors.BOLD}.{out.stdout}{colors.RESET}")
            return 0

    except:
        print(f"error: command not found: 'norminette'")
        print("see manual below")

def run_norm_HF(file_path) ->None:

    try:
        cmd: list = ["norminette", "-R", "CheckForbiddenSourceHeader", file_path]
        run_norm: subprocess.CompletedProcess[str] = subprocess.run(cmd, capture_output=True, text=True)

        if run_norm.returncode == 0:
            print(f"{colors.GREEN}|{colors.RESET}")
            print(F"{run_norm.stdout}")
        else:
            print(f"{colors.RED}---->{colors.RESET}{run_norm.stdout}")
    except:
        print(f"error: command not found: 'norminette'")
        print("see manual below")
"""END"""