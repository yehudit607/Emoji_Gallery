FROM python:3.9.10-slim
WORKDIR /app

ENV PYTHONPATH /app/

# Install requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY ./ /app/

ENTRYPOINT ["/app/entrypoint.sh"]
