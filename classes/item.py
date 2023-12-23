from dataclasses import dataclass
from re import compile, sub, split, IGNORECASE
from config.logging_config import logger
from nltk.metrics import distance


@dataclass
class Item:
    title: str
    current_price: float
    currency: str
    link: str
    availability: bool = True
    model: str = None
    memory: str = None
    color: str = None
    model_number: str = None

    def __post_init__(self):
        title_copy = self.title

        model_pattern = compile(r"[a-zA-Z]+ (?:\d+|XS|X|SE) (?:Pro Max|Pro|Plus|Mini|)", IGNORECASE)
        memory_pattern = compile(r"(?:32|64|128|256|512|1)(?:\s|)(?:GB|TB)", IGNORECASE)
        model_number_pattern = compile(r"\((?:[A-Z]+[0-9](?:\w+|)(?:/[A-Z]|)|DEMO)\)")
        color_pattern = compile(r"(?:[a-zA-Z]+(?:\s[a-zA-Z]+|)|\(PRODUCT\)(?: |)RED)", IGNORECASE)

        # extracting model
        if self.model is None:
            try:
                self.model = model_pattern.findall(title_copy)[0]
                title_copy = sub(self.model, '', title_copy, flags=IGNORECASE).strip()
            except IndexError:
                logger.warning("No matches to `model_pattern` in `title_copy`. Title: " + title_copy)

        # extracting memory
        if self.memory is None:
            try:
                self.memory = memory_pattern.findall(title_copy)[0]
                title_copy = sub(self.memory, '', title_copy, flags=IGNORECASE).strip()
            except IndexError:
                logger.warning("No matches to `memory_pattern` in `title_copy`. Title: " + title_copy)

        # extracting model_number (if exists)
        if self.model_number is None:
            try:
                model_number = model_number_pattern.findall(title_copy)[0]
                if model_number:
                    self.model_number = sub(r"[()]", '', model_number)
                    title_copy = sub(model_number_pattern, '', title_copy).strip()
            except IndexError:
                logger.warning("No matches to `model_number_pattern` in `title_copy`. Title: " + title_copy)

        # extracting color
        if self.color is None:
            try:
                self.color = color_pattern.findall(title_copy)[0]
            except IndexError:
                logger.warning("No matches to `color_pattern` in `title_copy`. Title: " + title_copy)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplementedError("You can compare `Item` instance only to another `Item` instance.")

        # if both model_numbers are equal, they are 100% same items
        if self.model_number is not None and other.model_number is not None:
            if self.model_number == other.model_number and self.model_number != 'DEMO':
                return True

        # normalize attributes
        model1 = sub(r"[^[a-z0-9]", "", self.model.lower())
        memory1 = sub(r"[^0-9]", "", self.memory)
        color1 = sub(r"[^a-z ]", "", self.color.lower())
        color1_words = split(r"\W+", color1)

        model2 = sub(r"[^[a-z0-9]", "", other.model.lower())
        memory2 = sub(r"[^0-9]", "", other.memory)
        color2 = sub(r"[^a-z ]", "", other.color.lower())
        color2_words = split(r"\W+", color2)

        # sort words in `color`
        color1_words.sort()
        color2_words.sort()
        sorted_color1 = " ".join(color1_words)
        sorted_color2 = " ".join(color2_words)

        # calculate Levenshtein distance between colors
        color_distance = distance.edit_distance(sorted_color1, sorted_color2)

        # define acceptable difference threshold for colors
        diff_threshold = 2

        # compare normalized attributes
        return (model1 == model2 and
                memory1 == memory2 and
                (sorted_color1 == sorted_color2 or color_distance <= diff_threshold))

    def __hash__(self):
        return hash((self.model, self.memory, self.color, self.model_number))
