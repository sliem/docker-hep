FROM ubuntu:latest
RUN apt-get update

# Required packages
RUN apt-get install --yes git dpkg-dev cmake g++ gcc binutils libx11-dev libxpm-dev \
                              libxft-dev libxext-dev

# Optional packages
RUN apt-get install --yes gfortran libssl-dev libpcre3-dev \
                          xlibmesa-glu-dev libglew1.5-dev libftgl-dev \
                          libmysqlclient-dev libfftw3-dev libcfitsio-dev \
                          graphviz-dev libavahi-compat-libdnssd-dev \
                          libldap2-dev python-dev libxml2-dev libkrb5-dev \
                          libgsl0-dev libqt4-dev python-numpy-dev

ENV ROOTSYS /usr/local
ENV rootversion v6-08-00

WORKDIR /
RUN git clone --quiet http://root.cern.ch/git/root.git /src/root

WORKDIR /src/root
RUN git checkout ${rootversion}

WORKDIR /build
RUN cmake ../src/root -DCMAKE_INSTALL_PREFIX=${ROOTSYS}
RUN cmake --build .
RUN cmake --build . --target install
RUN ldconfig

WORKDIR /
RUN rm -rf /src /build
