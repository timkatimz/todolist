FROM python:3.10-slim

WORKDIR /todolist

#ENV PIP_DISABLE_PIP_VERSION=on \
#    PIP_NO_CACHE_DIR=off \
#    PYTHON_PATH=/todolist

RUN groupadd --system service && useradd --system -g service api

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY entrypoint.sh ./entrypoint.sh

USER api

ENTRYPOINT ["bash", "entrypoint.sh"]

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]