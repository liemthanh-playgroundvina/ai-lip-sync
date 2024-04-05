FROM python:3.11-slim-bullseye

RUN apt-get update && \
    apt-get install -y git libgl1 ffmpeg libsm6 libxext6 build-essential gcc g++ && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}/

COPY . /app


CMD ["bash"]