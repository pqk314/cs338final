FROM python:3.11-alpine

WORKDIR /web

COPY . .

RUN pip install flask
RUN pip install requests

EXPOSE 5000

CMD ["python", "backend.py"]