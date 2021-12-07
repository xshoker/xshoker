FROM python:3.9-buster

RUN pip install FASTAPI

RUN pip install uvicorn

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
