FROM python:3.7

RUN mkdir /app
COPY src/requirements.txt /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

USER nobody

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
