FROM python:3.10-alpine

RUN apk add --no-cache build-base

RUN pip install --upgrade setuptools pip

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./boot.sh .
ENTRYPOINT /bin/sh ./boot.sh
CMD [ "/bin/sh" ]

RUN apk add --no-cache netcat-openbsd

WORKDIR /App
COPY . .
