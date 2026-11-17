FROM python:3.11.11-slim
RUN pip install --no-cache-dir numpy==2.2.6 pandas==2.3.3 matplotlib==3.10.9 scikit-learn==1.7.2
# Colab uses /content; keep it an alias of the same isolated working directory.
RUN ln -s /work /content
ENV MPLBACKEND=Agg MPLCONFIGDIR=/tmp/matplotlib OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
USER 65534:65534
WORKDIR /work
