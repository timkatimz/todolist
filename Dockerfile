FROM python:3.10-slim

WORKDIR /src

RUN pip install --upgrade pip
RUN pip install Django django-environ psycopg2-binary gunicorn

COPY . .
COPY entrypoint.sh ./entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

