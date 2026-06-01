FROM python:3.12-slim-bookworm

WORKDIR /data

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["sh", "-c", "cp -f image1.jpeg logo.png && cp -f image2.jpeg symbol.png && python image1.py && python image2.py"]
