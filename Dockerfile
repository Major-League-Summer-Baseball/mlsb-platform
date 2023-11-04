FROM python:3-alpine

WORKDIR ./mlsb-platform
LABEL maintainer "Dallas Fraser <dallas.fraser.waterloo@gmail.com>"

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV FLASK_APP=api/app

CMD ["python", "-m", "flask", "--app", "api/app", "run", "--host=0.0.0.0"]
