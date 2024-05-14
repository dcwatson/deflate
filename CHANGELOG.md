## 0.8.0 (unreleased)

* Use only the [limited Python API](https://docs.python.org/3/c-api/stable.html)
    * Use the Stable ABI for Python 3.11+
* Return [bytearray](https://docs.python.org/3/library/stdtypes.html#bytearray) from compression and decompression methods to avoid copying (resizing bytes is private API)
* Added typing stubs (and a shell python package to hold them and the renamed `_deflate` compiled extension) (#49)
* Added support and compiled wheels for PyPy.


## 0.7.0 (2024-05-09)

* Switched to [scikit-build-core](https://github.com/scikit-build/scikit-build-core) and CMake (#42, #43) - huge thanks to @henryiii
* Raise `ValueError` instead of `DeflateError` on invalid gzip data
* Lots of internal refactoring


## 0.6.1 (2024-05-06)

* Fixed broken wheels on macOS arm64 platforms


## 0.6.0 (2024-04-20, yanked)

* Require `originalsize` argument for `deflate_decompress` and `zlib_decompress`
* Updated bundled libdeflate to v1.20


## 0.5.0 (2023-12-20)

* Added raw DEFLATE functionality from libdeflate (#39)
* Added zlib functionality from libdeflate (#2)
* Updated bundled libdeflate to v1.19
* Test on and build wheels for Python 3.12 (#40)


## 0.4.0 (2023-06-29)

* Eliminate unnecessary allocation/copy in compression and decompression (#10)
* add DeflateError object to module, fixes related ImportError (#14)
* add deflate.crc32 api, docs, tests (#11)
* update bundled code to libdeflate v1.18 (#38)
* prefer system libdeflate (via pkgconfig) over bundled code, see the docs
  about how to influence this behaviour via environment variables (#29)
* setup.py: add pypi metadata, require python >= 3.8
* benchmark deflate.crc32 against zlib.crc32 using pytest-benchmark
* add tests (using pytest), flake8 linter, CI via github actions (#16, #13)


## 0.3.0 (2020-12-14)

* Compile libdeflate directly instead of trying to build/link it
* Actual working Windows binary wheels
* Change the default compression level to 6 to match zlib


## 0.2.0 (2020-11-19)

* Compile libdeflate with `-fPIC` (#5)
* Automatically build wheels for macOS, Linux, and Windows (#3)
* Fixed a memory leak (#6)
* Experimental support for building a universal library on Apple Silicon


## 0.1.0 (2020-06-17)

* Initial release
