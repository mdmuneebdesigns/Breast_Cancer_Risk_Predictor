FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the Hugging Face default port
EXPOSE 7860

# Run the start script
CMD ["bash", "start.sh"]
