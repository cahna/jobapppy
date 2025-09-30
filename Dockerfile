FROM python:3.12-slim
ARG JOBAPPPY_VERSION

RUN pip install jobapppy$JOBAPPPY_VERSION

ENTRYPOINT [ "python", "-m", "jobapppy" ]
