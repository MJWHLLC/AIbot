FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=paralegal_agent.app
EXPOSE 5000
CMD ["python", "-m", "paralegal_agent.app"]
