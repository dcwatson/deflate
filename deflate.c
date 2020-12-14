#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "libdeflate/libdeflate.h"

static PyObject *DeflateError;

static PyObject *deflate_gzip_compress(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *keywords[] = {"data", "compresslevel", NULL};
    Py_buffer data;
    int compression_level = 6;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*|i", keywords, &data, &compression_level))
    {
        return NULL;
    }

    if (compression_level < 1 || compression_level > 12)
    {
        PyBuffer_Release(&data);
        PyErr_SetString(PyExc_ValueError, "compresslevel must be between 1 and 12.");
        return NULL;
    }

    struct libdeflate_compressor *compressor = libdeflate_alloc_compressor(compression_level);
    size_t bound = libdeflate_gzip_compress_bound(compressor, data.len);
    void *compressed_data = PyMem_RawMalloc(bound);
    if (compressed_data == NULL)
    {
        libdeflate_free_compressor(compressor);
        PyBuffer_Release(&data);
        return PyErr_NoMemory();
    }
    size_t compressed_size = libdeflate_gzip_compress(compressor, data.buf, data.len, compressed_data, bound);
    libdeflate_free_compressor(compressor);

    if (compressed_size == 0)
    {
        PyMem_RawFree(compressed_data);
        PyBuffer_Release(&data);
        PyErr_SetString(DeflateError, "Compression failed.");
        return NULL;
    }

    PyObject *bytes = PyBytes_FromStringAndSize(compressed_data, compressed_size);
    PyMem_RawFree(compressed_data);
    PyBuffer_Release(&data);

    return bytes;
}

static PyObject *deflate_gzip_decompress(PyObject *self, PyObject *args)
{
    Py_buffer data;

    if (!PyArg_ParseTuple(args, "y*", &data))
    {
        return NULL;
    }

    if (data.len < 6)
    {
        PyErr_SetString(DeflateError, "Invalid gzip data.");
        PyBuffer_Release(&data);
        return NULL;
    }

    // Very basic gzip header check before we go allocating memory.
    uint8_t *bytes = (uint8_t *)data.buf;
    if (bytes[0] != 0x1F || bytes[1] != 0x8B)
    {
        PyErr_SetString(DeflateError, "Invalid gzip data.");
        PyBuffer_Release(&data);
        return NULL;
    }

    // The last 4 bytes of a gzip archive are the original data size, in little endian.
    bytes = (uint8_t *)data.buf + (data.len - 4);
    uint32_t size = (bytes[0] << 0) | (bytes[1] << 8) | (bytes[2] << 16) | (bytes[3] << 24);
    // TODO: upper bound on decompression size?

    size_t decompressed_size;
    void *decompressed_data = PyMem_RawMalloc(size);
    if (decompressed_data == NULL)
        return PyErr_NoMemory();
    struct libdeflate_decompressor *decompressor = libdeflate_alloc_decompressor();
    enum libdeflate_result result = libdeflate_gzip_decompress(
        decompressor, data.buf, data.len, decompressed_data, size, &decompressed_size);
    libdeflate_free_decompressor(decompressor);

    PyObject *output = NULL;

    switch (result)
    {
    case LIBDEFLATE_SUCCESS:
        output = PyBytes_FromStringAndSize(decompressed_data, decompressed_size);
        PyMem_RawFree(decompressed_data);
        PyBuffer_Release(&data);
        break;
    default:
        PyMem_RawFree(decompressed_data);
        PyBuffer_Release(&data);
        PyErr_SetString(DeflateError, "Decompression failed.");
    }

    return output;
}

static PyMethodDef deflate_methods[] = {
    {"gzip_compress", (PyCFunction)deflate_gzip_compress, METH_VARARGS | METH_KEYWORDS, "Compress data using gzip."},
    {"gzip_decompress", (PyCFunction)deflate_gzip_decompress, METH_VARARGS, "Decompress gzip data."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef deflate_module = {
    PyModuleDef_HEAD_INIT,
    "deflate",
    "Python wrapper module for libdeflate.",
    -1,
    deflate_methods};

PyMODINIT_FUNC PyInit_deflate(void)
{
    Py_Initialize();

    PyObject *module = PyModule_Create(&deflate_module);
    if (module == NULL)
        return NULL;

    DeflateError = PyErr_NewException("deflate.DeflateError", NULL, NULL);
    Py_INCREF(DeflateError);

    return module;
}
