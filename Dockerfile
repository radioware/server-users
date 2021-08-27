FROM python:3.9-slim
COPY app /app
COPY requirements.txt /
RUN python3 -m venv /venv \
    && /venv/bin/pip3 install --no-cache-dir --upgrade pip setuptools \
    && /venv/bin/pip3 install --no-cache-dir --requirement /requirements.txt
EXPOSE 8000
USER 1000:1000
WORKDIR /app
ENTRYPOINT ["/venv/bin/python3"]
CMD ["run.py"]
