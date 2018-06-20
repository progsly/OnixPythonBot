FROM python:3.5

RUN apt-get update && \
        apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000
ENV FLASK_DEBUG=True

CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:application", "--reload"]