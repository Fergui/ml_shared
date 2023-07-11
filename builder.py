import cffi
ffibuilder = cffi.FFI()

header = """
extern double ros_ml_predict(double *);
"""

module = """
from ros_ml import ffi
import pickle
import numpy as np

# Create the dictionary mapping ctypes to np dtypes.
ctype2dtype = {}

# Integer types
for prefix in ('int', 'uint'):
    for log_bytes in range(4):
        ctype = '%s%d_t' % (prefix, 8 * (2**log_bytes))
        dtype = '%s%d' % (prefix[0], 2**log_bytes)
        # print( ctype )
        # print( dtype )
        ctype2dtype[ctype] = np.dtype(dtype)

# Floating point types
ctype2dtype['float'] = np.dtype('f4')
ctype2dtype['double'] = np.dtype('f8')

def asarray(ffi, ptr, shape, **kwargs):
    length = np.prod(shape)
    # Get the canonical C type of the elements of ptr as a string.
    T = ffi.getctype(ffi.typeof(ptr).item)
    if T not in ctype2dtype:
        raise RuntimeError("Cannot create an array for element type: %s" % T)
    a = np.frombuffer(ffi.buffer(ptr, length * ffi.sizeof(T)),dtype=ctype2dtype[T])
    a = np.frombuffer(ffi.buffer(ptr, length * ffi.sizeof(T)), ctype2dtype[T]).reshape(shape, **kwargs)
    return a

with open('/glade/u/home/angelfc/scratch/ml_ros_project/ros_rf_model/ml_model.pkl','rb') as f:
    rf = pickle.load(f)
n = rf.n_features_in_ 

@ffi.def_extern()
def ros_ml_predict(x):
    x_ = asarray(ffi, x, shape=(n,))
    y = rf.predict([x_])[0]
    return y 
"""

with open("rosml.h", "w") as f:
    f.write(header)

ffibuilder.embedding_api(header)
ffibuilder.set_source("ros_ml", r'''
    #include "rosml.h"
''')

ffibuilder.embedding_init_code(module)
ffibuilder.compile(target="librosml.so", verbose=True)
