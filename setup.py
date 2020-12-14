import os
import platform

from setuptools import Extension, setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBDEFLATE_DIR = os.path.join(BASE_DIR, "libdeflate")

with open(os.path.join(BASE_DIR, "README.md"), "r") as readme:
    long_description = readme.read()

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
    version="0.3.0",
    description="Python wrapper for libdeflate.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dan Watson",
    author_email="dcwatson@gmail.com",
    url="https://github.com/dcwatson/deflate",
    license="MIT",
    ext_modules=[deflate],
)
