FC=gfortran
FFLAGS=-L./ -lrosml
SRC=ros_ml_predict.f90
OBJ=${SRC:.f90=.o}

%.o: %.f90
	$(FC) $(FFLAGS) -o $@ -c $<

ros_ml_predict: $(OBJ)
	$(FC) $(FFLAGS) -o $@ $(OBJ)

clean:
	@rm -f *.o *.mod ros_ml_predict
