from selectolax.parser import Node
from re import findall, compile, sub, IGNORECASE
from pandas import DataFrame
from datetime import datetime


def get_attribute_from_node(node: Node, attr: str):
    """
    Provide a Selectolax Node and get a specific HTML attribute.
    :param node: a Selectolax Node
    :param attr: attribute name, str
    :return: attribute value
    """
    if node is None or not issubclass(Node, type(node)):
        raise ValueError("The function expects a Selectolax Node type")

    return node.attributes.get(attr)


def remove_words_from_text(text: str, words_to_remove: [str]):
    """
    Remove `words_to_remove` from `text` (if found).
    :param text: original str
    :param words_to_remove: [str]
    :return: new str
    """
    if not issubclass(str, type(text)) or not issubclass(list, type(words_to_remove)):
        raise ValueError("The function expects arguments of str type")

    new_text = text
    for word in words_to_remove:
        new_text = sub(r'\b{}\b'.format(word), '', new_text, flags=IGNORECASE)
    return new_text.strip()


def regex_findall(input_text: str, pattern: str):
    """
    Find all matches with RegEx pattern in `input_text`.
    :param input_text: str
    :param pattern: str, RegEx pattern
    :return: [str]
    """
    if input_text is None:
        return None

    return findall(pattern, input_text)


def is_text_in_list(input_text: str, str_list: list):
    """
    Checks if `input_text` is contained in `str_list`. Case-insensitive.
    :param input_text: str
    :param str_list: [str]
    :return: bool
    """
    if input_text is None:
        return None

    pattern = compile(input_text, flags=IGNORECASE)
    for str_element in str_list:
        if pattern.search(str_element):
            return True

    return False


def transform_currency(input_text: str):
    """
    Checks if `input_text` contains any signs of currency and returns a unified value for respective currency found.
    :param input_text: str
    :return: str
    """
    if input_text is None:
        return None

    patterns_uah = [compile('грн', flags=IGNORECASE), compile('₴'), compile('uah', flags=IGNORECASE)]
    for pattern in patterns_uah:
        if pattern.search(input_text):
            return 'UAH'
    return input_text


def get_domain(link: str):
    """
    Extracts protocol, subdomain, domain name and top-level domain from the link.
    :param link: str
    :return: str
    """
    return compile(r'http(?:s|)://(?:www.|)\w+.[a-zA-Z]+(?:.[a-zA-Z]+|)').findall(link)[0]


def format_and_transform(attrs: dict, url: str):
    """
    Applies a respectful transformation on every value from `attrs` dictionary.
    :param attrs: dict with all the data for 1 item (title, model etc.)
    :param url: website URL
    :return: dict (with changed values)
    """

    # dictionary that defines how every value of 'attrs' should be transformed
    transforms = {
        "title": lambda x: remove_words_from_text(x, ["Смартфон", "APPLE"]),
        "current_price": lambda x: None if x is None else float("".join(regex_findall(x, r'\d+'))),
        "currency": lambda x: transform_currency(x),
        "link": lambda x: get_domain(url) + get_attribute_from_node(x, "href"),
        "availability": lambda x: is_text_in_list(x, ['в наявності', 'закінчується'])
    }

    for key, value in transforms.items():
        # in diff. words - if "key" is present in 'attrs', apply transform on its value
        if key in attrs:
            attrs[key] = value(attrs[key])

    return attrs


def get_common_items(list1: [object], list2: [object], check_availability: bool):
    """
    Provide 2 lists of items and get a list of tuples with both common items.
    :param list1: list
    :param list2: list
    :param check_availability: bool
    :return: list of tuples
    """
    common_items = []
    for item1 in list1:
        for item2 in list2:
            if check_availability:
                if item1 == item2 and item1.availability is True and item1.availability is True:
                    common_items.append((item1, item2))
                    break
            elif item1 == item2:
                common_items.append((item1, item2))
                break

    return common_items


def get_unique_items(list1: [object], list2: [object]):
    """
    Returns a list of elements present in list1 but not in list2.
    :param list1: list
    :param list2: list
    :return: list
    """
    # convert both lists to sets
    set1 = set(list1)
    set2 = set(list2)

    # use set.difference to find elements unique to list1
    return list(set1.difference(set2))


def unpack_list_of_tuples(input_list: list[(object, object)], domain1: str, domain2: str):
    """
    Provide a list of tuples from `get_common_items` function to unpack it into list of dictionaries that contain
    attributes of both instances of every tuple.
    Returned list can be easily converted to padnas DataFrame.
    Attributes will be named as `domain_attribute_name`
    :param input_list: list of tuples with items
    :param domain1: str (website domain)
    :param domain2: str (website domain)
    :return: list of dictionaries
    """
    attributes_of_both = []
    for pair in input_list:
        item1 = pair[0]
        item2 = pair[1]
        attributes_of_both.append({
            "title": item1.title,
            "{}_price".format(domain1): item1.current_price,
            "{}_currency".format(domain1): item1.currency,
            "{}_price".format(domain2): item2.current_price,
            "{}_currency".format(domain2): item2.currency,
            "{}_link".format(domain1): item1.link,
            "{}_link".format(domain2): item2.link,
            # rest is optional, can be commented
            "{}_availability".format(domain1): item1.availability,
            "{}_availability".format(domain2): item2.availability,
            "{}_model".format(domain1): item1.model,
            "{}_model".format(domain2): item2.model,
            "{}_memory".format(domain1): item1.memory,
            "{}_memory".format(domain2): item2.memory,
            "{}_color".format(domain1): item1.color,
            "{}_color".format(domain2): item2.color,
            "{}_model_number".format(domain1): item1.model_number,
            "{}_model_number".format(domain2): item2.model_number
        })

    return attributes_of_both


def save_to_file(data: list[object], filename="extract"):
    """
    Saves a list of dataclass instances to CSV file.
    :param data: a list of dataclass instances
    :param filename: filename (will be appended to current date)
    :return: None
    """
    if data is None:
        raise ValueError("The function expects `data` to be provided as list of objects")

    filename = f"parsed_data/{filename}_{datetime.now().strftime('%Y_%m_%d')}.csv"
    df = DataFrame(data)
    df.to_csv(filename, index=False)
