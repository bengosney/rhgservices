# Django
from django.template import Library, Node

register = Library()


@register.tag
def compress(parser, token):
    nodelist = parser.parse(("endcompress",))
    parser.delete_first_token()
    return LinelessNode(nodelist, "")


@register.tag
def lineless(parser, token):
    nodelist = parser.parse(("endlineless",))
    parser.delete_first_token()
    return LinelessNode(nodelist, "\n")


class LinelessNode(Node):
    def __init__(self, nodelist, join):
        self.nodelist = nodelist
        self.join = join

    def render(self, context):
        input_str = self.nodelist.render(context)
        output_str = ""
        for line in input_str.splitlines():
            if clean_line := line.strip():
                output_str = self.join.join((output_str, clean_line))
        return output_str.strip()
