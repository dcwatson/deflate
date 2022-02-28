deflate
=======

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
