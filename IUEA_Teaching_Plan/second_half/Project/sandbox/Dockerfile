# Grading sandbox that matches Google Colab (versions in colab_versions.json, read from googlecolab/backend-info).
# Build:  docker build -t iuea-notebooks:colab-2026.11 IUEA_Teaching_Plan/second_half/Project/sandbox
# The grader still runs it with --network=none, --read-only, no capabilities, 1 CPU, 1 GB and 64 processes (grader/isolated_grading.py).
ARG PYTHON=3.13.18
FROM python:${PYTHON}-slim
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --only-binary=:all: -r /tmp/requirements.txt && rm /tmp/requirements.txt
# Colab keeps notebooks and files in /content; here it is the same folder as the grader's working folder.
RUN ln -s /work /content
# Colab shows each figure under its cell and then closes it; the grader does the same after every cell (own_cells.py).
ENV MPLBACKEND=Agg MPLCONFIGDIR=/tmp/matplotlib OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
LABEL org.iuea.colab-python="3.13.18" org.iuea.source="googlecolab/backend-info, 13 November 2026"
USER 65534:65534
WORKDIR /work
