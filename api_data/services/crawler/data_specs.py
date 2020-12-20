import re


class DataSpecs:

    @classmethod
    def safe_price(cls, price):
        pattern = '\d*[\.|,]?\d+'
        size = re.findall(pattern, str(price).replace(',','.'))[0]
        return int(float(size) * 1000000)

    @classmethod
    def get_specifications(cls, seller, brand, name, price, description, specs, thumbnail):
        keyword = {
            "dimension": ["Kích thước", "Kích thước (Dài x Rộng x Cao)"],
            "weight": ["Trọng lượng", "Trọng Lượng", 'Weight'],
            "cpu": ["Bộ VXL", "CPU", "Bộ vi xử lý", "Tên bộ vi xử lý"],
            "display": ["Màn hình", "Display"],
            "screen_size": [],
            "vga": ["Cạc đồ họa", "Card đồ họa", "Card màn hình", "VGA"],
            "disk": ["Ổ cứng", "disk", "Ổ cứng", 'SSD'],
            "ram": ["Bộ nhớ", "RAM", "ram", 'Memory'],
            "battery": ["Kiểu Pin", "Pin", 'Battery'],
        }
        result = {
            "brand": '',
            "dimension": '',
            "weight": '',
            "cpu": '',
            "display": '',
            "screen_size": '',
            "vga": '',
            "disk": '',
            "ram": '',
            "battery": ''
        }
        result.update(brand=brand)
        result.update(seller=seller)
        result.update(name=name)
        result.update(description=description)
        result.update(thumbnails=thumbnail)
        result.update(price=cls.safe_price(price))
        for title in keyword.keys():
            for key in keyword.get(title, []):
                prefix = '\xa0'
                if specs.get(key, None):
                    temp_dict = {
                        title: specs.get(key)
                    }
                    result.update(temp_dict)
                    break
                if specs.get(prefix + key, None):
                    temp_dict = {
                        title: specs.get(prefix + key)
                    }
                    result.update(temp_dict)
                    break
        pattern = '\d*\.?\d+'
        try:
            size = re.findall(pattern, result.get('display'))[0]
            result.update(screen_size=size)
        except Exception:
            result.update(screen_size=0)
        return result