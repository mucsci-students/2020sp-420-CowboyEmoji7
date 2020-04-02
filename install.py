import subprocess, sys

requirements = [
    "Click==7.0",
    "Flask==1.1.1",
    "flask-marshmallow==0.10.1",
    "Flask-SQLAlchemy==2.4.1",
    "itsdangerous==1.1.0",
    "Jinja2==2.11.1",
    "MarkupSafe==1.1.1",
    "marshmallow==3.4.0",
    "marshmallow-sqlalchemy==0.21.0",
    "six==1.14.0",
    "SQLAlchemy==1.3.13",
    "Werkzeug==0.16.1",
    "parse==1.15.0"
]

windows = [
    "pyreadline"
]

linux = [
    "readline"
]

mac = [
    "gnureadline"
]

def install(list):
    for thing in list:
        subprocess.check_call([sys.executable, "-m", "pip", "install", thing])
        
if __name__ == "__main__":
    from sys import platform
    install(requirements)
    print("Preparing to install OS specific requirements...")
    if platform.startswith("win"):
        install(windows)
    if platform.startswith("darwin"):
        install(mac)
    if platform.startswith("linux"):
        install(linux)