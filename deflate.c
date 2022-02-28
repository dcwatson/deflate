#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "libdeflate/libdeflate.h"

#define MODULE_VERSION "0.4.0"

static PyObject *DeflateError;

static PyObject *deflate_gzip_compress(PyObject *self, PyObject *args,
                                       PyObject *kwargs) {
    static char *keywords[] = {"data", "compresslevel", NULL};
    Py_buffer data;
    int compression_level = 6;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*|i", keywords, &data,
                                     &compression_level)) {
        return NULL;
    }

    if (compression_level < 1 || compression_level > 12) {
        PyBuffer_Release(&data);
        PyErr_SetString(PyExc_ValueError, "compresslevel must be between 1 and 12.");
        return NULL;
    }

    struct libdeflate_compressor *compressor =
        libdeflate_alloc_compressor(compression_level);
    size_t bound = libdeflate_gzip_compress_bound(compressor, data.len);

    PyObject *bytes = PyBytes_FromStringAndSize(NULL, bound);
    if (bytes == NULL) {
        libdeflate_free_compressor(compressor);
        PyBuffer_Release(&data);
        return PyErr_NoMemory();
    }

    size_t compressed_size = libdeflate_gzip_compress(compressor, data.buf, data.len,
                                                      PyBytes_AsString(bytes), bound);
    libdeflate_free_compressor(compressor);
    PyBuffer_Release(&data);

    if (compressed_size == 0) {
        Py_DECREF(bytes);
        PyErr_SetString(DeflateError, "Compression failed.");
        return NULL;
    }

    _PyBytes_Resize(&bytes, compressed_size);

    return bytes;
}

static PyObject *deflate_gzip_decompress(PyObject *self, PyObject *args) {
    Py_buffer data;

    if (!PyArg_ParseTuple(args, "y*", &data)) {
        return NULL;
    }

    if (data.len < 6) {
        PyErr_SetString(DeflateError, "Invalid gzip data.");
        PyBuffer_Release(&data);
        return NULL;
    }

    // Very basic gzip header check before we go allocating memory.
    uint8_t *bytes = (uint8_t *)data.buf;
    if (bytes[0] != 0x1F || bytes[1] != 0x8B) {
        PyErr_SetString(DeflateError, "Invalid gzip data.");
        PyBuffer_Release(&data);
        return NULL;
    }

    // The last 4 bytes of a gzip archive are the original data size, in little
    // endian.
    bytes = (uint8_t *)data.buf + (data.len - 4);
    uint32_t size =
        (bytes[0] << 0) | (bytes[1] << 8) | (bytes[2] << 16) | (bytes[3] << 24);
    // TODO: upper bound on decompression size?

    PyObject *output = PyBytes_FromStringAndSize(NULL, size);
    if (output == NULL) {
        PyBuffer_Release(&data);
        return PyErr_NoMemory();
    }

    size_t decompressed_size;
    struct libdeflate_decompressor *decompressor = libdeflate_alloc_decompressor();
    enum libdeflate_result result =
        libdeflate_gzip_decompress(decompressor, data.buf, data.len,
                                   PyBytes_AsString(output), size, &decompressed_size);
    libdeflate_free_decompressor(decompressor);

    // Resize the bytes object to the decompressed size and release the input buffer.
    _PyBytes_Resize(&output, decompressed_size);
    PyBuffer_Release(&data);

    if (result != LIBDEFLATE_SUCCESS) {
        Py_DECREF(output);
        PyErr_SetString(DeflateError, "Decompression failed.");
        return NULL;
    }

    return output;
}

static PyObject *deflate_crc32(PyObject *self, PyObject *args) {
    Py_buffer data;
    unsigned int crc = 0;

    if (!PyArg_ParseTuple(args, "y*|I", &data, &crc)) {
        return NULL;
    }

    crc = libdeflate_crc32(crc, data.buf, data.len);
    PyBuffer_Release(&data);

    return Py_BuildValue("I", crc);
}

static PyMethodDef deflate_methods[] = {
    {"gzip_compress", (PyCFunction)deflate_gzip_compress, METH_VARARGS | METH_KEYWORDS,
     "Compress data using gzip."},
    {"gzip_decompress", (PyCFunction)deflate_gzip_decompress, METH_VARARGS,
     "Decompress gzip data."},
    {"crc32", (PyCFunction)deflate_crc32, METH_VARARGS,
     "CRC32 algorithm from libdeflate"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef deflate_module = {PyModuleDef_HEAD_INIT, "deflate",
                                            "Python wrapper module for libdeflate.", -1,
                                            deflate_methods};

PyMODINIT_FUNC PyInit_deflate(void) {
    Py_Initialize();

    PyObject *module = PyModule_Create(&deflate_module);
    if (module == NULL)
        return NULL;

    PyModule_AddStringConstant(module, "__version__", MODULE_VERSION);

    DeflateError = PyErr_NewException("deflate.DeflateError", NULL, NULL);
    Py_INCREF(DeflateError);
    PyModule_AddObject(module, "DeflateError", DeflateError);

    return module;
}
