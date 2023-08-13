FROM python:3.11.4-slim-bookworm
WORKDIR /app
RUN mkdir -p /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT [ "python" ]
