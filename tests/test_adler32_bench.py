# benchmark deflate adler32 against zlib adler32
# note: we have other tests for correctness of the result, so we do not check it here.

import os
import zlib

import deflate

data = os.urandom(10 * 1000000)


def test_deflate_adler32(benchmark):
    @benchmark
    def result():
        deflate.adler32(data)


def test_zlib_adler32(benchmark):
    @benchmark
    def result():
        zlib.adler32(data)
