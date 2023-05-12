from .connector import StoreConnector
from pandas import DataFrame, Series
from datetime import datetime

"""
    В данном модуле реализуется API (Application Programming Interface)
    для взаимодействия с БД с помощью объектов-коннекторов.
    
    ВАЖНО! Методы должны быть названы таким образом, чтобы по названию
    можно было понять выполняемые действия.
"""
# Вывод списка обработанных файлов с сортировкой по дате
def select_all_from_source_files(connector: StoreConnector):
    connector.start_transaction()  # начинаем выполнение запросов
    query = f'SELECT * FROM source_files ORDER BY processed'
    result = connector.execute(query).fetchall()
    connector.end_transaction()  # завершаем выполнение запросов
    return result

# Вставка в таблицу обработанных файлов
def insert_into_source_files(connector: StoreConnector, filename: str):
    now = datetime.now() # текущая дата и время
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")   # преобразуем в формат SQL
    connector.start_transaction()
    query = f'INSERT INTO source_files (filename, processed) VALUES (\'{filename}\', \'{date_time}\')'
    result = connector.execute(query)
    connector.end_transaction()
    return result

# Вставка строк из DataFrame в БД
def insert_rows_into_processed_data(connector: StoreConnector, dataframe: DataFrame, filename: str):
    rows = dataframe.to_dict('records')
    connector.start_transaction()
    for row in rows:
        connector.execute(f'INSERT INTO processed_data (LKG, target, source_file) VALUES (\'{row["avgRating"]}\', \'{row["item_id"]}\', 2)')
    connector.end_transaction()