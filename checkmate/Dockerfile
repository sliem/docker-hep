FROM sliem/docker-hep:root6
MAINTAINER Sebastian Liem <sebastian@liem.se>

RUN apt-get --yes install tcl python-scipy

ENV DELPHES_VER 3.4.0
ENV PYTHIA_VER 8219
ENV MG5_VER 2.5.2
ENV CHECKMATE_VER 2.0.0

WORKDIR /
RUN wget http://cp3.irmp.ucl.ac.be/downloads/Delphes-${DELPHES_VER}.tar.gz
RUN mkdir /delphes && tar -xzf Delphes-${DELPHES_VER}.tar.gz -C /delphes --strip-components 1

WORKDIR /delphes
RUN source /root/bin/thisroot.sh
RUN ./configure
RUN make

WORKDIR /
RUN wget http://home.thep.lu.se/~torbjorn/pythia8/pythia${PYTHIA_VER}.tgz
RUN tar -xzf pythia${PYTHIA_VER}.tgz

WORKDIR pythia${PYTHIA_VER}
RUN mkdir /pythia
RUN ./configure --prefix=/pythia
RUN make
RUN make install
RUN rm -r /pythia${PYTHIA_VER}

WORKDIR /
RUN wget --no-check-certificate https://launchpad.net/mg5amcnlo/2.0/2.5.x/+download/MG5_aMC_v${MG5_VER}.tar.gz
RUN mkdir /madgraph && tar -xzf MG5_aMC_v${MG5_VER}.tar.gz -C /madgraph --strip-components 1

WORKDIR /
RUN wget --no-check-certificate http://www.hepforge.org/archive/checkmate/CheckMATE-${CHECKMATE_VER}.tar.gz
RUN mkdir /checkmate && tar -xzf CheckMATE-${CHECKMATE_VER}.tar.gz -C /checkmate --strip-components 1

WORKDIR /checkmate
RUN ./configure --with-python=/usr/bin/python \
                --with-pythia=/pythia \
                --with-delphes=/delphes \
                --with-rootsys=/root \
                --with-madgraph=/madgraph
RUN make

WORKDIR /
RUN rm *.tar.gz *.tgz

