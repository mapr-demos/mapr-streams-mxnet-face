FROM docker.artifactory/pacc_nvidia:cuda-9.0-base

RUN apt-get update -y && \
   apt-get install -y vim build-essential libopenblas-dev liblapack-dev \
                       	libopencv-dev cuda-command-line-tools-9-0 \
                       	cuda-cublas-dev-9-0 \
                       	cuda-cudart-dev-9-0 \
                       	cuda-cufft-dev-9-0 \
                       	cuda-curand-dev-9-0 \
                       	cuda-cusolver-dev-9-0 \
                       	cuda-cusparse-dev-9-0 \
                       	python-dev python-setuptools python-numpy python-pip graphviz && \
   pip install opencv-python mxnet-cu90 flask graphviz easydict scipy tensorflow sklearn scikit-image


RUN echo 'LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/"' >> /etc/environment

RUN pip install --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" http://package.mapr.com/releases/MEP/MEP-4.0.0/mac/mapr-streams-python-0.9.2.tar.gz

RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/
RUN ln -s /opt/mapr/lib/libMapRClient.so.1 /opt/mapr/lib/libMapRClient_c.so

