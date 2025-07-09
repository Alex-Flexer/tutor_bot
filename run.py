import sys
import os


def set_work_dir():
    work_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(work_dir)
    sys.path.insert(0, work_dir)
    return work_dir


if __name__ == "__main__":
    work_dir = set_work_dir()

    if len(sys.argv) > 1 and sys.argv[1] == "--reload":
        os.system("pm2 reload main_bot")
        os.system("pm2 reload admin_bot")
    else:
        os.system("pm2 start main_bot.py --interpreter ./venv/bin/python")
        os.system("pm2 start admin_bot.py --interpreter ./venv/bin/python")

