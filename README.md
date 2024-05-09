# deflate API

This is a very thin Python wrapper Eric Biggers' excellent
[libdeflate](https://github.com/ebiggers/libdeflate).

Currently, it handles:

## Compression and decompression of gzip data, with a very basic API

```python
import deflate
level = 6  # The default; may be 1-12 for libdeflate.
compressed = deflate.gzip_compress(b"hello world!" * 1000, level)
original = deflate.gzip_decompress(compressed)
```

## Compression and decompression of raw DEFLATE or zlib data

The original size of the decompressed data needs to be kept through additional logic.

```python
import deflate
level = 6  # The default; may be 1-12 for libdeflate.
data = b"hello world!" * 1000
# DEFLATE
compressed = deflate.deflate_compress(data, level)
original = deflate.deflate_decompress(compressed, len(data))
# zlib
compressed = deflate.zlib_compress(data, level)
original = deflate.zlib_decompress(compressed, len(data))
```

## CRC32 computation

```python
import deflate
crc32 = deflate.crc32(b"hello world! ")  # initial
crc32 = deflate.crc32(b"hello universe!", crc32)  # continued
```

## Adler-32 computation

```python
import deflate
adler32 = deflate.adler32(b"hello world! ")  # initial
adler32 = deflate.adler32(b"hello universe!", adler32)  # continued
```

# Installation

`pip install deflate`

By default, `deflate` will compile and statically link the bundled `libdeflate` when you
build from source. To link to a system-installed `libdeflate`, set the
`LIBDEFLATE_PREFIX` environment variable:

```
LIBDEFLATE_PREFIX=/opt/homebrew/Cellar/libdeflate/1.20 python -m build
```

# Testing

```
pip install -r requirements-dev.lock
python -m pytest
```
