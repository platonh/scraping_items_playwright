from selectolax.parser import Node


def parse_raw_attributes(node: Node, selectors: list):
    """
    Provide a Selectolax Node and parse all the attributes needed from `selectors` list.
    :param node: a Selectolax Node
    :param selectors: a list of dicts; every dict contains attribute's name, selector, match and type.
    :return: a dict of parsed attributes for a single Node.
    """
    parsed = {}

    for s in selectors:
        name = s.get("name")  # attribute name
        selector = s.get("selector")  # CSS selector
        match = s.get("match")  # all or first
        type_ = s.get("type")  # text or node

        try:
            if match == "all":
                matched = node.css(selector)

                if type_ == "text":
                    parsed[name] = [node.text() for node in matched]
                elif type_ == "node":
                    parsed[name] = matched

            elif match == "first":
                matched = node.css_first(selector)

                if type_ == "text":
                    parsed[name] = matched.text()

                elif type_ == "node":
                    parsed[name] = matched

        except AttributeError:
            parsed[name] = None

    return parsed
