<div align="center">
  <h1>🚀 CC-auto</h1>
  <p><strong>A Lightweight & Modular C Audit CLI Tool</strong></p>
  
  ![Python](https://img.shields.io/badge/Language-Python_3-yellow.svg)
  ![C](https://img.shields.io/badge/Target-C-blue.svg)
  ![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)
  ![License](https://img.shields.io/badge/License-MIT-green.svg)
</div>

---

## 📖 Overview

**CC-auto** is a professional-grade, modular C audit CLI tool explicitly designed for 1337 and 42 Network students. It significantly streamlines the workflow by automating syntax validation and norm enforcement for C projects. 

Instead of manually checking each file, CC-auto traverses directories, validates syntax using strict compiler flags, and runs `norminette` checks, all presented through a clean, color-coded terminal interface.

## ✨ Key Features

*   **Syntax Checking (`-s`, `--syntax`)**: Recursively compiles C source files using strict flags (`-Wall -Wextra -Werror -fsyntax-only`). It ensures code validity without leaving behind cluttered binary outputs.
*   **Norminette Audit (`-d`, `--dir`)**: Automatically enforces the 42 Norme by running `norminette` on all `.c` and `.h` files within a specified directory.
*   **Comprehensive Audit (`--check-all`)**: Combines both syntax compilation and norm verification in a single, efficient pass.
*   **Single File Audit (`-f`, `--file`)**: Provides a quick, targeted check for individual source or header files.
*   **Clean Diagnostic Output**: Captures and redirects `stderr` to display compilation errors clearly and accurately.

## 🧠 Under the Hood

The architecture of CC-auto relies on Python's standard library to ensure robust execution and system interaction:
*   **Process Management**: Employs `subprocess.run` with `shell=True` to seamlessly allow wildcard expansion (`*/*`) for bulk file processing.
*   **Efficient Traversal**: Utilizes `os.scandir` for rapid, recursive directory exploration.
*   **Error Handling**: Intelligently redirects `stderr` to capture syntax warnings and compilation errors directly from `gcc`, ensuring they are displayed correctly to the user.

## ⚙️ Prerequisites

To run CC-auto, ensure you have the following installed in your Linux environment:
*   Python 3.x
*   `gcc` (GNU Compiler Collection)
*   `norminette` (42 Network norm checker)

## 🐍 Environment Setup (Recommended)

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

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/CC-auto.git
   cd CC-auto
   ```

2. **Make the script executable:**
   ```bash
   chmod +x main.py
   ```

3. **Run a basic audit:**
   *(Ensure your virtual environment is active if you used one)*
   ```bash
   ./main.py [OPTION] [PATH]
   ```

### Options & Manual

| Option | Description | Example |
| :--- | :--- | :--- |
| `-h`, `--help` | Show the help manual | `./main.py -h` |
| `-f`, `--file` | Audit a single `.c` or `.h` file | `./main.py -f C05/ft_strlen.c` |
| `-d`, `--dir` | Run Norminette audit on a directory | `./main.py -d C05` |
| `-s`, `--syntax` | Run recursive syntax check on a directory | `./main.py -s C05` |
| `--check-all` | Run both syntax check & norminette audit | `./main.py --check-all C05` |

## 🌍 Adding the Tool to your System `PATH` (Global Command)

To run `CC-auto` from any directory in your terminal like a real system command:

1. **Create a symbolic link** to a directory in your system's `PATH` (e.g., `~/.local/bin`):
   ```bash
   mkdir -p ~/.local/bin
   ln -s "$(pwd)/main.py" ~/.local/bin/cc-auto
   ```
   *(Ensure `~/.local/bin` is in your `~/.bashrc` or `~/.zshrc` via `export PATH="$HOME/.local/bin:$PATH"`)*

2. **Run it globally:**
   ```bash
   cc-auto --check-all C05
   ```

## 👨‍💻 Author

Built with ❤️ by **Hamza Mossaid** (1337 / 42 Network Student).
Focusing on low-level C programming, algorithm optimization, and automation tools.

---
*“Automation is the key to efficiency.”*
