# C shared library from Python to Fortran using CFFI

Instructions to reproduce the process:

1. Install python environment doing:
```shell
conda env create -f environment.yml
conda activate ml_ros
```

2. Create shared library:
```shell
python builder.py
```

3. Test shared library with a fortran example:
```shell
make
./ros_ml_predict
```
