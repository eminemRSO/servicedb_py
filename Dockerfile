FROM python:3.8-slim-buster
RUN apt-get update \
    && apt-get install build-essential -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./project/app .

EXPOSE 8082

CMD ["uvicorn", "main:app", "--port", "8082", "--host", "0.0.0.0"]
