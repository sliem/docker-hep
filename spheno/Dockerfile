FROM alpine:3.4
MAINTAINER Sebastian Liem <sebastian@liem.se>

RUN apk add --update --no-cache gfortran g++ python-dev musl-dev make libstdc++

WORKDIR /spheno
COPY ./SPheno_3.3.8 .
RUN make

COPY interface.py .

RUN apk del make gfortran g++ musl-dev

ENTRYPOINT ["python", "interface.py"]
