FROM python:3.9.10-alpine3.14
WORKDIR /srv

# Move relevant files to container
COPY requirements.txt requirements.txt
COPY greenworld greenworld
COPY .env .env

# Set up Python environment
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run web server
ENV PYTHONPATH=/srv
CMD ["python","greenworld/server/app.py"]