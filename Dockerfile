FROM python:3.10-slim-buster

WORKDIR /ice-pack-allocation

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

RUN mkdir -p src/output/

CMD [ "python", "./main.py" ]
