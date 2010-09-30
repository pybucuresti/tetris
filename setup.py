from setuptools import setup, find_packages

setup(
    name="tetris",
    packages=find_packages(),
    install_requires=[],
    entry_points={'console_scripts': [
        'tetris = tetris.cmd:main']},
)
