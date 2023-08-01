FROM python:3.11
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 1111
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1111"]