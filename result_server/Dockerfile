FROM python:3.11-rc-slim-bullseye
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
EXPOSE 5001
CMD ["python", "app.py"]

