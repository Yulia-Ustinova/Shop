from dataclasses import dataclass
import duckdb
from pathlib import Path

@dataclass
class Item:
    """класс товара с описанием атрибутов"""
    id_item: int
    name_item: str
    price_item: int
    quantity_items: int


class DatabaseWork:
    """класс работы с базой"""

    def __init__(self, db_name):
        self.db_name = db_name

    def do_sql(self, request: list) -> None:
        """метод, выполняющий sql-запрос без возврата чего-либо"""
        connection = duckdb.connect(self.db_name)
        for r in request:
            connection.sql(r)
        connection.close()

    def get_all(self, request: str) -> list:
        """метод, возвращающий все значения из базы в виде списка tuples"""
        connection = duckdb.connect(self.db_name)
        result = connection.sql(request).fetchall()
        connection.close()
        return result

    def get_one(self, request: str) -> tuple:
        """метод, возвращающий одно значение из базы в виде tuple"""
        connection = duckdb.connect(self.db_name)
        result = connection.sql(request).fetchone()
        connection.close()
        return result

    def check_existence(self):
        """проверка, существует ли база"""
        return Path(self.db_name).exists()

class ShopModel:
    """Вносит изменения и манипулирует товарами (Item)"""

    _shop_db = "shop_db.duckdb"
    _items_tbl = "items"
    _sales_tbl = "sales"

    def __init__(self) -> None:
        self.db = DatabaseWork(self._shop_db)
        if not self.db.check_existence():
            self._first_launch()

    def _first_launch(self) -> None:
        """Исп-ся для 1 подключения:
        - задает последовательное создание id,
        - создает базу данных товаров duckdb,
        - заполняет первые данные
        - создает базу данных продаж duckdb"""

        create_seq = "CREATE SEQUENCE id_sequence START 1"
        create_tbl_items = f"""
                        CREATE TABLE {self._items_tbl}(
                        id INTEGER DEFAULT nextval('id_sequence'),
                        name varchar,
                        price integer,
                        quantity integer)
                        """
        insert_i = f"""
                        INSERT INTO {self._items_tbl} 
                        (name, price, quantity)
                        VALUES
                        ('Помидоры', 20, 100)
                        """
        create_tbl_sales = f"""
                        CREATE TABLE {self._sales_tbl}(
                        item_id integer,
                        total_price integer,
                        quantity integer)
                        """
        self.db.do_sql([create_seq, create_tbl_items, insert_i, create_tbl_sales])

    def get_list(self) -> list:
        """метод для получения списка товаров"""
        select = f"""
                    SELECT *
                    FROM {self._items_tbl}
                    """
        list_items = self.db.get_all(select)
        items = []
        for tup in list_items:
            items.append(Item(*tup))
        return items

    def add_to_list(self, name_item: str, price_item: int, qty_item: int) -> None:
        """метод, добавляющий товар в список"""
        insert_i = f"""
                    INSERT INTO {self._items_tbl} 
                    (name, price, quantity)
                    VALUES
                    ('{name_item}', {price_item}, {qty_item})
                    """
        self.db.do_sql([insert_i])

    def check_id(self, id_item: int) -> int:
        """метод, проверяющий, существует ли входящий id"""
        find_id = f"""
                    SELECT id
                    FROM {self._items_tbl}
                    WHERE id = {id_item}
                    """
        found_id = self.db.get_one(find_id)
        if found_id:
            return 1
        else:
            return 0

    def check_qty(self, id_item: int, qty_item: int) -> int:
        """метод, проверяющий количество товара в наличии"""
        get_qty = f"""
                    SELECT quantity
                    FROM {self._items_tbl}
                    WHERE id = {id_item}
                    """
        real_qty = self.db.get_one(get_qty)[0]
        if real_qty >= qty_item:
            return 1
        else:
            return 0

    def change_qty_and_get_ttl_price(self, id_item: int, qty_item: int) -> int:
        """метод, изменяющий количество товара после продажи и возвращающий сумму продажи"""
        update_qty = f"""
                        UPDATE {self._items_tbl}
                        SET quantity = quantity - {qty_item}
                        WHERE id = {id_item}
                        """
        self.db.do_sql([update_qty])
        get_cur_price = f"""
                                SELECT price
                                FROM {self._items_tbl}
                                WHERE id = {id_item}
                                """
        cur_price = self.db.get_one(get_cur_price)[0]
        ttl_price = cur_price * qty_item
        update_sales = f"""
                        INSERT INTO {self._sales_tbl} VALUES
                        ({id_item}, {ttl_price}, {qty_item})
                        """
        self.db.do_sql([update_sales])
        return ttl_price

    def add_qty(self, id_item: int, qty_item: int) -> None:
        """Метод, увеличивающий количество товара на складе"""
        update_qty = (f"""
                        UPDATE {self._items_tbl}
                        SET quantity = quantity + {qty_item}
                        WHERE id = {id_item}
                        """)
        self.db.do_sql([update_qty])

    def subtract_qty(self, id_item: int, qty_item: int) -> None:
        """Метод, уменьшающий количество товара на складе"""
        update_qty = f"""
                            UPDATE {self._items_tbl}
                            SET quantity = quantity - {qty_item}
                            WHERE id = {id_item}
                            """
        self.db.do_sql([update_qty])

    def get_sales_report(self) -> list:
        """метод, получающий информацию о продажах из таблицы sales"""
        get_sql_report = f"""
                                SELECT s.item_id, i.name, sum(s.total_price) as ttl_price, sum(s.quantity) as ttl_qty
                                FROM {self._sales_tbl} as s
                                    join {self._items_tbl} as i on s.item_id = i.id
                                GROUP BY s.item_id, i.name
                                """
        sql_report = self.db.get_all(get_sql_report)
        report = []
        for tup in sql_report:
            saled_item = list(tup)
            report.append(saled_item)
        return report
