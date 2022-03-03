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

deflate package installation
============================

deflate will:
- use libdeflate from LIBDEFLATE_PREFIX when given
- use pkgconfig pypi package (if available) to locate a libdeflate
- fall back to bundled libdeflate code otherwise or when enforced via 
  USE_BUNDLED_DEFLATE=yes. 

```
export USE_BUNDLED_DEFLATE=no  # default is no
export LIBDEFLATE_PREFIX=/path/to/lib/deflate  # default: no path given
pip install pkgconfig  # optional, you also need pkg-config cli tool
pip install deflate
```
