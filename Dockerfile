FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=main.py
EXPOSE 5000
CMD ["flask", "run", "-h", "0.0.0.0"]
