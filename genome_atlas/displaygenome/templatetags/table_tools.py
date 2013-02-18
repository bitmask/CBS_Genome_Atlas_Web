from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

up_arrow = "&#x25B2;"
down_arrow = "&#x25BC;"

@register.simple_tag
def table_header(form_name, column_name, order_by, order_dir, column_text):
    text="""<th onclick="table_sorting('%s','%s','%s','%s')">%s&nbsp;%s</th>"""
    arrow="-"
    if( column_name == str(order_by.value()) ):
        if( order_dir.value() == "ASC" ):
            arrow=up_arrow;
        else:
            arrow=down_arrow;
    return text % (form_name, order_by.html_name, order_dir.html_name, column_name, column_text, arrow);

@register.simple_tag
def paginate(form_name, form_element, page_from, page_to, page_current, step_size):
    page_from = int(page_from)
    page_to = int(page_to)
    page_current = int(page_current)
    step_size = int(step_size)
    needs_first = ( page_current - page_from > step_size )
    needs_last = ( page_to - page_current > step_size)
    text="<div class='paginator'>Pages:&nbsp;&nbsp;"
    previous = max( page_from, page_current - step_size )
    next = min( page_to + 1, page_current + step_size + 1)
    if( needs_first ):
        needs_dots = ( page_current - page_from > step_size + 1 )
        span = "<span class='page'><a href='javascript:void(0)' onclick=\"goto_page('" + str(form_name) + "', '" + str( form_element ) + "', "  + str(page_from) + ")\">"+ str(page_from) +"</a></span>&nbsp;"
        if( needs_dots ):
            span = span + "<span class='page'>...</span>&nbsp;"
        text = text + span
    for i in range(previous,next):
        if i == page_current:
            span="<span class='page'>"+ str(i) + "</span>&nbsp;"
            text = text + span
        else:
            span = "<span class='page'><a href='javascript:void(0)' onclick=\"goto_page('" + str(form_name)  + "', '" + str( form_element ) + "', " + str(i) + ")\">" + str(i) + "</a></span>&nbsp;"
            text = text + span
    if( needs_last ):
         needs_dots = ( page_to - page_current > step_size + 1 )
         span = ""
         if( needs_dots ):
             span = "<span class='page'>...</span>&nbsp;"
         span = span + "<span class='page'><a href='javascript:void(0)' onclick=\"goto_page('" + str(form_name) + "', '" + str( form_element )  + "', " + str(page_to) + ")\">"+ str(page_to) +"</a></span>"
         text = text + span
    return text + "</div>"
        
