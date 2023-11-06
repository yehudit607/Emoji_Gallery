FROM python:3.11
WORKDIR /app

ENV PYTHONPATH /app/

# Install requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install alembic

# Copy code
COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]
