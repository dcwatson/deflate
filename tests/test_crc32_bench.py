# benchmark deflate crc32 against zlib crc32
# note: we have other tests for correctness of the result, so we do not check it here.

import os
import zlib

import deflate

data = os.urandom(10 * 1000000)


def test_deflate_crc32(benchmark):
    @benchmark
    def result():
        deflate.crc32(data)


def test_zlib_crc32(benchmark):
    @benchmark
    def result():
        zlib.crc32(data)
