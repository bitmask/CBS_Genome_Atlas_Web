from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from displaygenome.models import Genome_Stats, Replicon_Stats, Names, Nodes, Jobs, Tax_Stats
from django import forms
import datetime
import re
import string

"""
This view is responsible for handling the search requests.

Searches show:
--Multiple Matches:
   A list of the taxonomies for this match
--Single Match:
   Go to browse for this match
--No Match:
   Display a message about no matches found.

When a user clicks a taxonomy in the result-list, it should take them to
the browse page for that tax_id.
"""

class SearchResultForm(forms.Form):
# These fields are searchable for taxonomy nodes
    
    per_page_selection = (
                           (10,'10'),
                           (25,'25'),
                           (50,'50'),
                           (100,'100')
                         )

    order_dir_selection = (('ASC', 'Ascending'), ('DSC', 'Descending'))

    order_by_gen_selection=(
                             ('release_date', 'Release Date'),
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
                           )
    
    per_page_tax=forms.ChoiceField(choices=per_page_selection, label='Results per page')
    order_by_tax=forms.ChoiceField(choices=order_by_tax_selection, label='Order by')
    order_dir_tax=forms.ChoiceField(choices=order_dir_selection, label='Direction')
    current_page_tax=forms.IntegerField(min_value=1, label='Page number')
    per_page_tax.widget.attrs["onchange"]="this.form.submit()"
    per_page_gen=forms.ChoiceField(choices=per_page_selection, label='Results per page')
    order_by_gen=forms.ChoiceField(choices=order_by_gen_selection, label='Order by')
    order_dir_gen=forms.ChoiceField(choices=order_dir_selection, label='Direction')
    current_page_gen=forms.IntegerField(min_value=1, label='Page number')
    per_page_gen.widget.attrs["onchange"]="this.form.submit()"

regex_accession = re.compile(r'^[a-zA-Z]{1,4}[0-9]+$')
regex_accession_version = re.compile(r'^[a-zA-Z]{1,4}[0-9]+[\-\_\.][0-9]+$')
regex_accession_split = re.compile(r'[\-\_\.]')
regex_tax_or_bioproject = re.compile(r'^[0-9]+$')

query_types = [
                 'AN', # Accession
                 'TN', # Tax Name
                 'TI', # Tax ID
                 'BP', # Bioproject ID
                 'TIBP',
              ]

browse_link = "/browse/%i"

def on_request(request):
    """
    This is called by DJANGO when a request is made.
      1: Determine query type
      2: Make query
      3: Display Result
    """
    query = request.GET.get('q');
    query_type = request.GET.get('qt')
    
    if( not query ):
        pass # Change this to return something special?

    if( not query_type ):
        # Guess query type:
        if( regex_accession.match(query) or
                regex_accession_version.match(query) ):
            # Accession Number Query
            query_type='AN'
        elif( regex_tax_or_bioproject.match(query) ):
            # Bioproject or Taxonomy Query
            query_type='TIBP'
        else:
            # Taxon ID
            query_type='TN'
    if( query_type == 'AN' ):
        # Make accession query
        av = regex_accession_split.split(query, 2)
        if( len(av) == 1 ):
            accession = av[0]
            version = None
        else:
            accession = av[0]
            version = av[1]
            query = accession
        tax_nodes = find_by_accession( accession, version )
    elif( query_type == 'TN' ):
        tax_nodes = find_by_genome_name( query )
    elif( query_type == 'TI' ):
        tax_nodes = find_by_tax_id( query )
    elif( query_type == 'BP' ):
        tax_nodes = find_by_bioproject_id( query )
    elif( query_type == 'TIBP' ):
        tax_nodes = find_by_tax_id( query )
        if( not tax_nodes ):
           tax_nodes = find_by_bioproject_id( query )
    
    if (tax_nodes is None or tax_nodes.count() == 0):
        # No results found for search
        t = loader.get_template("search_error.html")
        ct = Context({
                 'search_type':query_type,
                 'search_term':query,
        })
        return HttpResponse(t.render(ct))
    if( tax_nodes.count() == 1 ):
        # One result found -- foward to genome page
        return HttpResponseRedirect( browse_link % tax_nodes[0].tax_id )
    else:
        # Multiple results found -- handle display of multiple results
        return display_results( request, tax_nodes )

def find_by_accession( accession, version=None ):
    """
    Find a taxonomy number by looking for the requested accession number. Return the result(s)
    -- There should generally be either zero or one result
    """
    if( accession and version ):
        replicon = Replicon_Stats.objects.filter( accession=accession.upper(), version=version )
    else:
        replicon = Replicon_Stats.objects.filter( accession=accession.upper() )
    genome = Genome_Stats.objects.filter( genome_id = replicon[0].genome_id )
    return Tax_Stats.objects.filter( tax_id = genome[0].tax_id )



def find_by_tax_id( tax_id ):
    """
    Find a tax node using a given tax_id. Return the node
    """
    # Should be either one or zero results (no guarantees...)
    return Tax_Stats.objects.filter(tax_id=tax_id)


def find_by_bioproject_id( bioproject_id ):
    """
    Find a tax node by a given bioproject_id. Return the node
    """
    # Find the nodes with that bioproject id
    # Should be either one or zero results (no guarantees...)
    genomes = Genome_Stats.objects.filter(bioproject_id=bioproject_id)
    if genomes:
        return Tax_Stats.objects.filter( tax_id = genomes[0].tax_id )
    else:
        return None


def find_by_genome_name( genome_name) :
    """
    Find taxa by a given genome name. This search looks for the name string within the
    NCBItax database (names table). Tax_IDs retrieved from the NCBItax database are then
    be cross referenced against our tax_stats. Return found results
    """
    # Search our NCBI TAX database for distinct taxa given this name
    matching_taxons = Names.objects.using("taxonomy").filter(name_txt__icontains=genome_name).values('tax_id').distinct()
    # If matching taxa are found, try and find them in our data as well
    if( matching_taxons ):
        search_string = string.join( ( str(t['tax_id']) for t in matching_taxons), "," )
        nodes = Tax_Stats.objects.all().extra(where=[("tax_id IN (%s)" % (search_string))] )
        return nodes
    return None

def display_results( request, taxons ):
    """
    Display the results when there are more than one tax_node to display. First, look up matching genomes.
    """
    tax_ids = taxons.values('tax_id')
    search_string = string.join( ( str(t['tax_id']) for t in tax_ids), "," )
    genomes = Genome_Stats.objects.all().extra(where=[("tax_id IN (%s)" % search_string)])
    taxon_count = taxons.count()
    genome_count = genomes.count()

    # Make/Get POST data for display:
    if(request.method == 'POST'):
        form_data=SearchResultForm(request.POST)
    else:
        # No post data, load initial instead
        initial_data={
                       'current_page_gen':1,
                       'current_page_tax':1,
                       'order_by_tax':'tax_name',
                       'order_by_gen':'genome_name',
                       'order_dir_tax':'ASC',
                       'order_dir_gen':'ASC',
                       'per_page_gen':10,
                       'per_page_tax':10,
                     }
        form_data=SearchResultForm(initial_data)

    # Validate the form
    if form_data.is_valid():
        # Tax table ordering
        current_page_tax = form_data.cleaned_data['current_page_tax']
        order_by_tax = form_data.cleaned_data['order_by_tax']
        order_dir_tax = form_data.cleaned_data['order_dir_tax']
        per_page_tax = int(form_data.cleaned_data['per_page_tax'])

        # Genome table ordering/pages
        current_page_gen=form_data.cleaned_data['current_page_gen']
        order_by_gen=form_data.cleaned_data['order_by_gen']
        order_dir_gen=form_data.cleaned_data['order_dir_gen']
        per_page_gen=int(form_data.cleaned_data['per_page_gen'])
    else:
        # Need to handle this case better...
        return HttpResponse( str(form_data.errors) )

    order_gen = order_by_gen
    if order_dir_gen == 'DSC':
        order_gen = '-' + order_gen

    order_tax = order_by_tax
    if order_dir_tax == 'DSC':
        order_tax = '-' + order_tax

    genomes = genomes.order_by( order_gen )
    taxons = taxons.order_by( order_tax )

    # Calculate the number of pages and fix the current page if needed
    number_of_pages_gen = (genome_count / per_page_gen) + 1
    current_page_gen = min( number_of_pages_gen, current_page_gen )
    number_of_pages_tax = (taxon_count / per_page_tax) + 1
    current_page_tax = min( number_of_pages_tax, current_page_tax )


    # The index of the first genome in the list
    first_index_gen = (current_page_gen-1) * per_page_gen
    if( genomes ):
        # A slice of the genomes we have
        genome_slice = genomes[first_index_gen : first_index_gen + per_page_gen]
    else:
        # No genomes were found... empty slice
        genome_slice = []
    size_gen = min( per_page_gen, genome_count - first_index_gen )
    last_index_gen = first_index_gen + size_gen

    # The index of the first taxon in the list
    first_index_tax = (current_page_tax-1) * per_page_tax
    if( taxons ):
        # A slice of the taxon we have
        taxon_slice = taxons[first_index_tax : first_index_tax + per_page_tax]
    else:
        # No taxons were found... empty slice (THIS SHOULD NOT HAPPEN!)
        taxon_slice = []
    size_tax = min( per_page_tax, taxon_count - first_index_tax )
    last_index_tax = first_index_tax + size_tax
    
    # Get the index template and build the context
    t = loader.get_template("search.html")
    c = RequestContext(request, {
      'taxon_slice': taxon_slice,
      'taxon_slice_first': first_index_tax,
      'taxon_slice_count': size_tax,
      'taxon_slice_last': last_index_tax,
      'taxon_total_count':taxon_count,
      
      'genome_slice':genome_slice,
      'genome_slice_first': first_index_gen,
      'genome_slice_count': size_gen,
      'genome_slice_last': last_index_gen,
      'genome_total_count': genome_count,

      'form_data': form_data,

      'forced_current_page_tax':current_page_tax,
      'number_of_pages_tax': number_of_pages_tax,
      'forced_current_page_gen':current_page_gen,
      'number_of_pages_gen': number_of_pages_gen,
    })
     
    return HttpResponse(t.render(c))


