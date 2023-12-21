from selectolax.parser import HTMLParser
from utils.extract_playwright import extract_html_body
from utils.parse import parse_raw_attributes
from config.tools import get_config
from config.logging_config import logger
from utils.postprocess import format_and_transform, save_to_file, get_common_items, get_unique_items, unpack_list_of_tuples
from classes.item import Item


def scrape_parse_and_save(config_file: str):
    config = get_config(f"config/{config_file}.json")

    # playwright scrapes the page
    html = extract_html_body(config.get("url"), config.get("button_selector"),
                             config.get("popup") if "popup" in config.keys() else None)

    # selectolax parses item containers
    tree = HTMLParser(html)
    all_items_nodes = tree.css(config.get("container").get("selector"))

    # logging amount of items
    logger.info("Amount of items parsed: " + str(len(all_items_nodes)))

    parsed_data = []

    # parsing item attributes
    for node in all_items_nodes:
        attrs = parse_raw_attributes(node, config.get("item_attributes"))
        attrs = format_and_transform(attrs, config.get("url"))
        parsed_data.append(Item(**attrs))

    # TODO: get rid of it
    # save_to_file(parsed_data (old), config_file)

    return parsed_data


if __name__ == "__main__":
    eldorado_items = scrape_parse_and_save("eldorado")
    foxtrot_items = scrape_parse_and_save("foxtrot")

    common_items = get_common_items(eldorado_items, foxtrot_items, check_availability=True)
    unique_eldorado_items = get_unique_items(eldorado_items, foxtrot_items)
    unique_foxtrot_items = get_unique_items(foxtrot_items, eldorado_items)

    save_to_file(unpack_list_of_tuples(common_items, "eldorado", "foxtrot"), "common")
    save_to_file(unique_eldorado_items, "eldorado_unique")
    save_to_file(unique_foxtrot_items, "foxtrot_unique")

