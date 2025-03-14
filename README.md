Запуск:
1 `docker build -t airflow-with-dependencies .`
2 `docker-compose up --build`


Для репликации запустить dag "data_replication_dag"

Для инициализации витрин запустить dag "create_datamarket_dag", перед этим настроить соединение:
Connection id: postgresql
Host: postgres_target
Database: orders
Login: airflow
Password: airflow


Всего 3 витрины со следующими схемами: