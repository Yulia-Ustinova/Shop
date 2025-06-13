class ShopController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self) -> None:
        while True:
            menu_shop = self.view.get_menu_shop()

            if menu_shop == 1:
                self.view.show_list_items(self.model.get_list())

            if menu_shop == 2:
                item_name, item_price, item_qty = self.view.ask_for_new_item()
                self.model.add_to_list(item_name, item_price, item_qty)
                self.view.respond_success_new_item()

            if menu_shop == 3:
                id_item = self.view.ask_for_item()
                response = self.model.check_id(id_item)
                if response == 0:
                    self.view.respond_wrong_item()
                else:
                    qty_item = self.view.ask_for_qty()
                    response = self.model.check_qty(id_item, qty_item)
                    if response == 0:
                        self.view.respond_wrong_qty()
                    else:
                        ttl_price = self.model.change_qty_and_get_ttl_price(id_item, qty_item)
                        self.view.respond_ttl_price(ttl_price)

            if menu_shop == 4:
                id_item = self.view.ask_for_item()
                response = self.model.check_id(id_item)
                if response == 0:
                    self.view.respond_wrong_item()
                else:
                    qty_item = self.view.ask_for_qty()
                    self.model.add_qty(id_item, qty_item)
                    self.view.respond_success_qty()

            if menu_shop == 5:
                id_item = self.view.ask_for_item()
                response = self.model.check_id(id_item)
                if response == 0:
                    self.view.respond_wrong_item()
                else:
                    qty_item = self.view.ask_for_qty()
                    response = self.model.check_qty(id_item, qty_item)
                    if response == 0:
                        self.view.respond_wrong_qty()
                    else:
                        self.model.subtract_qty(id_item, qty_item)
                        self.view.respond_success_qty()

            if menu_shop == 6:
                self.view.show_sale_report(self.model.get_sales_report())

            if menu_shop == 7:
                break
