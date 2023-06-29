import os
import platform
import re

from setuptools import Extension, setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBDEFLATE_DIR = os.path.join(BASE_DIR, "libdeflate")
TRUISH_VALUES = ("1", "true", "t", "yes", "y")

with open(os.path.join(BASE_DIR, "README.md"), "r") as readme:
    long_description = readme.read()

with open(os.path.join(BASE_DIR, "deflate.c"), "r") as src:
    version = re.match(r'.*#define MODULE_VERSION "(.*?)"', src.read(), re.S).group(1)

prefer_system_libdeflate = (
    os.environ.get("USE_BUNDLED_DEFLATE", "").lower() not in TRUISH_VALUES
)
system_prefix_libdeflate = os.environ.get("LIBDEFLATE_PREFIX")

try:
    import pkgconfig as pc
except ImportError:
    if prefer_system_libdeflate and not system_prefix_libdeflate:
        print("Warning: can not import pkgconfig python package.")
    pc = None

deflate_sources = [
    "deflate.c",
]

if prefer_system_libdeflate and system_prefix_libdeflate:
    print("Detected and preferring libdeflate [via LIBDEFLATE_PREFIX]")
    extension_kwargs = dict(
        include_dirs=[os.path.join(system_prefix_libdeflate, "include")],
        library_dirs=[os.path.join(system_prefix_libdeflate, "lib")],
        libraries=["deflate"],
    )
elif prefer_system_libdeflate and pc and pc.installed("libdeflate", ">= 1.10"):
    print("Detected and preferring libdeflate [via pkgconfig]")
    extension_kwargs = pc.parse("libdeflate")
else:
    cpu = "arm" if platform.machine().startswith("arm") else "x86"
    print(f"Using bundled libdeflate [{cpu}]")
    deflate_sources.extend(
        [
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
        ]
    )
    extension_kwargs = dict(include_dirs=[LIBDEFLATE_DIR], extra_compile_args=["-w"])

deflate = Extension("deflate", deflate_sources, **extension_kwargs)

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
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving :: Compression",
    ],
    python_requires=">=3.8",
)
