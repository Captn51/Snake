# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable

build_options = {
    "packages": ["pygame"],
    "excludes": ["numpy"],    # Des parties de numpy sont présentes par défaut...
    "include_files": ["snake.ico"]
}
executables = [
    Executable("__main__.py", base="Console", targetName="Snake.exe", icon="snake.ico")
]

setup(
    name="Snake",
    options={"build_exe": build_options},
    executables=executables
)

