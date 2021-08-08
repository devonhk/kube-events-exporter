FROM python:3.9-slim-buster

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "src/k8s_asyncio.py"]