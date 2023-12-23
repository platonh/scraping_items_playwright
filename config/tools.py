import json

_config = {
    "url": "https://www.foxtrot.com.ua/uk/shop/mobilnye_telefony_apple.html",
    "button_selector": "div[class*=\"card card-more\"]",
    "container": {
        "name": "all_items_nodes",
        "selector": 'div[class*="card js-card sc-product isTracked"]',
        "match": "all",
        "type": "node"
    },
    "item_attributes": [
        {
            "name": "title",
            "selector": 'div[class*="card__body"] > a[class*="card__title"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "current_price",
            "selector": 'div[class*="card__body"] > div[class*="card__col-price"] > div[class*="card__price"] '
                        'div[class*="card__price"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "currency",
            "selector": 'div[class*="card__body"] > div[class*="card__col-price"] > div[class*="card__price"] '
                        'div[class*="card__price"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "link",
            "selector": 'div[class*="card__body"] > a[class*="card__title"]',
            "match": "first",
            "type": "node"
        }
    ]
}


def get_config(file_name=False):
    """
    Open JSON configuration file. If `file_name` is not provided, returns `_config` blueprint from `tools.py`.
    :param file_name: config file name (full path if necessary)
    :return: dict
    """
    if file_name:
        with open(file_name) as file:
            return json.load(file)

    return _config


def generate_config():
    """
    Generate a JSON configuration file with blueprint in `tools.py`.
    :return:
    """
    with open("foxtrot.json", "w") as file:
        json.dump(_config, file, indent=4)


if __name__ == "__main__":
    generate_config()
