from collections.abc import Buffer

# This is what it was before 3.12
# Buffer = Union[bytearray, memoryview, array.array[Any], mmap.mmap, ctypes._CData]

__version__: str

class DeflateError(Exception): ...

def adler32(data: Buffer, initial: int = 1) -> int:
    """
    Computes the Adler-32 checksum of `data`, using `initial` as the initial value.
    """
    ...

def crc32(data: Buffer, initial: int = 0) -> int:
    """
    Computes the CRC-32 checksum of `data`, using `initial` as the initial value.
    """
    ...

def deflate_compress(data: Buffer, compresslevel: int = 6) -> bytearray:
    """
    Compresses `data` using DEFLATE. `compresslevel` must be between 1 and 12.
    """
    ...

def deflate_decompress(data: Buffer, originalsize: int) -> bytearray:
    """
    Decompresses `data` using DEFLATE. `originalsize` must be (at least) the length of
    the original uncompressed data.
    """
    ...

def gzip_compress(data: Buffer, compresslevel: int = 6) -> bytearray:
    """
    Compresses `data` using GZip. `compresslevel` must be between 1 and 12.
    """
    ...

def gzip_decompress(data: Buffer, originalsize: int = 0) -> bytearray:
    """
    Decompresses `data` using GZip. `originalsize`, if specified, must be (at least)
    the length of the original uncompressed data. If unspecified or 0, the original size
    will be parsed from the GZip data footer.
    """
    ...

def zlib_compress(data: Buffer, compresslevel: int = 6) -> bytearray:
    """
    Compresses `data` using zlib. `compresslevel` must be between 1 and 12.
    """
    ...

def zlib_decompress(data: Buffer, originalsize: int) -> bytearray:
    """
    Decompresses `data` using zlib. `originalsize` must be (at least) the length of
    the original uncompressed data.
    """
    ...
