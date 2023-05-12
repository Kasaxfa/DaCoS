from abc import ABC, abstractmethod     # подключаем инструменты для создания абстрактных классов
import pandas   # библиотека для работы с датасетами
from typing import List

"""
    В данном модуле реализуются классы обработчиков для 
    применения алгоритма обработки к различным типам файлов (csv или txt).
    
    ВАЖНО! Если реализация различных обработчиков занимает большое 
    количество строк, то необходимо оформлять каждый класс в отдельном файле
"""

# Родительский класс для обработчиков файлов
class DataProcessor(ABC):
    def __init__(self, datasource):
        # общие атрибуты для классов обработчиков данных
        self._datasource = datasource   # путь к источнику данных
        self._dataset = None            # входной набор данных
        self.result = None              # выходной набор данных (результат обработки)

    # Метод, инициализирующий источник данных
    # Все методы, помеченные декоратором @abstractmethod, ОБЯЗАТЕЛЬНЫ для переобределения
    @abstractmethod
    def read(self) -> bool:
        pass

    # Точка запуска методов обработки данных
    @abstractmethod
    def run(self):
        pass

    """
        Пример одного из общих методов обработки данных.
        В данном случае метод просто сортирует входной датасет по значению заданной колонки (аргумент col)
        
        ВАЖНО! Следует логически разделять методы обработки, например, отдельный метод для сортировки, 
        отдельный метод для удаления "пустот" в датасете и т.д. Это позволит гибко применять необходимые
        методы при переопределении метода run для того или иного типа обработчика.
        НАПРИМЕР, если ваш источник данных это не файл, а база данных, тогда метод сортировки будет не нужен,
        т.к. сортировку можно сделать при выполнении SQL-запроса типа SELECT ... ORDER BY...
    """
    def sort_data_by_col(self, df: pandas.DataFrame, colname: str, asc: bool) -> pandas.DataFrame:
            return df.sort_values(by=[colname], ascending=asc)

    def remove_col_by_name(self, df: pandas.DataFrame, colname: List[str]) -> pandas.DataFrame:
        return df.drop(colname, axis=1)

    def sort_by_filter(self, df: pandas.DataFrame, filter_expr: str) -> pandas.DataFrame:
        return df.query(filter_expr)

    # Абстрактный метод для вывоа результата на экран
    @abstractmethod
    def print_result(self):
        pass


# Реализация класса-обработчика csv-файлов
class CsvDataProcessor(DataProcessor):
    # Переобпределяем конструктор родительского класса
    def __init__(self, datasource):
        DataProcessor.__init__(self, datasource)    # инициализируем конструктор родительского класса для получения общих атрибутов
        self.separator = ';'        # дополнительный атрибут - сепаратор по умолчанию
    """
        Переопределяем метод инициализации источника данных.
        Т.к. данный класс предназначен для чтения CSV-файлов, то используем метод read_csv
        из библиотеки pandas
    """
    def read(self):
        try:
            self._dataset = pandas.read_csv(self._datasource, sep=self.separator, header='infer', names=None, encoding="utf-8")
            # Читаем имена колонок из файла данных
            col_names = self._dataset.columns
            # Если количество считанных колонок < 2 возвращаем false
            if len(col_names) < 2:
                return False
            return True
        except Exception as e:
            print(str(e))
            return False

    #    Сортируем данные по значениям колонки "LKG" и сохраняем результат в атрибуте result
    def run(self):
        cleaned_result = self.remove_col_by_name(self._dataset, ["dateAdded"])
        target_values = ["directedBy", "title"]
        for t in target_values:
            cleaned_result = self.sort_data_by_col(cleaned_result, t, False)
        self.result = pandas.concat([self.result, cleaned_result], ignore_index=True)

    def print_result(self):
        print(f'Running CSV-file processor!\n', self.result)


# Реализация класса-обработчика txt-файлов
class TxtDataProcessor(DataProcessor):
    # Реализация метода для чтения TXT-файла
    def read(self):
        try:
            self._dataset = pandas.read_table(self._datasource, sep='\s+', engine='python')
            col_names = self._dataset.columns
            if len(col_names) < 2:
                return False
            return True
        except Exception as e:
            print(str(e))
            return False

    def run(self):
        cleaned_result = self.remove_col_by_name(self._dataset, ["dateAdded"])
        target_values = ["directedBy", "title"]
        for t in target_values:
            cleaned_result = self.sort_data_by_col(cleaned_result, t, False)
        self.result = pandas.concat([self.result, cleaned_result], ignore_index=True)

    def print_result(self):
        print(f'Running TXT-file processor!\n', self.result)
# Реализация класса-обработчика json-файлов
class JSONDataProcessor(DataProcessor):
    # Реализация метода для чтения JSON-файла
    def read(self):
        try:
            self._dataset = pandas.read_json(self._datasource, lines=True)
            col_names = self._dataset.columns
            if len(col_names) < 2:
                return False
            return True
        except Exception as e:
            print(str(e))
            return False

    def run(self):
        cleaned_result = self.remove_col_by_name(self._dataset, ["dateAdded", "avgRating"])
        target_values = ["directedBy", "title"]
        for t in target_values:
            cleaned_result = self.sort_data_by_col(cleaned_result, t, True)
        self.result = pandas.concat([self.result, cleaned_result], ignore_index=True)

    def print_result(self):
        print(f'Running JSON-file processor!\n', self.result)