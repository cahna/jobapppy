FROM python:3.11-slim
ARG JOBAPPPY_VERSION

RUN pip install jobapppy$JOBAPPPY_VERSION

ENTRYPOINT [ "python", "-m", "jobapppy" ]
