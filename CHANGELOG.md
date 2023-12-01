## 0.5.0

* Added raw DEFLATE functionality from libdeflate


## 0.4.0

* Eliminate unnecessary allocation/copy in compression and decompression (#10)
* add DeflateError object to module, fixes related ImportError (#14)
* add deflate.crc32 api, docs, tests (#11)
* update bundled code to libdeflate v1.18 (#38)
* prefer system libdeflate (via pkgconfig) over bundled code, see the docs
  about how to influence this behaviour via environment variables (#29)
* setup.py: add pypi metadata, require python >= 3.8
* benchmark deflate.crc32 against zlib.crc32 using pytest-benchmark
* add tests (using pytest), flake8 linter, CI via github actions (#16, #13)


## 0.3.0

* Compile libdeflate directly instead of trying to build/link it
* Actual working Windows binary wheels
* Change the default compression level to 6 to match zlib


## 0.2.0

* Compile libdeflate with `-fPIC` (#5)
* Automatically build wheels for macOS, Linux, and Windows (#3)
* Fixed a memory leak (#6)
* Experimental support for building a universal library on Apple Silicon


## 0.1.0

* Initial release
