import sys
import os


def set_work_dir():
    work_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(work_dir)
    sys.path.insert(0, work_dir)
    return work_dir


if __name__ == "__main__":
    work_dir = set_work_dir()

    START_CMD = "pm2 start"
    RELOAD_CMD = "pm2 reload"
    INTERPRETER = "--interpreter ./venv/bin/python"

    paths = ["main_bot", "admin_bot"]

    if len(sys.argv) > 1 and sys.argv[1] == "--reload":
        for path in paths:
            os.system(' '.join(RELOAD_CMD, path))
    else:
        for path in paths:
            os.system(' '.join(RELOAD_CMD, path, INTERPRETER))
