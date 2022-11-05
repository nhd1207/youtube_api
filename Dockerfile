FROM python:3.8-alpine 
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --upgrade -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
EXPOSE 5000
CMD ["flask", "run", "-h", "0.0.0.0"]