FROM python:3.12-slim

#  Set working directory for better layer caching
WORKDIR /workspace

#  Copy only requirements to cache dependencies layer
COPY requirements.txt .

#  Create venv, install dependencies, register kernel, 
# configure bashrc, and clean up in one layer
RUN set -eux; \
    python -m venv /opt/venv; \
    # ensure the virtualenv is activated in interactive shells
    echo 'source /opt/venv/bin/activate' >> /root/.bashrc; \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip; \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt; \
    rm requirements.txt; \
    # register this environment as a Jupyter kernel
    /opt/venv/bin/python -m ipykernel install --sys-prefix --name venv --display-name "Python3.12 (venv)"

#  Prepend venv to PATH and ensure bash sources bashrc in non-interactive mode
ENV PATH="/opt/venv/bin:$PATH" \
    BASH_ENV="/root/.bashrc"

#  Expose Jupyter Notebook port
EXPOSE 8888

#  Launch bash (venv will be active via bashrc)
CMD ["bash"]