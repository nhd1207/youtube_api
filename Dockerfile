FROM python:3.8 
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --upgrade -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
EXPOSE 5000
CMD ["flask", "run", "-h", "0.0.0.0"]