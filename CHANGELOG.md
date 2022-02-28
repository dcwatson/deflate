## 0.4.0

* Eliminate unnecessary allocation/copy in compression and decompression (#10)


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
