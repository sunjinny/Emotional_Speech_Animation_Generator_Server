ARG UBUNTU_VERSION=16.04
FROM ubuntu:${UBUNTU_VERSION}

RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	wget \
	tar \
	libgomp1 \
        python-setuptools \
        libgtk2.0-dev \
        python3-dev \
        python3-numpy \
        python3-pip \
		libsndfile1 \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# For Korean input
ENV LC_ALL=C.UTF-8

WORKDIR /app
COPY ./app /app

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install setuptools && \
    python3 -m pip install librosa && \
    python3 -m pip install flask

EXPOSE 5000

CMD export FLASK_APP=/app/main.py && flask run --host=0.0.0.0