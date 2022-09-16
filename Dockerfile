FROM google/cloud-sdk
MAINTAINER Wildan<wildan.putra@devoteam.com>

# RUN apt-get install python-setuptools -y
# RUN apt-get install python-pip -y

# Update apt packages
RUN apt update
RUN apt upgrade -y

# Install python 3.7
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.7 -y

# Make python 3.7 the default
RUN echo "alias python=python3.7" >> ~/.bashrc
RUN export PATH=${PATH}:/usr/bin/python3.7
RUN /bin/bash -c "source ~/.bashrc"

#Copy Files
COPY docs/* /main/docs/
COPY Dockerfile /main/
COPY requirements.txt /main/
COPY app.py /main/

# Install pip
RUN apt install python3-pip -y
RUN python3 -m pip install --upgrade pip

RUN pip install --upgrade oauth2client 
RUN pip install --upgrade google-api-python-client
RUN pip install -r /main/requirements.txt

WORKDIR main

ENTRYPOINT ["python3", "/main/app.py"]