FROM python:3.10.0-slim

WORKDIR /hit_record

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "run.py"]