from .crawler import MegaCrawler, PhiLongCrawler, XuanVinhCrawler, TikiCrawler


class ShopCrawler:

    @classmethod
    def fetch_data(cls, shop_id):
        if shop_id == 1:
            return XuanVinhCrawler.fetch_data()
        elif shop_id == 2:
            return PhiLongCrawler.fetch_data()
        elif shop_id == 3:
            return MegaCrawler.fetch_data()
        # elif shop_id == 4:
        #     return TikiCrawler.fetch_data()
