FROM python:3.10-slim

WORKDIR /src

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
COPY entrypoint.sh ./entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

