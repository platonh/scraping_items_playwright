import pytest
from classes.item import Item
import utils.postprocess


def test_regex():
    iphone = Item('iPhone 13 Pro Max 128GB Silver (MLL73)', 10, 'uah', 'www.', True)
    assert iphone.model == 'iPhone 13 Pro Max'
    assert iphone.memory == '128GB'
    assert iphone.color == 'Silver'
    assert iphone.model_number == 'MLL73'


def test_regex_2():
    iphone = Item('iPhone 15 Plus 128GB Black (MU0Y3RX/A)', 10, 'uah', 'www.', True)
    assert iphone.model == 'iPhone 15 Plus'
    assert iphone.memory == '128GB'
    assert iphone.color == 'Black'
    assert iphone.model_number == 'MU0Y3RX/A'


def test_regex_3():
    iphone = Item('iPhone 14 Pro Max 512GB Space Black (MQAF3RX/A)', 10, 'uah', 'www.', True)
    assert iphone.model == 'iPhone 14 Pro Max'
    assert iphone.memory == '512GB'
    assert iphone.color == 'Space Black'
    assert iphone.model_number == 'MQAF3RX/A'


def test_regex_4():
    iphone = Item('Space Black 512GB iPhone 14 Pro Max (MQAF3RX/A)', 10, 'uah', 'www.', True)
    assert iphone.model == 'iPhone 14 Pro Max'
    assert iphone.memory == '512GB'
    assert iphone.color == 'Space Black'
    assert iphone.model_number == 'MQAF3RX/A'


def test_item_from_dict():
    # only Python 3.10+
    my_dict = {'title': 'iPhone 14 Pro Max 512GB Space Black (MQAF3RX/A)', 'current_price': 1000.0, 'currency': 'uah', 'link': 'www', 'availability': True}
    iphone = Item(**my_dict)
    print(iphone)


def test_item_from_dict_2():
    # only Python 3.10+
    my_dict = {'title': 'iphone lol', 'current_price': 1000.0, 'currency': 'uah', 'link': 'www', 'availability': True}
    iphone = Item(**my_dict)
    print(iphone)


def test_item_comparison_1():
    iphone1 = Item(**{
        'title': 'iPhone 14 Pro Max 512GB Space Black (MQAF3RX/A)',
        'current_price': 1000.0,
        'currency': 'uah',
        'link': 'www',
        'availability': True
    })
    iphone2 = Item(**{
        'title': 'iphone 14 pro max 512 gb bleck space',
        'current_price': 1000.0,
        'currency': 'uah',
        'link': 'www',
        'availability': True
    })
    assert iphone1 == iphone2


def test_item_comparison_2():
    iphone1 = Item(**{
        'title': 'iPhone 13 Pro 1TB Sierra Blue (MQAF3RX/A)',
        'current_price': 1000.0,
        'currency': 'uah',
        'link': 'www',
        'availability': True
    })
    iphone2 = Item(**{
        'title': 'iphone 13 pro blue siera 1 tb',
        'current_price': 1000.0,
        'currency': 'uah',
        'link': 'www',
        'availability': True
    })
    assert iphone1 == iphone2


def test_item_comparison_3():
    iphone1 = Item(**{
        'title': 'iPhone 13 1TB Red Product (MQAF3RX/A)',
        'current_price': 1000.0,
        'currency': 'uah',
        'link': 'www',
        'availability': True
    })
    iphone2 = Item(**{
        'title': 'iphone 13 1 tb (PRODUCT)Red',
        'current_price': 1000.0,
        'currency': 'uah',
        'link': 'www',
        'availability': True
    })
    assert iphone1 == iphone2


def test_item_common_func():
    iphone1 = Item(**{
        'title': 'iPhone 13 1TB Red Product (MQAF3RX/A)',
        'current_price': 1000.0,
        'currency': 'uah',
        'link': 'www',
        'availability': True
    })
    iphone2 = Item(**{
        'title': 'iphone 13 1 tb (PRODUCT)Red',
        'current_price': 1000.0,
        'currency': 'uah',
        'link': 'www',
        'availability': True
    })

    common_items = utils.postprocess.get_common_items([iphone1, iphone2], [iphone1, iphone2], True)
    unique_items = utils.postprocess.get_unique_items([iphone1, iphone2], [iphone1])

    assert common_items == [(iphone1, iphone1), (iphone2, iphone2)]
    assert unique_items == [iphone2]

