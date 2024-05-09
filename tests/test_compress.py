# test compress / decompress functionality

import gzip
import os
import zlib

import pytest

import deflate


@pytest.mark.parametrize(
    "data",
    [
        b"",
        b"\0",
        b"\0" * 23,
        b"foobar",
        b"foobar" * 42,
        os.urandom(50),
    ],
)
def test_roundtrip(data):
    """test whether decompressing compressed data yields the original data"""
    assert deflate.gzip_decompress(deflate.gzip_compress(data)) == data
    assert deflate.gzip_decompress(gzip.compress(data)) == data
    assert gzip.decompress(deflate.gzip_compress(data)) == data

    assert deflate.zlib_decompress(deflate.zlib_compress(data), len(data)) == data
    assert deflate.zlib_decompress(zlib.compress(data), len(data)) == data
    assert zlib.decompress(deflate.zlib_compress(data)) == data

    assert deflate.deflate_decompress(deflate.deflate_compress(data), len(data)) == data


@pytest.mark.parametrize("compresslevel", range(1, 12 + 1))
def test_shorter(compresslevel):
    """tests whether compressed data is actually shorter than original data and
    also uses all supported compresslevels"""
    data = b"foobar" * 123
    len_original = len(data)
    len_compressed = len(deflate.gzip_compress(data, compresslevel))
    print(compresslevel, len_original, len_compressed)
    assert len_compressed < len_original


@pytest.mark.parametrize("compresslevel", [-1, 0, 13, 256, 65536])
def test_unsupported_compresslevel(compresslevel):
    """test if compresslevels outside of supported range raise ValueError"""
    with pytest.raises(ValueError):
        deflate.gzip_compress(b"foobar", compresslevel)


@pytest.mark.parametrize(
    "compressed",
    [
        b"",
        b"\0",
        b"\0" * 23,
        b"foobar",
        b"foobar" * 42,
    ],
)
def test_invalid_decompression(compressed):
    """test whether giving invalid data to decompress raises ValueError"""
    with pytest.raises(ValueError):
        deflate.gzip_decompress(compressed)
