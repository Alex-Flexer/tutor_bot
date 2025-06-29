from subprocess import Popen
import sys
import os


def set_work_dir():
    work_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(work_dir)
    sys.path.insert(0, work_dir)
    return work_dir


if __name__ == "__main__":
    work_dir = set_work_dir()
    Popen(["python", "main_bot.py"], cwd=work_dir)
    Popen(["python", "admin_bot.py"], cwd=work_dir)
