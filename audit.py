#!/usr/bin/env python3

import fsyn
from fsyn import *
from colors import colors

def check_syntax(name_dir) ->None:
    try:
        if os.path.isfile(name_dir):
            cmd  = f"cc -Wall -Wextra -Werror -fsyntax-only {name_dir} */*"
            out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if out.returncode == 0:
                print(f"{colors.GREEN}<EVERYTHING IS OKEY!>{colors.RESET}")
            else:
                print(f"{out.stderr}")
        else:
            cmd = f"cc -Wall -Wextra -Werror -fsyntax-only {name_dir}/*/*"
            out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if out.returncode == 0:
                print(f"{colors.GREEN}<EVERYTHING IS OKEY!>{colors.RESET}")
            else:
                print(f"{out.stderr}")
    except:
        print("something wrong!")

def main() ->None:
    if len(sys.argv) <= 1:
        print(f"{colors.RED}{colors.BOLD}try: python3 main.py --help or -h to see manual{colors.RESET}\n")

    elif len(sys.argv) == 2 and sys.argv[1] in ("--help", "-h"):
        file = open("usage.txt", "r")
        data = file.read()
        print(data)
    elif len(sys.argv) == 3 and sys.argv[1] in ("-f", "--file"):
        file_path = sys.argv[2]
        if os.path.isfile(file_path):
            print(f"\n{colors.BLUE}{colors.BOLD}-----|>{file_path}{colors.RESET}")
            if file_path.endswith(".c"):
                fsyn.run_norm_CF(file_path)
            elif file_path.endswith(".h"):
                fsyn.run_norm_HF(file_path)
        else:
            print(f"{colors.RED}{colors.BOLD}{file_path} is not C file or Header file!{colors.RESET}")
    elif len(sys.argv) == 3 and sys.argv[1] in ("-d", "--dir"):
        dir_path = sys.argv[2]
        if os.path.isdir(dir_path):
            print(f"{colors.GREEN}{colors.BOLD}MAIN_DIR: {dir_path}{colors.RESET}\n")
            with os.scandir(dir_path) as names:
                for T in names:
                    if T.is_file() and T.name.endswith(".c"):
                        fsyn.run_norm_CF(T.path)
                    elif T.is_file() and T.name.endswith(".h"):
                        fsyn.run_norm_HF(T.path)
                    elif T.is_dir():
                        print(f"{colors.YELLOW}|----|>{colors.RESET} {colors.BLUE}{colors.BOLD}{T.name}{colors.RESET}")
                        with os.scandir(T) as ens:
                            for N in ens:
                                if N.is_file() and N.name.endswith(".c"):
                                    fsyn.run_norm_CF(N.path)
                                elif N.is_file() and N.name.endswith(".h"):
                                    fsyn.run_norm_HF(N.path)
                                else:
                                    pass
                    else:
                        pass
        else:
            print(f"{colors.RED}{colors.BOLD}['{sys.argv[2]}' not found!] try: python3 main.py --help or -h to see manual{colors.RESET}\n")

    elif len(sys.argv) == 3 and sys.argv[1] in ("--syntax", "-s"):
        dir_path = sys.argv[2]
        if os.path.isdir(dir_path):
            check_syntax(dir_path)
        elif os.path.isfile(dir_path):
            print(dir_path)
            check_syntax(dir_path)
        else:
            print(f"{colors.RED}{colors.BOLD}['{sys.argv[2]}' not found!] try: python3 main.py --help or -h to see manual{colors.RESET}\n")

    elif len(sys.argv) == 3 and sys.argv[1] in ("--check-all, -l"):
        path_name = sys.argv[2]
        if os.path.isdir(path_name):
            print(f"{colors.GRAY}{colors.BOLD}--|>.CHECK SYNTAX...{colors.RESET}\n")
            check_syntax(path_name)

            print(f"\n{colors.GRAY}{colors.BOLD}--|>.CHECK NORMINETTE...{colors.RESET}")
            with os.scandir(path_name) as dirs:
                print(f"{colors.GREEN}{colors.BOLD}MAIN_DIR: {path_name}{colors.RESET}\n")
                for name in dirs:
                    if name.is_file() and name.name.endswith(".c"):
                        fsyn.run_norm_CF(name)
                    elif name.is_file() and name.name.endswith(".h"):
                        fsyn.run_norm_HF(name)
                    elif name.is_dir():
                        with os.scandir(name) as nother_dirs:
                            print(f"{colors.YELLOW}|----|>{colors.RESET} {colors.BLUE}{colors.BOLD}{name.name}{colors.RESET}")
                            for name in nother_dirs:
                                if name.is_file() and name.name.endswith(".c"):
                                    fsyn.run_norm_CF(name)
                                elif name.is_file() and name.name.endswith(".h"):
                                    fsyn.run_norm_HF(name)
                                else:
                                    pass
                    else:
                        pass                
        else:
            print(f"{colors.RED}{colors.BOLD}['{sys.argv[2]}' not found!] try: python3 main.py --help or -h to see manual{colors.RESET}\n")

    else:
        print(f"{colors.RED}{colors.BOLD}try: python3 main.py --help or -h to see manual{colors.RESET}\n")

            

if __name__ == "__main__":
    main()