FROM apache/airflow:3.0.3

# Update OS and install git
USER root
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Install Python dependencies
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt

# Set DBT_PROFILES_DIR to your local .dbt path inside the container
ENV DBT_PROFILES_DIR=/opt/airflow/config/.dbt
