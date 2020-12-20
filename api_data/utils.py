from bs4 import BeautifulSoup
import re

FAKE_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Accept': '*/*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://shopee.vn/',
    'X-Shopee-Language': 'vi',
    'X-Requested-With': 'XMLHttpRequest',
    'X-API-SOURCE': 'pc'
}

ITEM_FIELDS = ["id", "description", "name", "price", "stock", "rating_average", "review_count", "specifications"]


# only works for tiki
def get_specifications(specs):
    attributes = {
        "Thông tin chung": ["Thương hiệu", "Kích thước", "Trọng lượng"],
        "Bộ xử lý": ["CPU", "Chip set", "Hệ điều hành"],
        "Màn hình": ["Độ phân giải", "Kích thước màn hình", "Loại/ Công nghệ màn hình"],
        "Đồ họa": ["Card đồ họa"],
        "Đĩa cứng": ["Dung lượng ổ cứng", "Loại ổ đĩa"],
        "Bộ nhớ": ["RAM", "Loại RAM", "Bus"],
        "Thông tin pin": ["Loại pin"]
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
    result_fields = list(result.keys())
    title = list(attributes.keys())
    for spec in specs:
        if spec.get('name') == title[0]:
            fields = attributes.get(title[0])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[0]] = attr.get('value')
                elif attr.get('name') == fields[1]:
                    result[result_fields[1]] = attr.get('value')
                elif attr.get('name') == fields[2]:
                    result[result_fields[2]] = attr.get('value')

        if spec.get('name') == title[1]:
            fields = attributes.get(title[1])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[3]] = attr.get('value')
                if attr.get('name') == fields[1]:
                    result[result_fields[3]] = result[result_fields[3]] + " " + attr.get('value')

        if spec.get('name') == title[2]:
            fields = attributes.get(title[2])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[4]] = attr.get('value')
                elif attr.get('name') == fields[1]:
                    result[result_fields[5]] = attr.get('value')

        if spec.get('name') == title[3]:
            fields = attributes.get(title[3])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[6]] = attr.get('value')

        if spec.get('name') == title[4]:
            fields = attributes.get(title[4])
            for attr in spec.get('attributes'):
                result[result_fields[7]] = result[result_fields[7]] + "&" + attr.get('value')

        if spec.get('name') == title[5]:
            fields = attributes.get(title[5])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[8]] = attr.get('value')

        if spec.get('name') == title[6]:
            fields = attributes.get(title[6])
            for attr in spec.get('attributes'):
                if attr.get('name') == fields[0]:
                    result[result_fields[9]] = attr.get('value')

    return result

def has_cpu(text):
    for i in specs_dictionaries.get('cpu'):
        if i in text.lower():
            return True
    return False


def has_ram(text):
    for i in specs_dictionaries.get('ram'):
        if i in text.lower():
            return True
    return False


def has_screen(text):
    for i in specs_dictionaries.get('display'):
        if i in text.lower():
            return True
    return False


def has_disk(text):
    for i in specs_dictionaries.get('disk'):
        if i in text.lower():
            return True
    return False


def has_vga(text):
    for i in specs_dictionaries.get('vga'):
        if i in text.lower():
            return True
    return False


def has_dimension(text):
    for i in specs_dictionaries.get('dimension'):
        if i in text.lower():
            return True
    return False


def has_battery(text):
    for i in specs_dictionaries.get('battery'):
        if i in text.lower():
            return True
    return False


def has_weight(text):
    for i in specs_dictionaries.get('weight'):
        if i in text.lower():
            return True
    return False


specs_dictionaries = {
    'cpu': ['cpu', 'bộ vi xử lý', 'chip', 'bộ vxl'],
    'ram': ['ddr3', 'ddr4', 'ram'],
    'disk': ['ssd', 'hdd'],
    'display': ['13.3', 'inch', '14\'\'', '15.6', 'fhd', 'display'],
    'vga': ["chipset đồ họa", "card đồ họa", "đồ họa", "vga", "Card đồ hoạ", "gpu", "card màn hình"],
    'dimension': [],
    'weight': ['kg'],
    'battery': ['pin']
}

def clean_data(item):
    result = {
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
    description = item.description
    end = description.find('<span')
    temp_description = description[0:end:1]
    #print(temp_description)import re

    texts = re.split('<br />|\n',temp_description)
    for text in texts:
        text = text.strip()
        if not result['cpu'] and has_cpu(text):
            result['cpu'] = text
        if not result['ram'] and has_ram(text):
            result['ram'] = text
        if not result['disk'] and has_disk(text):
            result['disk'] = text
        if not result['vga'] and has_vga(text):
            result['vga'] = text
        if not result['battery'] and has_battery(text):
            result['battery'] = text
        if has_screen(text):
            if not result["display"]:
                result["display"] = text
            if not result["screen_size"]:
                if '15.' in text.lower():
                    result["screen_size"] = 15.6
                    continue
                elif '13.' in text.lower():
                    print(text)
                    result["screen_size"] = 13.3
                    continue
                elif '14.' in text.lower() or '14' in text.lower() or '14\'\'' in text.lower():
                    result["screen_size"] = 14
                    continue
                elif '17.' in text.lower():
                    result["screen_size"] = 17.3
                    continue
        # if (text1.startswith(f[4])):
        #     pass
        # i = text1.index(f[4])
        # str1 = text1.split(':')[1]
        # result['display'] = str1.split(',')[1]
        # result['screen_size'] = str1.split(',')[0]
        # if not item.battery and (text1.startswith(f[5])):
        #     i = text1.index(f[5])
        #     result["battery"] = text1[i:]
    #print(result)

    soup = BeautifulSoup(text, "lxml")
    #print(soup.prettify())
    #s = soup.find_all("span", id=lambda value: value and value.startswith("input_line_"))
    s = soup.findAll('span', {"class": ""})
    #print(soup.find_all("div", id=lambda value: value and value.startswith("input_line_")))
    # for s1 in s:
    #     if(s1.get('data-mention')):
    #         s3 = str(s1.get('data-mention'))
    #         if(f[6] in str(s1.get('data-mention'))):
    #             i = s3.index(f[6])
    #             i1 = s3.index('kg')
    #             result["weight"] = s3[i + 12:i1 + 2]
    #             result["dimension"] = s1.get('data-mention')
    return result
