FROM python:3.12-slim

COPY ./ /qMODES/

WORKDIR /qMODES/

# installing vim
RUN apt-get update && apt-get install -y vim

# installing python packages
RUN pip install xarray
RUN pip install dask
RUN pip install cdsapi
RUN pip install datetime
RUN pip install h5netcdf
RUN pip install h5py
RUN pip install matplotlib
RUN pip install netCDF4
RUN pip install scipy

# Setting the PythonPath environment variables
ENV PYTHONPATH="/qMODES/src"

# Setting qMODES environment variables
ENV QMODES_BASE_DIR="/"

ENV QMODES_ERA_DIR="$QMODES_BASE_DIR/input_data/ERA_data"
ENV QMODES_MODES_DIR="$QMODES_BASE_DIR/input_data/MODES_data"

ENV QMODES_COEF_DIR="$QMODES_MODES_DIR/coef"
ENV QMODES_HOUGH_DIR="$QMODES_MODES_DIR/hough"
ENV QMODES_FREQ_DIR="$QMODES_MODES_DIR/hough"
ENV QMODES_VSF_DIR="$QMODES_MODES_DIR/vsf"
ENV QMODES_VSFINT_DIR="$QMODES_MODES_DIR/vsf"
ENV QMODES_QKDATA_DIR="$QMODES_BASE_DIR/output_data/qk_data"
ENV QMODES_QMODESDATA_DIR="$QMODES_BASE_DIR/output_data/qmodes_data"
ENV QMODES_PLOTS_DIR="$QMODES_BASE_DIR/output_data/plots"

CMD ["bash"]
