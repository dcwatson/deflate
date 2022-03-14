# test crc32 function

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
def test_crc32_simple(data):
    """test whether crc32 function computes correctly (reference: zlib.crc32)"""
    assert deflate.crc32(data) == zlib.crc32(data)


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
def test_crc32_with_start_value(data):
    """test whether crc32 function computes correctly,
    with start value (reference: zlib.crc32)"""
    # 0 is the default start value
    assert deflate.crc32(data, 0) == deflate.crc32(data)
    # 0 start value behaviour as in zlib
    assert deflate.crc32(data, 0) == zlib.crc32(data, 0)
    # "random" start value behaviour as in zlib
    assert deflate.crc32(data, deflate.crc32(data, 0)) == zlib.crc32(
        data, zlib.crc32(data, 0)
    )
    # continued crc32 computation yields same result as in one go
    assert deflate.crc32(data, deflate.crc32(data, 0)) == deflate.crc32(data * 2, 0)
