from airflow import DAG
from airflow.operators import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/mnt/c/Users/adity/Downloads/Interview/Alt_DE/psacard')
from loadall_auction_items import main as loadall_auction_items
from populate_transaction_amount import main as populate_transaction_amount
from populate_certificates import main as populate_certificates

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 9, 2),
    'email': ['akroy@umass.edu'],
    'email_on_failure': True,
    'email_on_success': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'end_date': datetime(2020, 9, 10),
    'priority_weight': 1
}

ingestion_dag = DAG('alt_ingestion_pipeline', default_args=default_args)

load_auction_items = PythonOperator(task_id='refresh_auction_listing', python_callable=loadall_auction_items, dag=ingestion_dag)
populate_transaction_amount = PythonOperator(task_id='populate_transaction_tables', python_callable=populate_transaction_amount, dag=ingestion_dag)
populate_certificates = PythonOperator(task_id='fetch_certificate_update', python_callable=populate_certificates, dag=ingestion_dag)

# Setting up the necessary dependencies
load_auction_items >> populate_transaction_amount >> populate_certificates 
