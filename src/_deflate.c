#define PY_SSIZE_T_CLEAN
// If Py_LIMITED_API defined (to 0x030b00f0), will use Stable ABI

#include <Python.h>

#include "libdeflate.h"

#define MODULE_VERSION "0.9.0"

static PyObject *DeflateError;

typedef size_t (*CompressFunc)(struct libdeflate_compressor *, const void *, size_t,
                               void *, size_t);
typedef enum libdeflate_result (*DecompressFunc)(struct libdeflate_decompressor *,
                                                 const void *, size_t, void *, size_t,
                                                 size_t *);
typedef size_t (*BoundFunc)(struct libdeflate_compressor *, size_t);

static PyObject *compress(Py_buffer *data, int compression_level,
                          CompressFunc compressfunc, BoundFunc boundfunc) {
    if (compression_level < 0 || compression_level > 12) {
        PyErr_SetString(PyExc_ValueError, "compresslevel must be between 0 and 12");
        return NULL;
    }

    struct libdeflate_compressor *compressor =
        libdeflate_alloc_compressor(compression_level);
    size_t bound = (*boundfunc)(compressor, data->len);

    PyObject *bytes = PyByteArray_FromStringAndSize(NULL, bound);
    if (bytes == NULL) {
        libdeflate_free_compressor(compressor);
        return PyErr_NoMemory();
    }

    size_t compressed_size = (*compressfunc)(compressor, data->buf, data->len,
                                             PyByteArray_AsString(bytes), bound);
    libdeflate_free_compressor(compressor);

    if (compressed_size == 0) {
        Py_DecRef(bytes);
        PyErr_SetString(DeflateError, "Compression failed");
        return NULL;
    }

    if (compressed_size != bound) {
        PyByteArray_Resize(bytes, compressed_size);
    }

    return bytes;
}

static PyObject *decompress(Py_buffer *data, unsigned int originalsize,
                            DecompressFunc decompressfunc) {
    // Nothing in, nothing out.
    if (originalsize == 0) {
        return PyByteArray_FromStringAndSize(NULL, 0);
    }

    PyObject *output = PyByteArray_FromStringAndSize(NULL, originalsize);
    if (output == NULL) {
        return PyErr_NoMemory();
    }

    size_t decompressed_size;
    struct libdeflate_decompressor *decompressor = libdeflate_alloc_decompressor();
    enum libdeflate_result result = (*decompressfunc)(
        decompressor, data->buf, data->len, PyByteArray_AsString(output), originalsize,
        &decompressed_size);
    libdeflate_free_decompressor(decompressor);

    if (result != LIBDEFLATE_SUCCESS) {
        Py_DecRef(output);
        PyErr_SetString(DeflateError, "Decompression failed");
        return NULL;
    }

    if (decompressed_size != originalsize) {
        PyByteArray_Resize(output, decompressed_size);
    }

    return output;
}

/* GZIP */

static int read_gzip_size(Py_buffer *data, unsigned int *outsize) {
    uint8_t *bytes = (uint8_t *)data->buf;
    if ((data->len < 6) || (bytes[0] != 0x1F || bytes[1] != 0x8B)) {
        return -1;
    }

    // The last 4 bytes of a gzip archive are the original data size, in little endian.
    bytes += (data->len - 4);
    (*outsize) = ((uint32_t)bytes[0] << 0) | ((uint32_t)bytes[1] << 8) |
                 ((uint32_t)bytes[2] << 16) | ((uint32_t)bytes[3] << 24);

    return 0;
}

static PyObject *deflate_gzip_compress(PyObject *self, PyObject *args,
                                       PyObject *kwargs) {
    static char *keywords[] = {"data", "compresslevel", NULL};
    Py_buffer data;
    int compression_level = 6;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*|i", keywords, &data,
                                     &compression_level)) {
        return NULL;
    }

    PyObject *obj = compress(&data, compression_level, libdeflate_gzip_compress,
                             libdeflate_gzip_compress_bound);
    PyBuffer_Release(&data);
    return obj;
}

static PyObject *deflate_gzip_decompress(PyObject *self, PyObject *args,
                                         PyObject *kwargs) {
    static char *keywords[] = {"data", "originalsize", NULL};
    Py_buffer data;
    unsigned int originalsize = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*|I", keywords, &data,
                                     &originalsize)) {
        return NULL;
    }

    if (originalsize == 0) {
        if (read_gzip_size(&data, &originalsize) != 0) {
            PyBuffer_Release(&data);
            PyErr_SetString(PyExc_ValueError, "Invalid gzip data");
            return NULL;
        }
    }

    PyObject *obj = decompress(&data, originalsize, libdeflate_gzip_decompress);
    PyBuffer_Release(&data);
    return obj;
}

/* DEFLATE */

static PyObject *deflate_deflate_compress(PyObject *self, PyObject *args,
                                          PyObject *kwargs) {
    static char *keywords[] = {"data", "compresslevel", NULL};
    Py_buffer data;
    int compression_level = 6;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*|i", keywords, &data,
                                     &compression_level)) {
        return NULL;
    }

    PyObject *obj = compress(&data, compression_level, libdeflate_deflate_compress,
                             libdeflate_deflate_compress_bound);
    PyBuffer_Release(&data);
    return obj;
}

static PyObject *deflate_deflate_decompress(PyObject *self, PyObject *args,
                                            PyObject *kwargs) {
    static char *keywords[] = {"data", "originalsize", NULL};
    Py_buffer data;
    unsigned int originalsize = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*I", keywords, &data,
                                     &originalsize)) {
        return NULL;
    }

    PyObject *obj = decompress(&data, originalsize, libdeflate_deflate_decompress);
    PyBuffer_Release(&data);
    return obj;
}

/* ZLIB */

static PyObject *deflate_zlib_compress(PyObject *self, PyObject *args,
                                       PyObject *kwargs) {
    static char *keywords[] = {"data", "compresslevel", NULL};
    Py_buffer data;
    int compression_level = 6;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*|i", keywords, &data,
                                     &compression_level)) {
        return NULL;
    }

    PyObject *obj = compress(&data, compression_level, libdeflate_zlib_compress,
                             libdeflate_zlib_compress_bound);
    PyBuffer_Release(&data);
    return obj;
}

static PyObject *deflate_zlib_decompress(PyObject *self, PyObject *args,
                                         PyObject *kwargs) {
    static char *keywords[] = {"data", "originalsize", NULL};
    Py_buffer data;
    unsigned int originalsize = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*I", keywords, &data,
                                     &originalsize)) {
        return NULL;
    }

    PyObject *obj = decompress(&data, originalsize, libdeflate_zlib_decompress);
    PyBuffer_Release(&data);
    return obj;
}

/* CRC-32/Adler-32 */

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

static PyObject *deflate_adler32(PyObject *self, PyObject *args) {
    Py_buffer data;
    unsigned int adler = 1;

    if (!PyArg_ParseTuple(args, "y*|I", &data, &adler)) {
        return NULL;
    }

    adler = libdeflate_adler32(adler, data.buf, data.len);
    PyBuffer_Release(&data);

    return Py_BuildValue("I", adler);
}

static PyMethodDef deflate_methods[] = {
    {"gzip_compress", (PyCFunction)deflate_gzip_compress, METH_VARARGS | METH_KEYWORDS,
     "Compress data using gzip."},
    {"gzip_decompress", (PyCFunction)deflate_gzip_decompress,
     METH_VARARGS | METH_KEYWORDS, "Decompress gzip data."},
    {"deflate_compress", (PyCFunction)deflate_deflate_compress,
     METH_VARARGS | METH_KEYWORDS, "Compress data using raw DEFLATE."},
    {"deflate_decompress", (PyCFunction)deflate_deflate_decompress,
     METH_VARARGS | METH_KEYWORDS, "Decompress raw DEFLATE data."},
    {"zlib_compress", (PyCFunction)deflate_zlib_compress, METH_VARARGS | METH_KEYWORDS,
     "Compress data using zlib."},
    {"zlib_decompress", (PyCFunction)deflate_zlib_decompress,
     METH_VARARGS | METH_KEYWORDS, "Decompress zlib data."},
    {"crc32", (PyCFunction)deflate_crc32, METH_VARARGS,
     "CRC32 algorithm from libdeflate"},
    {"adler32", (PyCFunction)deflate_adler32, METH_VARARGS,
     "adler32 algorithm from libdeflate"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef deflate_module = {PyModuleDef_HEAD_INIT, "_deflate",
                                            "Python wrapper module for libdeflate.", -1,
                                            deflate_methods};

PyMODINIT_FUNC PyInit__deflate(void) {
    PyObject *module = PyModule_Create(&deflate_module);
    if (module == NULL)
        return NULL;

    PyModule_AddStringConstant(module, "__version__", MODULE_VERSION);

    DeflateError = PyErr_NewException("deflate.DeflateError", NULL, NULL);
    Py_IncRef(DeflateError);
    PyModule_AddObject(module, "DeflateError", DeflateError);

    return module;
}
