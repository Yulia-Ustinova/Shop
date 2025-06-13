from tabulate import tabulate
from shop_model import Item


class ShopView:
    """Взаимодействует с пользователем"""

    def show_list_items(self, items: list[Item]) -> None:
        """метод, выводящий список товаров
        :param items: список товаров (экз-ов класса) из метода get_list в model"""
        list_of_items = []
        for item in items:
            # "class.__dict__" - получает словарь атрибутов экземпляра класса. Ключ - название, значение - значение
            # ".values()" - метод словаря, получающий его значения (против ".keys()" - получающий ключи)
            list_of_values = list(item.__dict__.values())
            list_of_items.append(list_of_values)

        print(tabulate(list_of_items,
                       headers=["ID", "Название", "Цена", "Количество"],
                       tablefmt="simple_outline"))

    def show_sale_report(self, report: list) -> None:
        """Метод, выводящий отчет о продажах"""
        print(tabulate(report,
                       headers=["ID Товара", "Название", "Итоговая цена", "Суммарное количество"],
                       tablefmt="simple_outline"))

    def ask_for_new_item(self) -> tuple:
        """Метод, запрашивающий у пользователя название, цену и количество нового товара"""
        item_name = input("Напишите название нового товара: ")
        item_price = input("Напишите цену нового товара: ")
        item_qty = input("Напишите количество нового товара: ")
        return item_name, item_price, item_qty

    def ask_for_item(self) -> int:
        """Метод, запрашивающий id товара"""
        id_item = int(input("Напишите номер товара: "))
        return id_item

    def ask_for_qty(self) -> int:
        """Метод, запрашивающий количество товара"""
        qty_item = int(input("Напишите количество товара: "))
        return qty_item

    def respond_ttl_price(self, ttl_price: int) -> None:
        """Метод, возвращающий сообщение об успешном изменении количества товара и сумму продажи"""
        print("\nКоличество товара на складе изменено.")
        print(f"Сумма продажи составляет {ttl_price} р.\n")

    def respond_success_qty(self) -> None:
        """Метод, возвращающий сообщение об успешном изменении количества товара"""
        print("\nКоличество товара было успешно изменено.\n")

    def respond_success_new_item(self) -> None:
        """Метод, возвращающий сообщение об успешном внесении нового товара"""
        print("\nНовый товар было успешно внесен.\n")

    def respond_wrong_item(self) -> None:
        """Метод, возвращающий сообщение, что номер, введенный пользователем, не существует"""
        print("\nНомер не существует. Введите существующий номер.\n")

    def respond_wrong_qty(self) -> None:
        """Метод, возвращающий сообщение об ошибке при недостаточном количестве товара"""
        print("\nНедостаточно товара на складе.\n")

    def get_menu_shop(self) -> int:
        print("Что вы хотите сделать?")
        print("1. Посмотреть список всех товаров")
        print("2. Добавить новый товар")
        print("3. Продать товар")
        print("4. Увеличить количество товара на складе (внести поставку)")
        print("5. Уменьшить количество товара на складе (списать часть товара)")
        print("6. Получить отчет о продажах")
        print("7. Выйти из программы")
        return int(input("Введите номер пункта, который хотите выполнить: "))
