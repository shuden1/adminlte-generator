from bs4 import BeautifulSoup, Tag
import sys
from collections import Counter
import os

def remove_script_tags(input_html_file):
    """
    Remove all <script> tags from the input HTML file and update the file.

    Parameters:
    input_html_file (str): Path to the HTML file to be processed.
    """
    with open(input_html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    for script in soup.find_all('script'):
        script.decompose()

    with open(input_html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def clean_html(input_html):
    """
    Clean an HTML file by iterating through each element, limiting the number of child elements
    with the same structure to 5, considering both the child's and its parent's structure.

    Parameters:
    input_html (str): String containing the HTML content to be cleaned.

    Returns:
    str: Cleaned HTML content.
    """
    soup = BeautifulSoup(input_html, 'html.parser')

    # Replace all <iframe> tags with <section> tags
    for iframe in soup.find_all('iframe'):
        new_tag = soup.new_tag("section")
        new_tag.attrs = iframe.attrs
        new_tag.extend(iframe.contents)
        iframe.replace_with(new_tag)

    # Define tags to remove completely
    tags_to_remove = ['script', 'style', 'meta', 'head', 'img', 'footer', 'path', 'svg', 'symbol']

    # Remove specified tags
    for tag in tags_to_remove:
        for element in soup.find_all(tag):
            element.decompose()

    def get_element_signature(element):
        """
        Get a signature consisting of the element's tag name and sorted class attributes.
        """
        if not isinstance(element, Tag):
            return ''
        return (element.name, tuple(sorted(element.attrs.get('class', []))))

    def limit_children(parent):
        """
        Limit the number of direct child elements with a specific combination of parent and child structure to 5.
        """
        child_count = {}
        for child in list(parent.find_all(recursive=False)):  # Direct children only
            parent_signature = get_element_signature(parent)
            child_signature = get_element_signature(child)
            combined_signature = (parent_signature, child_signature)

            child_count[combined_signature] = child_count.get(combined_signature, 0) + 1
            if child_count[combined_signature] > 5:
                child.decompose()

    # Apply the limitation to each element in the document
    for element in soup.find_all(recursive=True):
        limit_children(element)

    for element in soup.find_all():
        if isinstance(element, Tag) and not element.contents and not element.get_text().strip():
            element.decompose()

    # Return the cleaned HTML
    return str(soup)

# Example usage
if __name__ == "__main__":
    input_html = sys.argv[1]
    output_filename = sys.argv[2]
    if os.path.isfile(input_html):
        remove_script_tags(input_html)
        # Now read the updated HTML file and process it further
        with open(input_html, 'r', encoding='utf-8') as file:
            original_html = file.read()

        cleaned_html = clean_html(original_html)
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(cleaned_html)
    else:
        print(f"File not found: {input_html}")
