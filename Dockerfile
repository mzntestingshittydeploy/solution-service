FROM python:3.9

RUN useradd -m python
USER python

WORKDIR /home/python

COPY requirements.txt .
ENV PATH="${PATH}:/home/python/.local/bin"
RUN pip install --user -r requirements.txt

COPY src src

CMD uvicorn --host 0.0.0.0 --port 8080 src.main:app
