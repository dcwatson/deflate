import os
import subprocess

from distutils.command.build_ext import build_ext
from setuptools import Extension, setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(BASE_DIR, "README.md"), "r") as readme:
    long_description = readme.read()


class DeflateBuilder(build_ext):
    def run(self, *args, **kwargs):
        libdeflate_dir = os.path.join(BASE_DIR, "libdeflate")
        result = subprocess.run(["make"], cwd=libdeflate_dir)
        if result.returncode == 0:
            super().run(*args, **kwargs)
        else:
            print("*** Failed to build libdeflate")


deflate = Extension(
    "deflate", sources=["deflate.c"], extra_objects=["libdeflate/libdeflate.a"]
)

setup(
    name="deflate",
    version="0.1.0",
    description="Python wrapper for libdeflate.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dan Watson",
    author_email="dcwatson@gmail.com",
    url="https://github.com/dcwatson/deflate",
    license="MIT",
    cmdclass={"build_ext": DeflateBuilder},
    ext_modules=[deflate],
)
