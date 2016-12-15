FROM blitznote/debootstrap-amd64:16.04
MAINTAINER Sebastian Liem <sebastian@liem.se>

RUN apt-get update

RUN apt-get install --yes git dpkg-dev cmake g++ gcc binutils libx11-dev libxpm-dev \
                          libxft-dev libxext-dev \
                          gfortran libssl-dev libpcre3-dev \
                          xlibmesa-glu-dev libglew1.5-dev libftgl-dev \
                          libmysqlclient-dev libfftw3-dev libcfitsio-dev \
                          graphviz-dev libavahi-compat-libdnssd-dev \
                          libldap2-dev python-dev libxml2-dev libkrb5-dev \
                          libgsl0-dev libqt4-dev python-numpy-dev \
                          wget


ENV ROOTSYS /root
ENV PATH "${PATH}:/root/bin"
ENV tarball root_v6.08.02.Linux-ubuntu16-x86_64-gcc5.4.tar.gz

WORKDIR /
RUN wget --no-check-certificate https://root.cern.ch/download/${tarball}
RUN tar -xzf ${tarball}
RUN rm ${tarball}

RUN apt-get --yes clean
