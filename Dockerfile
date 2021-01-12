FROM centos/python-38-centos7
USER root
RUN yum install musl-dev linux-headers g++ gcc git curl
RUN yum clean all
WORKDIR /code
COPY . /code
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN yes "" | bash setup.sh
ENTRYPOINT ["python", "phen2gene.py"]
CMD ["-h"]
