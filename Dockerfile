FROM python:3.8-slim

COPY . .

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/Essato_internship/app

EXPOSE 5000

ENV NAME World

CMD [ "python", "-m", "flask", "run" ]
