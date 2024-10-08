# read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM python:3.9

WORKDIR /code

# COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Set TRANSFORMERS_CACHE environment variable
ENV TRANSFORMERS_CACHE=.cache

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
