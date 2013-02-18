from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

root="""-+&nbsp;<a href="/browse">Root</a>"""
next_line="""+-+-&nbsp;<a href="/browse/%s">%s</a>"""

@register.simple_tag
def lineage(tax_list):
    i = 0
    output = root
    for tax in tax_list:
        if tax.tax_id==0 or tax.tax_id==1:
            continue
        else:
            padding = i*2 + 1
            i += 1
            output += "<br />" + ("&nbsp;" * padding) + (next_line % ( tax.tax_id, tax.tax_name ))
    return output
