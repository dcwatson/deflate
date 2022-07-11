deflate API
===========

This is a very thin Python wrapper Eric Biggers' excellent
[libdeflate](https://github.com/ebiggers/libdeflate).

Currently, it only handles:

compression and decompression of gzip data, with a very basic API
-----------------------------------------------------------------

```python
import deflate
level = 6  # The default; may be 1-12 for libdeflate.
compressed = deflate.gzip_compress(b"hello world!" * 1000, level)
original = deflate.gzip_decompress(compressed)
```

crc32 computation
-----------------

```python
import deflate
crc32 = deflate.crc32(b"hello world! ")  # initial
crc32 = deflate.crc32(b"hello universe!", crc32)  # continued
```


adler32 computation
-----------------

```python
import deflate
adler32 = deflate.adler32(b"hello world! ")  # initial
adler32 = deflate.adler32(b"hello universe!", adler32)  # continued
```

Installation
============

Installing `deflate` will either link to or compile `libdeflate`, depending on the
following:

1. If a `LIBDEFLATE_PREFIX` environment variable is set, it will always be used to look
   for a system-installed `libdeflate`.
2. If the `pkgconfig` package is installed, it will be used to automatically find (and
   link to) a system-installed `libdeflate` if available.
3. Falls back to compiling the bundled libdeflate code. This behavior can be triggered
   manually by setting `USE_BUNDLED_DEFLATE=1`.


```
export USE_BUNDLED_DEFLATE=no  # default is no
export LIBDEFLATE_PREFIX=/path/to/lib/deflate  # default: no path given
pip install pkgconfig  # optional, you also need pkg-config cli tool
pip install deflate
```
