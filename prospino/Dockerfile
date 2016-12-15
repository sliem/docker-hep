FROM alpine:3.4
MAINTAINER Sebastian Liem <sebastian@liem.se>

RUN apk add --update --no-cache gfortran g++ python-dev musl-dev make libstdc++

WORKDIR /prospino
COPY ./on_the_web_10_17_14 .
RUN make

COPY interface.py .

RUN apk del make gfortran g++ musl-dev

ENTRYPOINT ["python", "interface.py"]
