import os
import subprocess
from uranium import task_requires


def main(build):
    build.packages.install(".", develop=True)


@task_requires("main")
def test(build):
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    build.packages.install("aiohttp")
    build.packages.install("pytest-sanic")
    build.packages.install("radon")
    build.executables.run([
        "pytest", "./tests",
        "--cov", "sanic_transmute",
        "--cov-report", "term-missing",
        "--disable-pytest-warnings",
    ] + build.options.args)


def distribute(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.packages.install("twine")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "upload",
    ])
    build.executables.run([
        "twine", "upload", "dist/*"
    ])


@task_requires("main")
def build_docs(build):
    build.packages.install("sphinx")
    build.packages.install("sphinx_rtd_theme")
    return subprocess.call(
        ["make", "html"], cwd=os.path.join(build.root, "docs")
    )