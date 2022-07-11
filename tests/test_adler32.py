# test adler32 function

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
def test_adler_simple(data):
    """test whether adler32 function computes correctly (reference: zlib.adler32)"""
    assert deflate.adler32(data) == zlib.adler32(data)


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
def test_adler32_with_start_value(data):
    """test whether adler32 function computes correctly,
    with start value (reference: zlib.adler32)"""
    # 1 is the default start value
    assert deflate.adler32(data,1) == deflate.adler32(data)
    # 1 start value behaviour as in zlib
    assert deflate.adler32(data, 1) == zlib.adler32(data, 1)
    # "random" start value behaviour as in zlib
    assert deflate.adler32(data, deflate.adler32(data, 0)) == zlib.adler32(
        data, zlib.adler32(data, 0)
    )
    # continued adler32 computation yields same result as in one go
    assert deflate.adler32(data, deflate.adler32(data, 0)) == deflate.adler32(
        data * 2, 0
    )
