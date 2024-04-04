
FROM python:3.9

COPY app .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN cd ./app

EXPOSE 5000

CMD [ "python", "-m", "flask", "run" ]

