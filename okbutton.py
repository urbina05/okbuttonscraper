import argparse
from lxml import html, etree

ORIGINAL_BUTTON_ID = 'make-everything-ok-button'


def get_xpath_element_from_file(file, element_xpath):
    with open(file) as file:
        file_contents = file.read()
        html_tree = html.fromstring(file_contents)

        try:
            (element,) = html_tree.xpath(element_xpath)
        except:
            raise Exception(
                'Could not find exactly one element with the xpath: {}'.format(element_xpath))

        return element

def get_element_description(element):
    return "{}: {}".format(element.getroottree().getpath(
        element), element.text.strip())

def get_class_attrib(class_name):
    return 'contains(@class, "{class_name}")'.format(class_name=class_name)

def test_match_buttons(originalFile, sampleFile):
    original_button_xpath = '//a[@id="{button_id}"]'.format(
        button_id=ORIGINAL_BUTTON_ID)
    original_button = get_xpath_element_from_file(originalFile, original_button_xpath)

    original_button_classes = original_button.attrib['class'].split(' ')

    xpath_class_attribute = ' or '.join(
        [get_class_attrib(button_class) for button_class in original_button_classes])
    xpath_href_attribute = 'contains(@href, "{href_value}")'.format(
        href_value=original_button.attrib['href'])
    xpath_mandatory_attribute = '@rel and @title'

    sample_button_xpath = '//a[({class_attrib}) and {href_attrib} and {mandatory_attrib}]'.format(
        class_attrib=xpath_class_attribute,
        href_attrib=xpath_href_attribute,
        mandatory_attrib=xpath_mandatory_attribute)
    sample_button = get_xpath_element_from_file(sampleFile, sample_button_xpath)

    return (original_button, sample_button)


parser = argparse.ArgumentParser()

parser.add_argument('origin_file_path', help="origin file")
parser.add_argument('other_sample_file_path', help="other sample file")
args = parser.parse_args()

buttons = test_match_buttons(args.origin_file_path,args.other_sample_file_path)
for button in buttons:
    print(get_element_description(button))
