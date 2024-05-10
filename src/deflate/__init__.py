from ._deflate import (
    DeflateError,
    __version__,
    adler32,
    crc32,
    deflate_compress,
    deflate_decompress,
    gzip_compress,
    gzip_decompress,
    zlib_compress,
    zlib_decompress,
)

__all__ = [
    "DeflateError",
    "__version__",
    "adler32",
    "crc32",
    "deflate_compress",
    "deflate_decompress",
    "gzip_compress",
    "gzip_decompress",
    "zlib_compress",
    "zlib_decompress",
]
