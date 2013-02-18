from django.template import Context, RequestContext, loader
from django import forms
from django.http import HttpResponse
from displaygenome.models import Genome_Stats, Replicon_Stats, Names, Nodes, Jobs, Tax_Stats
from displaygenome.forms import TaxonomyForm
import string


"""
This view should display the main index page.

The main index page consists of the base phyla list given by Dave. Below this list,
there should be the list of genomes as current. Header should show links (using
#labels to these two sections).

"""

top_level_phyla_string = '28889, 28890, 651137, 57723, 201174, 200783, 67819, 976, 67814, 204428, 74201, 1090, 200795, 200938, 1117, 200930, 1298, 270, 68297, 74152, 65842, 57723, 1239, 32066, 142182, 256845, 40117, 203682, 1224, 203691, 508458, 544448, 200940, 189775, 200918, 74201'

class IndexForm(forms.Form):
# These fields are searchable for taxonomy nodes
    
    per_page_selection = (
                           (10,'10'),
                           (25,'25'),
                           (50,'50'),
                           (100,'100')
                         )

    order_dir_selection = (('ASC', 'Ascending'), ('DSC', 'Descending'))
    order_by_gen_selection=(
                             ('modify_date', 'Modify Date'),
                             ('tax_id', 'Taxonomy ID'),
                             ('bioproject_id', 'Bioproject ID'),
                             ('genome_name', 'Genome Name'),
                             ('score','Genome Score'),
                             ('chromosome_count','Chromosomes'),
                             ('plasmid_count','Plasmids'),
                             ('percent_at','Percent AT'),
                             ('total_bp','Total Length (bp)'),
                             ('gene_count','Gene Count'),
                             ('gene_density','Gene Density'),
                             ('rrna_count','rRNA Count'),
                             ('trna_count','tRNA Count'),
                       )

    order_by_tax_selection=(
                              ('tax_id', 'Taxonomy ID'),
                              ('genome_count','Genomes'),
                              ('tax_name','Taxonomic Name'),
                              ('score', 'Score'),
                              ('percent_at', 'Percent AT'),
                              ('gene_density', 'Gene Density'),
                           )
    
    """For the top level taxonomy, we only offer ordering, no pages..."""
    order_by_tax=forms.ChoiceField(choices=order_by_tax_selection, label='Order by')
    order_dir_tax=forms.ChoiceField(choices=order_dir_selection, label='Direction')
    per_page_gen=forms.ChoiceField(choices=per_page_selection, label='Results per page')
    order_by_gen=forms.ChoiceField(choices=order_by_gen_selection, label='Order by')
    order_dir_gen=forms.ChoiceField(choices=order_dir_selection, label='Direction')
    current_page_gen=forms.IntegerField(min_value=1, label='Page number')
    per_page_gen.widget.attrs["onchange"]="this.form.submit()"

def on_request(request):
    # Make the formset with 2 forms (one for the taxonomies, one for genomes
    if(request.method == 'POST'):
        form_data=IndexForm(request.POST)
    else:
        # No post data, load initial instead
        initial_data={
                       'current_page_gen':1,
                       'order_by_tax':'tax_name',
                       'order_by_gen':'modify_date',
                       'order_dir_tax':'ASC',
                       'order_dir_gen':'DSC',
                       'per_page_gen':10,
                     }
        form_data=IndexForm(initial_data)

    # Validate the form
    if form_data.is_valid():
        # Tax table ordering
        order_by_tax = form_data.cleaned_data['order_by_tax']
        order_dir_tax = form_data.cleaned_data['order_dir_tax']
        
        # Genome table ordering/pages
        current_page=form_data.cleaned_data['current_page_gen']
        order_by=form_data.cleaned_data['order_by_gen']
        order_dir=form_data.cleaned_data['order_dir_gen']
        per_page=int(form_data.cleaned_data['per_page_gen'])
    else:
        return HttpResponse( form_data.errors )
        order_by_tax = 'genome_name'
        order_dir_tax = 'ASC'
        current_page=int(1)
        order_by='genome_name'
        order_dir='ASC'
        per_page=int(10)
    
    # Convert so we can use in our query
    order = order_by
    if order_dir == 'DSC':
        order = '-' + order
    # Convert so we can use in our query
    order_tax = order_by_tax
    if order_dir_tax == 'DSC':
        order_tax = '-' + order_tax

    # Get the top level phyla from the database:
    taxon = Tax_Stats.objects.extra(where=[ "tax_id in (" + top_level_phyla_string + ")" ]).order_by(order_tax)
    taxon_count = taxon.count()

    # Get all the genomes from the database:
    genome = Genome_Stats.objects.all().exclude(genome_name=None).order_by(order)
    genome_count = genome.count()

    # Calculate the number of pages and fix the current page if needed
    number_of_pages = (genome_count/per_page) + 1
    current_page = min( number_of_pages, current_page )

    # The index of the first genome in the list
    first_index = (current_page-1) * per_page
    if( genome ):
        # A slice of the genomes we have
        genome_slice = genome[first_index : first_index + per_page]
    else:
        # No genomes were found... empty slice
        genome_slice = []
    
    # Get the index template and build the context
    t = loader.get_template("index.html")
    c = RequestContext(request, {
      'taxon': taxon,
      'taxon_count':taxon_count,
      'genome_slice':genome_slice,
      'genome_slice_first': first_index,
      'genome_slice_count': min( per_page, genome_count - first_index ),
      'genome_total_count': genome_count,
      'form_data': form_data,
      'forced_current_page_gen':current_page,
      'number_of_pages_gen': number_of_pages,
    })
     
    return HttpResponse(t.render(c))
    
