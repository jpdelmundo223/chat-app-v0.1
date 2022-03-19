from setuptools import setup
from setuptools import find_packages

setup(
    name="Chat App using Flask-SocketIO",
    packages=find_packages(),
    version="0.1",
    description="A simple chat application developed using Flask-SocketIO",
    author="John Paul Del Mundo",
    author_email="jpdelmundo223@gmail.com",
    requires=[
        "flask",
        "flask-socketio",
        "eventlet",
        "gevent",
        "flask-migrate",
        "flask-sqlalchemy"
    ]
)