import os
import platform
import re

from setuptools import Extension, setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBDEFLATE_DIR = os.path.join(BASE_DIR, "libdeflate")

with open(os.path.join(BASE_DIR, "README.md"), "r") as readme:
    long_description = readme.read()

with open(os.path.join(BASE_DIR, "deflate.c"), "r") as src:
    version = re.match(r'.*#define MODULE_VERSION "(.*?)"', src.read(), re.S).group(1)

cpu = "arm" if platform.machine().startswith("arm") else "x86"
deflate = Extension(
    "deflate",
    sources=[
        "libdeflate/lib/adler32.c",
        "libdeflate/lib/crc32.c",
        "libdeflate/lib/deflate_compress.c",
        "libdeflate/lib/deflate_decompress.c",
        "libdeflate/lib/gzip_compress.c",
        "libdeflate/lib/gzip_decompress.c",
        "libdeflate/lib/utils.c",
        "libdeflate/lib/zlib_compress.c",
        "libdeflate/lib/zlib_decompress.c",
        "libdeflate/lib/{}/cpu_features.c".format(cpu),
        "deflate.c",
    ],
    include_dirs=[LIBDEFLATE_DIR],
)

setup(
    name="deflate",
    version=version,
    description="Python wrapper for libdeflate.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dan Watson",
    author_email="dcwatson@gmail.com",
    url="https://github.com/dcwatson/deflate",
    license="MIT",
    ext_modules=[deflate],
)
