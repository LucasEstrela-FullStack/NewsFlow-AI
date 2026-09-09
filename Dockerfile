FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

RUN addgroup --system newflow && adduser --system --ingroup newflow newflow

COPY --chown=newflow:newflow app ./app
COPY --chown=newflow:newflow config.py run.py ./

USER newflow

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:application"]
