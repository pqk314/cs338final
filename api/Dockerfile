FROM python:3.9.12

WORKDIR /web

COPY . .

RUN pip install --upgrade pip
RUN pip install flask
RUN pip install requests
RUN pip install psycopg2



EXPOSE 5000

CMD ["python", "backend.py", "db.py"]