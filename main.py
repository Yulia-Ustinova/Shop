from shop_model import ShopModel
from shop_view import ShopView
from shop_controller import ShopController

if __name__ == "__main__":

    shop_model = ShopModel()
    shop_view = ShopView()
    shop_controller = ShopController(shop_model, shop_view)

    shop_controller.run()
