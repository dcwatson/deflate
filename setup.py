import os
import platform
import subprocess
import sysconfig

from distutils.command.build_ext import build_ext
from setuptools import Extension, setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APPLE_UNIVERSAL = os.getenv("APPLE_UNIVERSAL", "0") == "1"

with open(os.path.join(BASE_DIR, "README.md"), "r") as readme:
    long_description = readme.read()


def env(**kwargs):
    base = {"PATH": os.environ["PATH"]}
    for name, value in kwargs.items():
        base[name.upper()] = value
    return base


class DeflateBuilder(build_ext):
    def run(self, *args, **kwargs):
        build_dir = os.path.join(BASE_DIR, "build")
        libdeflate_dir = os.path.join(BASE_DIR, "libdeflate")
        # Check to see if we're building on Apple Silicon.
        is_apple_silicon = platform.system() == "Darwin" and platform.machine() == "arm64"
        # Building a universal library (at least right now) means building libdeflate twice and joining them.
        if is_apple_silicon and APPLE_UNIVERSAL:
            lipo_libs = []
            # Make sure we target the same version of macOS Python did, so the linker doesn't complain.
            target = sysconfig.get_config_var("MACOSX_DEPLOYMENT_TARGET")
            os.makedirs(build_dir, exist_ok=True)
            for arch in ("arm64", "x86_64"):
                lib_name = os.path.join(build_dir, "libdeflate.{}.a".format(arch))
                cflags = "-fPIC -arch {} -mmacosx-version-min={}".format(arch, target)
                # -B tells make to always rebuild, so we don't need to clean between builds.
                subprocess.run(["make", "clean", "libdeflate.a"], cwd=libdeflate_dir, env=env(cflags=cflags))
                subprocess.run(["mv", "-f", "libdeflate.a", lib_name], cwd=libdeflate_dir)
                lipo_libs.append(lib_name)
            # Join all the architectures into a single universal library.
            result = subprocess.run(["lipo", "-create", *lipo_libs, "-output", "libdeflate.a"], cwd=libdeflate_dir)
        else:
            # Only need to build the static library we're going to link, no need for programs.
            # Even though we build libdeflate as static, we might be built as shared, so make sure libdeflate is PIC.
            result = subprocess.run(["make", "clean", "libdeflate.a"], cwd=libdeflate_dir, env=env(cflags="-fPIC"))
        if result.returncode == 0:
            super().run(*args, **kwargs)
            """"
            if is_apple_silicon and not APPLE_UNIVERSAL:
                # Our extension will likely have been built universal, so if we didn't also build libdeflate universal,
                # thin out the resulting library to just arm64.
                for lib in self.get_outputs():
                    subprocess.run(["lipo", lib, "-thin", "arm64", "-output", lib])
            """
        else:
            print("*** Failed to build libdeflate")


deflate = Extension(
    "deflate", sources=["deflate.c"], extra_objects=["libdeflate/libdeflate.a"]
)

setup(
    name="deflate",
    version="0.2.0",
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
