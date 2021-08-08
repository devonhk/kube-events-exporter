FROM python:3.9-slim-buster

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "src/k8s_asyncio.py"]