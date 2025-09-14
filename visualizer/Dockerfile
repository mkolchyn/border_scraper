FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /visualizer

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scripts
COPY visualizer.py visualizer_stats.py visualizer_functions.py visualizer_archive.py main.py ./

CMD ["python", "main.py"]
