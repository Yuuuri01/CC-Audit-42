<div align="center">
  <h1> CC-AUDIT-42</h1>
  <p><strong>A Lightweight & Modular C Audit CLI Tool</strong></p>
  
  ![Python](https://img.shields.io/badge/Language-Python_3-yellow.svg)
  ![C](https://img.shields.io/badge/Target-C-blue.svg)
  ![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)
  ![License](https://img.shields.io/badge/License-MIT-green.svg)
</div>

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Yuuuri01/READMENOW/main/CC-Audit-42-linkedin.png" alt="CC-Audit Banner" width="100%">
</p>

## Overview

**CC-Audit-42** is a modular C audit CLI tool designed for 1337 and 42 Network students. It streamlines the workflow by automating syntax validation, norm enforcement, and running the community testers for **libft**, **ft_printf** and **get_next_line** from a single command.

Instead of manually checking each file, CC-Audit-42 traverses directories, validates syntax using strict compiler flags, runs `norminette`, and launches the testers on your project, all presented through a clean, color-coded terminal interface.

## Key Features

*   **Syntax Checking (`-s`, `--syntax`)**: Recursively compiles C source files using strict flags (`-Wall -Wextra -Werror -fsyntax-only`). It ensures code validity without leaving behind cluttered binary outputs.
*   **Norminette Audit (`-d`, `--dir`)**: Automatically enforces the 42 Norme by running `norminette` on all `.c` and `.h` files within a specified directory and its sub-folders.
*   **Comprehensive Audit (`-l`, `--check-all`)**: Combines both syntax compilation and norm verification in a single pass.
*   **Single File Audit (`-f`, `--file`)**: Provides a quick, targeted check for individual source or header files.
*   **Tester Launcher (`--libft`, `--printf`, `--gnl`)** *(new)*: Runs the libft, ft_printf and get_next_line testers on your project with one command. You can run all tests of a tester or only the ones you choose.
*   **Exit Codes** *(new)*: Returns `0` on success and `1` when errors are found, so the tool can be used in scripts and CI.
*   **Clean Diagnostic Output**: Captures `stderr` to display compilation errors clearly and accurately.

##  Under the Hood

The architecture of CC-Audit-42 relies on Python's standard library:

*   **Modular layout**: `audit.py` parses the options and dispatches, `fsyn.py` runs the norminette checks, `colors.py` handles the terminal colors, and `testers.py` manages the testers.
*   **Process Management**: Uses `subprocess.run` with argument lists (no `shell=True`), so file names with spaces or special characters are handled safely.
*   **Efficient Traversal**: Uses `glob` and `os.scandir` for directory exploration.
*   **Error Handling**: Captures `stderr` from the compiler and checks that required tools exist before running them.
*   **Tester Execution**: The testers look for your project in their **parent folder**. To make this work, CC-Audit-42 builds your project, copies the tester into a temporary hidden folder inside your project (`.cc_audit_tester`), runs it, and always deletes the copy afterwards, even if the tester crashes. Your project stays clean.

## Project Structure

```
CC-Audit-42/
├── audit.py        # entry point: options and dispatch
├── fsyn.py         # norminette checks for .c / .h files
├── colors.py       # terminal colors
├── testers.py      # launcher for the libft / printf / gnl testers
├── usage.txt       # text shown by --help
├── TESTER/
│   ├── LIBFT_TESTER/
│   ├── PRINTF_TESTER/
│   └── GNL_TESTER/
├── LICENSE
└── README.md
```

## Prerequisites

To run CC-Audit-42, ensure you have the following installed in your Linux environment:

*   Python 3.x
*   `gcc` or `cc` (C compiler, used for the syntax check)
*   `norminette` (42 Network norm checker)

Additionally, **for the testers**:

*   `make`
*   `clang++` (the testers are written in C++)
*   `valgrind` (used by the testers on Linux for leak checks)

## Environment Setup (Recommended)

If `norminette` is not installed globally on your system, it is highly recommended to use a Python virtual environment (`venv`).

**Why use a Virtual Environment?**
It isolates the tool's dependencies from your system's global Python packages. This prevents version conflicts and keeps your core system clean, ensuring `norminette` works exactly as expected for this specific tool.

### 1. Create and Activate the Environment
Open your terminal inside the project directory and run:

```bash
# Create the virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 2. Install Dependencies
Once the environment is active (you will see `(venv)` in your prompt), install `norminette`:

```bash
pip install --upgrade pip
pip install norminette
```

*(To exit the isolated environment when you are done, simply run: `deactivate`)*

## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Yuuuri01/CC-Audit-42.git CC-Audit-42
   cd CC-Audit-42
   ```

2. **Make the script executable:**
   ```bash
   chmod +x audit.py
   ```

3. **Run a basic audit:**
   *(Ensure your virtual environment is active if you used one)*
   ```bash
   ./audit.py [OPTION] [PATH]
   ```

> ⚠️ An **option is always required** before the path. `./audit.py my_project` does nothing but print the help hint; use `./audit.py -d my_project` instead.

### Options & Manual

| Option | Description | Example |
| :--- | :--- | :--- |
| `-h`, `--help` | Show the help manual | `./audit.py -h` |
| `-f`, `--file` | Audit a single `.c` or `.h` file | `./audit.py -f C05/ft_strlen.c` |
| `-d`, `--dir` | Run Norminette audit on a directory | `./audit.py -d C05` |
| `-s`, `--syntax` | Run recursive syntax check on a directory | `./audit.py -s C05` |
| `-l`, `--check-all` | Run both syntax check & norminette audit | `./audit.py --check-all C05` |
| `--libft PATH` | Run the libft tester on your project | `./audit.py --libft ~/libft` |
| `--printf PATH` | Run the ft_printf tester on your project | `./audit.py --printf ~/ft_printf` |
| `--gnl PATH` | Run the get_next_line tester on your project | `./audit.py --gnl ~/get_next_line` |
| `--only TESTS...` | Run only specific tests (after a tester option) | `./audit.py --libft ~/libft --only strlen split` |

## Testers (libft, ft_printf, get_next_line)

CC-Audit-42 can launch three community testers stored in the `TESTER/` folder. `PATH` must be the folder that contains **your project** (your `Makefile` and `.c` files).

### Usage

```bash
# libft: all tests, or only some functions
./audit.py --libft ~/libft
./audit.py --libft ~/libft --only strlen split

# ft_printf: all tests, or only some (test names, then optional test numbers)
./audit.py --printf ~/ft_printf
./audit.py --printf ~/ft_printf --only c s

# get_next_line
./audit.py --gnl ~/get_next_line
```

### How each tester finds your project

| Tester | What your project folder must provide |
| :--- | :--- |
| `--libft` | A `Makefile` that builds **`libft.a`** |
| `--printf` | A `Makefile` that builds **`libftprintf.a`** |
| `--gnl` | `get_next_line.c`, `get_next_line_utils.c` and `get_next_line.h` (plus the `_bonus` files for bonus tests) |

For `--libft` and `--printf`, CC-Audit-42 runs `make` in your project first. If your project fails to build, or the library is missing, the tester is not started and you get a clear message.

### Troubleshooting

*   **`'clang++' is required but not installed`**: install `clang` and `valgrind` with your package manager.
*   **`libft.a not found`**: your `Makefile` must create the library in the root of the project folder you passed.
*   **Wrong path**: run `ls PATH` first; you should see your `Makefile` and source files.

##  Adding the Tool to your System `PATH` (Global Command)

To run `CC-Audit-42` from any directory in your terminal like a real system command:

1. **Create a symbolic link** to a directory in your system's `PATH` (e.g., `~/.local/bin`):
   ```bash
   mkdir -p ~/.local/bin
   ln -s "$(pwd)/audit.py" ~/.local/bin/CC-Audit-42
   ```
   *(Ensure `~/.local/bin` is in your `~/.bashrc` or `~/.zshrc` via `export PATH="$HOME/.local/bin:$PATH"`)*

2. **Run it globally:**
   ```bash
   CC-Audit-42 --check-all C05
   CC-Audit-42 --libft ~/libft
   ```

The tool resolves its real location, so `--help` and the testers work from any folder.

## Credits & Licenses

The testers in `TESTER/` are **third-party open-source projects** and belong to their original authors. They keep their own licenses, which are included in their folders.

| Tester | Author / Repository |
| :--- | :--- |
| `LIBFT_TESTER` | *(add author and GitHub link)* |
| `PRINTF_TESTER` | *(add author and GitHub link)* |
| `GNL_TESTER` | *(add author and GitHub link)* |

CC-Audit-42 only launches them; it does not modify their code. Thank you to their authors for making them available.

## 👨‍💻 Author
--> (Yuuuri-01)
Built by **Hamza Mossaid** (1337 / 42 Network Student).
Focusing on low-level C programming, algorithm optimization, and automation tools.

---
*“Automation is the key to efficiency.”*
