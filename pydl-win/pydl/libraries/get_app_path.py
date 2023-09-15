# from: https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
import os
import sys
import platformdirs

config_name = "pydl.conf"


def config():
    config_dir = platformdirs.user_config_dir(appname="pydl", appauthor="gro-david", ensure_exists=True)
    config_path = os.path.join(config_dir, config_name)
    return config_path


def main():
    # determine if application is a script file or frozen exe
    if getattr(sys, "frozen", False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.join(__file__, os.path.join(os.pardir, os.pardir))
    return application_path
