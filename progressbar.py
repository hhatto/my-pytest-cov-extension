import os
import sys
import shutil
import lxml.html as lhtml
from lxml.html import Element


def get_progressbar_element(percentage):
    progressbar_child_element = Element("div")
    percentage = int(percentage)
    if percentage >= 70:
        # green
        progressbar_child_element.attrib[
            "class"
        ] = "progress-bar progress-bar-success progress-bar-striped"
    elif percentage >= 50:
        progressbar_child_element.attrib[
            "class"
        ] = "progress-bar progress-bar-warning progress-bar-striped"
    else:
        progressbar_child_element.attrib[
            "class"
        ] = "progress-bar progress-bar-danger progress-bar-striped"
    progressbar_child_element.attrib["role"] = "progressbar"
    progressbar_child_element.attrib["aria-valuenow"] = "10"  # "{}".format(percentage)
    progressbar_child_element.attrib["aria-valuemin"] = "0"
    progressbar_child_element.attrib["aria-valuemax"] = "100"
    progressbar_child_element.attrib[
        "style"
    ] = "width:{}%; text-align:left; padding-left: 5px;".format(percentage)
    progressbar_child_element.text = "{}%".format(percentage)
    progressbar_element = Element("div")
    progressbar_element.attrib["class"] = "progress"
    progressbar_element.attrib["style"] = "margin-bottom:0;"
    progressbar_element.append(progressbar_child_element)
    return progressbar_element


def add_progressbar(input_filename, output_filename):
    # load html elements
    with open(input_filename) as fp:
        htmlstring = fp.read()
    html = lhtml.fromstring(htmlstring)

    # table header
    th_num = len(html.xpath('//*[@id="index"]/table/thead/tr/th'))
    v = html.xpath('//*[@id="index"]/table/thead/tr/th[@class="right"]')[0]
    v.attrib["style"] = "text-align:center;width:20em;"
    # table body
    for elm in html.xpath(f'//*[@id="index"]/table/tbody/tr/td[{th_num}]'):
        percentage = elm.text.split("%")[0]  # xx% -> xx
        elm.text = ""
        elm.append(get_progressbar_element(percentage))
    # table footer
    elm = html.xpath('//*[@id="index"]/table/tfoot/tr/td[@class="right"]')[0]
    percentage = elm.text.split("%")[0]  # xx% -> xx
    elm.text = ""
    elm.append(get_progressbar_element(percentage))

    # output html
    with open(output_filename, "w") as fp:
        fp.write(lhtml.tostring(html, encoding=str))


def add_bootstrap_in_html_header(input_filename, output_filename):
    with open(input_filename) as fp:
        htmlstring = fp.read()
    bootstrap = Element("link")
    bootstrap.attrib["rel"] = "stylesheet"
    bootstrap.attrib["href"] = "static/css/bootstrap.min.css"
    bootstrap.attrib["type"] = "text/css"
    html = lhtml.fromstring(htmlstring)

    # find link tag
    existing_links = html.head.findall("link")
    if existing_links:
        first_link = existing_links[0]
        first_link_index = html.head.index(first_link)
        html.head.insert(first_link_index, bootstrap)
    else:
        # not found css
        html.head.append(bootstrap)

    with open(output_filename, "w") as fp:
        fp.write(lhtml.tostring(html, encoding=str))


def staticgen(html_path):
    target_dir = os.path.dirname(html_path)
    target_static_dir = os.path.join(target_dir, "static")
    if os.path.exists(target_static_dir):
        # ignore & finish
        return
    script_static_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "static"
    )
    shutil.copytree(script_static_dir, target_static_dir)


def process_html_file(file_path):
    if not os.path.exists(file_path):
        return
    add_bootstrap_in_html_header(file_path, file_path)
    add_progressbar(file_path, file_path)


def main():
    html_path = sys.argv[1]
    html_dir = os.path.dirname(html_path)

    # Process index.html (main file)
    process_html_file(html_path)

    # Process additional HTML files if they exist
    function_index_path = os.path.join(html_dir, "function_index.html")
    class_index_path = os.path.join(html_dir, "class_index.html")

    process_html_file(function_index_path)
    process_html_file(class_index_path)

    # Copy static files once for all HTML files
    staticgen(html_path)


if __name__ == "__main__":
    main()
