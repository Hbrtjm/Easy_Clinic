
FROM python:3.9

ADD app .

RUN pip install -r requirements.txt

RUN cd ./app

CMD [ "python", "-m", "flask", "run" ]

