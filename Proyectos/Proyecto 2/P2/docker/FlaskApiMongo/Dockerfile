FROM python:3.10.7-slim-bullseye

WORKDIR /app

COPY app/. .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -u tests.py

RUN python -u testsm.py

CMD [ "flask",  "--app", "app", "run" ]