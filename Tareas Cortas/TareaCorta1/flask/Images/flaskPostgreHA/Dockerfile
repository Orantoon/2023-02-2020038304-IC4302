FROM python:3.10.7-slim-bullseye

WORKDIR /app

COPY app/. .
RUN pip install --no-cache-dir -r requirement.txt

CMD [ "python", "-u", "./app.py" ]
