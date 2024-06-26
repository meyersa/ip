FROM python:3-slim
WORKDIR /app

# Install deps and clean
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

# Actual app
COPY . /app/

# Run Server
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]