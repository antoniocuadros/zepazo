FROM python:3.8-slim

LABEL version="1.0.0" maintainer="antculap@gmail.com"

RUN apt-get update -y

#Install opencv dependencies
RUN apt install --no-install-recommends build-essential -y
RUN apt install libgl1-mesa-glx -y && \
    apt install libglib2.0-0 -y && \
    apt install libgtk2.0-dev -y && \
    apt install libqt5x11extras5 -y

#Needed to avoid errors in opencv
ENV LANG=C.UTF-8

#Upgrade PIP, if not, can cause problems installing opencv-python
RUN pip install --upgrade pip

#Install poetry to install dependencies
RUN pip install poetry

#Copy dependency files
COPY poetry.lock pyproject.toml /home/test_user/

#We are in a container, it is isolated, virtualenv is not needed
RUN poetry config virtualenvs.create false

WORKDIR /home/test_user/

#Install dependencies
RUN poetry install

COPY . .

#Dependency files no longer needed
RUN rm -r /home/test_user/poetry.lock


CMD ["poetry", "run", "task", "test"]

