# test compress / decompress functionality

import array
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
        os.urandom(500),
        bytearray(b"hello world") * 100,
        memoryview(b"hello world" * 100),
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


def test_array():
    """test roundtripping compressed array.array values"""
    a = array.array("d", [-42.0, 1.0, 2.0, 3.14, float("inf"), float("-inf")])
    c = deflate.gzip_compress(a)
    b = array.array("d", deflate.gzip_decompress(c))
    assert a == b


@pytest.mark.parametrize("compresslevel", range(1, 12 + 1))
def test_shorter(compresslevel):
    """tests whether compressed data is actually shorter than original data and
    also uses all supported compresslevels"""
    data = b"foobar" * 123
    len_original = len(data)
    len_compressed = len(deflate.gzip_compress(data, compresslevel))
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


def test_decompress_resize():
    """test that decompressing with overestimated originalsize works, and fails when
    originalsize is too small"""
    block = os.urandom(4096)
    compressed = deflate.gzip_compress(block)
    result = deflate.gzip_decompress(compressed, 5000)
    assert block == result
    with pytest.raises(deflate.DeflateError):
        deflate.gzip_decompress(compressed, 3000)
