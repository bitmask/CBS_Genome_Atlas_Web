from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django import forms
from displaygenome.models import Genome_Stats, Replicon_Stats, Names, Nodes, Jobs, Tax_Stats
import datetime
import re
import string

"""
This view is responsible for displaying parents, nodes, and children. Each level
of the tree should contain links to their levels. Clicking on a current node will
have no real effect at the moment, as it would bring you to the same page. This may
change for actual genomes though, as we might want a separate page for the specific
genome statistics.

parents:
A list of the parent taxonomy, with links back to those levels
-- Display as a list, or as some sort of tree?

nodes:
The current node, this could either be a taxonomy node, or a genome node
-- Use related data

children:
Children are only present on taxonomy nodes. These children may be genomes or
taxonomy nodes; but only taxonomy style nodes will be shown. (The genome case
will happen when they click the link and end up at that node instead.
"""

class BrowseForm(forms.Form):

    per_page_selection = ( 
                           (10,'10'),
                           (25,'25'),
                           (50,'50'),
                           (100,'100')
                         )

    order_dir_selection = (('ASC', 'Ascending'), ('DSC', 'Descending'))

    order_by_selection=( 
                             ('release_date', 'Release Date'),
                             ('tax_id', 'Taxonomy ID'),
                             ('tax_name', 'Tax Name'),
                             ('score','Genome Score'),
                             ('genome_count','Genome Count'),
                             ('percent_at','Percent AT'),
                             ('gene_density','Gene Density'),
                       )

    per_page=forms.ChoiceField(choices=per_page_selection, label='Results per page')
    order_by=forms.ChoiceField(choices=order_by_selection, label='Order by')
    order_dir=forms.ChoiceField(choices=order_dir_selection, label='Direction')
    current_page=forms.IntegerField(min_value=1, label='Page number')

    per_page.widget.attrs["onchange"]="this.form.submit()"


# Will be called as a result of urls.py
def on_request(request, tax_id):

    if(request.method == 'POST'):
        form_data=BrowseForm(request.POST)
    else:
        # No post data, load initial instead
        initial_data={
                       'current_page':1,
                       'order_by':'tax_name',
                       'order_dir':'ASC',
                       'per_page':10,
                     }   
        current_page=int(1)
        form_data=BrowseForm(initial_data)


    # Validate the form
    if form_data.is_valid():
        current_page=form_data.cleaned_data['current_page']
        per_page=int(form_data.cleaned_data['per_page'])
        order_by = form_data.cleaned_data['order_by']
        order_dir = form_data.cleaned_data['order_dir']
    else:
        return HttpResponse( form_data.errors )
        current_page=int(1)
        per_page=int(10)


    # Fetch the current level
    tax_level = Tax_Stats.objects.get(tax_id=tax_id)
    
    # While not at the top
    ptax_id = tax_id;
    not_top = True 
    parent_ids = ''
    while not_top:
        # Find this node
        parent = Nodes.objects.using('taxonomy').get(tax_id=ptax_id)
        # Should perhaps also ignore item 'cellular organisms"? (ID: 131557)
        if parent.parent_tax_id == 1 or parent.parent_tax_id == 131557:
            break
        if not parent_ids: # Accounts for None case and empty case
            parent_ids = str(parent.parent_tax_id)
        else:
            parent_ids = parent_ids + ", " + str(parent.parent_tax_id)
            ptax_id = parent.parent_tax_id

    parent_level = Tax_Stats.objects.extra(where=["tax_id in (" + parent_ids + ")"]).order_by('genome_count').reverse()

    #get the children of the request tax_id
    children = Nodes.objects.using('taxonomy').filter(parent_tax_id__exact = tax_id)

    child_ids = ""
    for child in children:
        if not child_ids:
            child_ids = str(child.tax_id)
        else:
            child_ids = child_ids + ", " + str(child.tax_id)
    
    is_accession = False
    if not child_ids:
        # then the current node appears in the genome table
        this = Genome_Stats.objects.filter(tax_id__exact = tax_level.tax_id)
        for t in this:
            genome_level = t
        if (genome_level):
            child_level = Replicon_Stats.objects.filter(genome_id__exact = genome_level.genome_id).order_by('accession')
            number_of_pages = (child_level.count() / per_page) + 1
            current_page = min(number_of_pages, current_page)
            first_index = (current_page-1) * per_page
            tax_level = genome_level # use the genome objects, not the tax objects
            is_accession = True
        else:
            print "uh oh, no genome with tax_id = " + tax_level.tax_id + " in genome table where one should exist" #XXX error messaging?
    else:
        if order_dir == 'DSC':
            order_by = '-' + order_by
        child_level = Tax_Stats.objects.extra(where=["tax_id in (" + child_ids  + ")"]).order_by(order_by)
        number_of_pages = (child_level.count() / per_page) + 1
        current_page = min( number_of_pages, current_page )
        first_index = (current_page-1) * per_page
        child_slice = child_level[first_index : first_index + per_page]
        child_level = child_slice

    t = loader.get_template('browse.html')
    c = RequestContext(request, {
        'parents': parent_level,
        'current_node': tax_level,
        'children': child_level,
        'is_accession': is_accession,
        'form_data': form_data,
        'number_of_pages': number_of_pages,
        'forced_current_page': current_page,
    })
    return HttpResponse(t.render(c))

