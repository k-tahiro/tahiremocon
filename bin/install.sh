#!/bin/bash

sudo apt update
sudo apt install -y build-essential \
                    libopenblas-dev \
                    libblas-dev \
                    libatlas-base-dev \
                    m4 \
                    cmake \
                    cython \
                    python3-dev \
                    python3-yaml \
                    python3-setuptools \
                    python3-wheel \
                    python3-pillow \
                    zlib1g-dev \
                    libjpeg-dev
mkdir -p $(cd $(dirname $0) && pwd)/../{data,log}
