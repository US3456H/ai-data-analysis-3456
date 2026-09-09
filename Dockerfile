FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Create workdir
WORKDIR /workspace

# Upgrade pip and install Python packages
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir jupyterlab mlflow[extras] gradio scikit-learn pandas numpy matplotlib seaborn
# AutoGluon can be very large; install only if there's enough resources. Uncomment to enable in your environment.
# RUN pip install --no-cache-dir autogluon

# Create a non-root user
RUN useradd -m jovyan
USER jovyan

EXPOSE 8888 7860

CMD ["bash", "-lc", "jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=''"]
