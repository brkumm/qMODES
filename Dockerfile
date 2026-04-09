FROM python:3.12-trixie

COPY ./ /qMODES/

WORKDIR /qMODES/

# Installing Python packages
RUN pip install -r qMODES_requirements.txt

# Installing vim
RUN apt-get update && apt-get install -y vim

# Setting the PythonPath environment variables
ENV PYTHONPATH="/qMODES/src"

# Setting qMODES environment variables
ENV QMODES_BASE_DIR=""

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
