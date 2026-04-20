FROM python:3.14-slim
LABEL authors="Collin Geersen"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app

ENV FLASK_APP=app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]