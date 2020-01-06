import re


def remove_color_tag(text):
    pattern = r'\[/?color.*?\]'
    no_color_text = re.sub(pattern, '', text)
    return no_color_text