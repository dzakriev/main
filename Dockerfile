FROM apache/airflow:2.10.5

USER root

RUN apt-get update && \
    apt install -y default-jdk wget && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements_airflow.txt /requirements.txt
RUN chmod 777 /requirements.txt

USER airflow
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt