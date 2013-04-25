from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

root= """<div class="taxrow">
<div class="taximgs">
<img height=20px width=20px src="/static/tax-root.png"><img height=20px width=20px src="/static/tax-root.png">
</div>
<div class="taxname">
<a href="/browse">Root</a>
</div>
</div>"""

rootbranch = """<div class="taxrow">
<div class="taximgs">
<img height=20px width=20px src="/static/tax-root.png"><img height=20px width=20px src="/static/tax-branch.png">
</div>
<div class="taxname">
<a href="/browse">Root</a>
</div>
</div>"""

next_line = """<img height=20px width=20px src="/static/tax-corner.png"><img height=20px width=20px src="/static/tax-branch.png">
</div>
<div class="taxname">
<a href="/browse/%s">%s</a>
</div>"""

last_line = """<img height=20px width=20px src="/static/tax-corner.png"><img height=20px width=20px src="/static/tax-root.png">
</div>
<div class="taxname">
<a href="/browse/%s">%s</a>
</div>"""

@register.simple_tag
def lineage(tax_list):
    i = 1
    if len(tax_list) > 0:
        output = rootbranch
    else:
        output = root
    for tax in tax_list:
        if tax.tax_id==0 or tax.tax_id==1:
            continue
        else:
            padding = i
            output += '<div class="taxrow"><div class="taximgs">'
            paddingtext = '<img height=20px width=20px src="/static/tax-padding.png">'
            output += (paddingtext * padding) 
            if i < len(tax_list):
                output += (next_line % ( tax.tax_id, tax.tax_name ))
            else:
                output += (last_line % ( tax.tax_id, tax.tax_name ))
            output += '</div>'
            i += 1
    return output
