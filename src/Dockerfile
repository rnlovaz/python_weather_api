
FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./src .

# This is just metadata of the port server runs by default (can be changed)
EXPOSE 8000

CMD ["python", "run.py"]