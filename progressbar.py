import sys
import lxml.html as lhtml
from lxml.html import Element


def get_progressbar_element(percentage):
    progressbar_child_element = Element("div")
    percentage = int(percentage)
    if percentage >= 70:
        # green
        progressbar_child_element.attrib['class'] = "progress-bar progress-bar-success progress-bar-striped"
    elif percentage >= 50:
        progressbar_child_element.attrib['class'] = "progress-bar progress-bar-warning progress-bar-striped"
    else:
        progressbar_child_element.attrib['class'] = "progress-bar progress-bar-danger progress-bar-striped"
    progressbar_child_element.attrib['role'] = "progressbar"
    progressbar_child_element.attrib['aria-valuenow'] = "10"  # "{}".format(percentage)
    progressbar_child_element.attrib['aria-valuemin'] = "0"
    progressbar_child_element.attrib['aria-valuemax'] = "100"
    progressbar_child_element.attrib['style'] = "width:{}%; text-align:left; padding-left: 5px;".format(percentage)
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
    v = html.xpath('//*[@id="index"]/table/thead/tr/th[@class="right shortkey_c"]')[0]
    v.attrib["style"] = "text-align:center;width:20em;"
    # table body
    for elm in html.xpath('//*[@id="index"]/table/tbody/tr/td[5]'):
        percentage = elm.text.split("%")[0]    # xx% -> xx
        elm.text = ""
        elm.append(get_progressbar_element(percentage))
    # table footer
    elm = html.xpath('//*[@id="index"]/table/tfoot/tr/td[@class="right"]')[0]
    percentage = elm.text.split("%")[0]    # xx% -> xx
    elm.text = ""
    elm.append(get_progressbar_element(percentage))

    # output html
    with open(output_filename, 'w') as fp:
        fp.write(lhtml.tostring(html, encoding=str))


def add_bootstrap_in_html_header(input_filename, output_filename):
    with open(input_filename) as fp:
        htmlstring = fp.read()
    bootstrap = Element("link")
    bootstrap.attrib["rel"] = "stylesheet"
    bootstrap.attrib["href"] = "static/css/bootstrap.min.css"
    bootstrap.attrib["type"] = "text/css"
    html = lhtml.fromstring(htmlstring)
    html.head.append(bootstrap)
    with open(output_filename, 'w') as fp:
        fp.write(lhtml.tostring(html, encoding=str))


def main():
    add_bootstrap_in_html_header(sys.argv[1], sys.argv[1])
    add_progressbar(sys.argv[1], sys.argv[1])


if __name__ == '__main__':
    main()
