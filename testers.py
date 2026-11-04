import os
import shutil
import subprocess

BASE = os.path.dirname(os.path.realpath(__file__))
TESTER_DIR = os.path.join(BASE, "TESTER")

TESTERS = {
    "libft":  {"dir": "LIBFT_TESTER",  "build_first": True},   
    "printf": {"dir": "PRINTF_TESTER", "build_first": True},   
    "gnl":    {"dir": "GNL_TESTER",    "build_first": False},  
}

TMP_NAME = ".cc_audit_tester"

def run_tester(name, project_path, goals=None):
    conf = TESTERS[name]
    src = os.path.join(TESTER_DIR, conf["dir"])
    project = os.path.realpath(project_path)
    goals = goals or []

    if not os.path.isdir(src):
        print(f"Tester not found: {src}")
        return 1
    if not os.path.isdir(project):
        print(f"Project folder not found: {project}")
        return 1

    if conf["build_first"]:
        print(f"Building your project with make in {project} ...")
        rc = subprocess.run(["make"], cwd=project).returncode
        if rc != 0:
            print("Your project failed to build, tester not started.")
            return rc

    dest = os.path.join(project, TMP_NAME)
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(src, dest)
    try:
        return subprocess.run(["make", *goals], cwd=dest).returncode
    finally:
        shutil.rmtree(dest, ignore_errors=True)