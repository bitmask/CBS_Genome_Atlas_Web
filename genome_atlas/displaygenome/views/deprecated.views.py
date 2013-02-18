from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from displaygenome.models import Genome_Stats, Replicon_Stats, Names, Nodes, Jobs, Tax_Stats
import datetime
import re
import string


def tax_index(request):
    top_level_phyla = Tax_Stats.objects.extra(where=["tax_id in (28889, 28890, 651137, 57723, 201174, 200783, 67819, 976, 67814, 204428, 74201, 1090, 200795, 200938, 1117, 200930, 1298, 270, 68297, 74152, 65842, 57723, 1239, 32066, 142182, 256845, 40117, 203682, 1224, 203691, 508458, 544448, 200940, 189775, 200918, 74201)"])
    t = loader.get_template('tax/index.html')
    c = Context({
        'phyla': top_level_phyla,
    })
    return HttpResponse(t.render(c))

def tax(request, tax_id):
    if( not tax_id or tax_id == "131567" ):
        return tax_index(request)
    tax_level = Tax_Stats.objects.filter(tax_id__exact = tax_id).exclude(accession__isnull=False)
    
    parent_ids = ""
    top = 0
    ptax_id = tax_id
    
    genome_id = 0
    for row in tax_level: # Should be one
        genome_id = row.genome_id

    while top < 1:
        this = Nodes.objects.using('taxonomy').filter(tax_id__exact = ptax_id)
        for row in this: #only one row since tax_id is the primary key
            print "parent: " + str(row.parent_tax_id)
            # Should perhaps also ignore item 'cellular organisms"? (ID: 131557)
            if row.parent_tax_id == 1: # TODO should match list in above query
                top = 1
                continue; # Ignore empty root node w/ id 1
            if not parent_ids: # Accounts for None case and empty case
                parent_ids = str(row.parent_tax_id)
            else:
                parent_ids = parent_ids + ", " + str(row.parent_tax_id)
            ptax_id = row.parent_tax_id

    parent_level = Tax_Stats.objects.extra(where=["tax_id in (" + parent_ids + ")"]).exclude(accession__isnull=False).order_by('genome_count').reverse()

    #get the children of the request tax_id
    children = Nodes.objects.using('taxonomy').filter(parent_tax_id__exact = tax_id)

    child_ids = ""
    for child in children:
        if not child_ids:
            child_ids = str(child.tax_id)
        else:
            child_ids = child_ids + ", " + str(child.tax_id)
        print "child: " + str(child.tax_id)
    
    is_accession = False
    if not child_ids:
        #child_level = Tax_Stats.objects.filter(tax_id__exact = tax_id).exclude(accession__isnull=True).order_by('accession')
        child_level = Replicon_Stats.objects.filter(genome_id__exact = genome_id).order_by('accession')       
        is_accession = True
    else:
        child_level = Tax_Stats.objects.extra(where=["tax_id in (" + child_ids  + ")"]).exclude(accession__isnull=False).order_by('tax_name')

    t = loader.get_template('tax/index.html')
    c = Context({
        'parents': parent_level,
        'phyla': tax_level,
        'children': child_level,
        'is_accession':is_accession,
    })
    return HttpResponse(t.render(c))




def latest(request):
    latest_genome_list = Genome_Stats.objects.all().order_by("-genome_id")[:10]
    #latest_genome_list = Genome_Stats.objects.filter(modify_date__gt=datetime.date(2012, 01, 10)).order_by("-genome_id") #yyyyddmm
    accession = []
    for genome in latest_genome_list:
        accession.append(Replicon_Stats.objects.filter(genome_id__exact = genome.genome_id))
    genome_list = zip(latest_genome_list, accession)
    t = loader.get_template('genomes/index.html')
    c = Context({
        'latest_genome_list': genome_list,
    })
    return HttpResponse(t.render(c))


def index(request):
    top_level_phyla = Nodes.objects.using('taxonomy').extra(where=["tax_id in (28889, 28890, 651137, 57723, 201174, 200783, 67819, 976, 67814, 204428, 74201, 1090, 200795, 200938, 1117, 200930, 1298, 270, 68297, 74152, 65842, 57723, 1239, 32066, 142182, 256845, 40117, 203682, 1224, 203691, 508458, 544448, 200940, 189775, 200918, 74201)"])
    top_level_phyla_names = Names.objects.using('taxonomy').extra(where=["tax_id in (28889, 28890, 651137, 57723, 201174, 200783, 67819, 976, 67814, 204428, 74201, 1090, 200795, 200938, 1117, 200930 , 1298, 270, 68297, 74152, 65842, 57723, 1239, 32066, 142182, 256845, 40117, 203682, 1224, 203691, 508458, 544448, 200940, 189775, 200918, 74201)"]).filter(name_class__exact = "scientific name")


    phyla = zip(top_level_phyla, top_level_phyla_names)

    parent_tax_id = "" 

    t = loader.get_template('genomes/index.html')
    c = Context({
        'phyla': phyla,
        'parent_tax_id': parent_tax_id,
    })
    return HttpResponse(t.render(c))

def phylum(request, phylum_id):
    # Display a single phyla and it's details
    t = loader.get_template('phyla/index.html')
    phyla_no = Nodes.objects.using('taxonomy').filter(tax_id__exact = phylum_id)
    phyla_na = Names.objects.using('taxonomy').filter(tax_id__exact = phylum_id)

    c = Context({
        'phyla': zip(phyla_no, phyla_na),
        'parent_id': phyla_no[0].parent_tax_id
    })
    return HttpResponse(t.render(c))

def parent_phylum(request, parent_id):
    # Display the children of the given phyla
    t = loader.get_template('phyla/index.html')
    phyla_no = Nodes.objects.using('taxonomy').filter(parent_tax_id__exact = parent_id)
    phyla_na = Names.objects.using('taxonomy').filter(name_class__exact = "scientific name").extra(where=["tax_id in (select tax_id from nodes where parent_tax_id = %s)"], params=[parent_id]).order_by("-name_txt")
    phyla = zip(phyla_no, phyla_na)


    phyla_tax_id = "";
    for p in (phyla_no):
        if len(phyla_tax_id) == 0:
            phyla_tax_id = str(p.tax_id)
        else:
            phyla_tax_id = phyla_tax_id + ", " + str(p.tax_id)
    
    genome_list = Genome_Stats.objects.extra(where=["tax_id in (" + phyla_tax_id + ")"])
    accession = []
    for genome in genome_list:
        accession.append(Replicon_Stats.objects.filter(genome_id__exact = genome.genome_id))
    phyla_genome_list = zip(genome_list, accession)

    c = Context({
        'phyla': phyla,
        'parent_id': parent_id,
        'genome_list': phyla_genome_list,
    })
    return HttpResponse(t.render(c))

def detail(request, genome_id):
    #return HttpResponse("this is id " + str(genome_id));

    genome = Genome_Stats.objects.filter(genome_id__exact = genome_id)
    replicons = Replicon_Stats.objects.filter(genome_id__exact = genome_id)
    t = loader.get_template('genomes/single.html')
    c = Context({
        'genome': genome,
        'replicons': replicons,
    })
    return HttpResponse(t.render(c))
  
def accession(request, accession):
    genome_id = Replicon_Stats.objects.filter(accession__exact = accession)
    print "genome_id " + str(genome_id[0].genome_id)
    return detail(request, genome_id[0].genome_id)

def search(request):
    #term could be a name, accession number, tax id
    term = request.GET.get('q', '')
    thing = ""
    if not term:
        return tax_index(request)
    if re.match(r'[A-Z]{2}[0-9]+', term, re.I):
        thing = Replicon_Stats.objects.filter(accession__exact = term)
        if(thing and thing[0].accession):
            print "accession search: " + str(thing[0].accession)
            return accession(request, thing[0].accession)
    elif re.match(r'[0-9]+', term):
        thing = Nodes.objects.using('taxonomy').filter(tax_id__exact = term)
        if(thing and thing[0].tax_id):
            print "Tax ID search: " + str(thing[0].tax_id)
            return tax(request, thing[0].tax_id)
        else:
            return HttpResponse("No results found")
    else:
        search_results = Names.objects.using('taxonomy').filter(name_txt__icontains = term).values('tax_id').distinct()
        if( search_results ):
            tax_ids = [ str( r['tax_id'] ) for r in search_results.values() ]
            taxons = Tax_Stats.objects.extra(where=["tax_id in (" + string.join(tax_ids, ',') + ")", "tax_name is not null"])
            
            #if not taxons:
            #return HttpResponse( "No results found for query: " + term )

            t = loader.get_template('tax/index.html')
            c = RequestContext({
                'search_term':term,
                'result_count': len(taxons),
                'parents':'',
                'phyla':taxons,
                'children':'',
            })
            return HttpResponse(t.render(c))
        else:
             return HttpResponse( "No results found for query: " + term )
    return HttpResponse("searched for " + term)

def admin(request):
    failed_jobs = Jobs.objects.filter(step_status__exact = 'Failure').order_by("-job_start_time")[:10]
    successful_jobs = Jobs.objects.filter(step_status__exact = 'Success').order_by("-job_start_time")[:10]
    t = loader.get_template('admin/index.html')
    c = Context({
        'failed_jobs': failed_jobs,
        'successful_jobs': successful_jobs,
    })
    return HttpResponse(t.render(c))

def frontpage(request):
    return index(request)

def genome_new(request):
    """
    This is kind of like NCBI's genome/browse page -- shows all genomes in the database and allows for
    some basic search functionality. Allows sorting in all columns. Tables can use the sorting function
    by calling the table_tools templates.
    """
    # Load the genome browsing form
    from forms import GenomeBrowseForm
 
    q = request.GET.get('q', None)
    qtype = request.GET.get('qtype', None)
    # Manually safety check -- since q and qtype are not forms in themselves
    # TODO: Make q and qtype into forms... will better fit the design -- that this requires formsets instead though...
    if( str(q)=="None" ):
        q = None
        qtype = None
    if( str(qtype) not in ["AN","TD","BP"]):
        qtype = "GN"

    if(request.method == 'POST'):
        form_data=GenomeBrowseForm(request.POST)
    else:
        initial_data={'current_page':1,
                      'order_by':'genome_name',
                      'order_dir':'ASC',
                      'per_page':10}
        form_data=GenomeBrowseForm(initial_data)

    if form_data.is_valid():
        current_page=form_data.cleaned_data['current_page']
        order_by=form_data.cleaned_data['order_by']
        order_dir=form_data.cleaned_data['order_dir']
        per_page=int(form_data.cleaned_data['per_page'])
    else:
        current_page=int(1)
        order_by='genome_name'
        order_dir='ASC'
        per_page=int(10)
    
    order = order_by
    if order_dir == 'DSC':
        order = '-' + order
    
    genomes = None
    
    # If no query, just return the list of all genomes
    if not q :
        number_of_genomes = Genome_Stats.objects.exclude(genome_name=None).count()
        genomes = Genome_Stats.objects.exclude(genome_name=None).order_by(order)
    else:
    # Otherwise, search by:
        q = str(q)
        qtype = str(qtype)
        if qtype == "GN": # Search by Genome Name
            qtype = "Genome Name"
            search_results = Names.objects.using('taxonomy').filter(name_txt__icontains = q).values('tax_id').distinct()
            if( search_results ):
                tax_ids = [ str( r['tax_id'] ) for r in search_results.values() ]
                genomes = Genome_Stats.objects.extra(where=["tax_id in (" + string.join(tax_ids, ',') + ")"]).exclude(genome_name=None).order_by(order)
                number_of_genomes = genomes.count()
            else:
                number_of_genomes=0
        elif qtype == "AN": # Search by Accession Number
            qtype = "Accession Number"
            search_results = Replicon_Stats.objects.filter(accession_icontains=q).values('genome_id').distinct()
            if( search_results ):
                genome_ids = [ str( r['genome_id'] ) for r in search_results.values() ]
                genomes = Genome_Stats.objects.extra(where=["genome_id in (" + string.join(genome_ids, ',') + ")"]).exclude(genome_name=None).order_by(order)
                number_of_genomes = genomes.count()
            else:
                number_of_genomes = 0
        elif qtype == "TD": # Search by Tax ID
            qtype = "Taxonomy ID"
            try:
               tax=int(q)
               genomes = [ Genome_Stats.objects.get(tax_id=tax) ];
               number_of_genomes=1
            except Exception, e:
               number_of_genomes=0
        elif qtype == "BP": # Search by Bioproject ID
            qtype = "Bioproject ID"
            try:
                bp = int(q)
                genomes = [ Genome_Stats.objects.get(bioproject_id=bp) ]
                number_of_genomes=1
            except Exception, e:
                number_of_genomes=0
        else:
            number_of_genomes=0

    number_of_pages = (number_of_genomes/per_page) + 1
    if current_page > number_of_pages:
        current_page = number_of_pages

    first_index = (current_page-1) * per_page
    if( genomes ):
        genomes_slice = genomes[first_index : first_index + per_page]
    else:
        genomes_slice = None

    t = loader.get_template('genomes_new/index.html')
    c = RequestContext(request, {
                 'search_term':q,
                 'search_type':qtype,
                 'start_index':first_index + 1,
                 'end_index': min(first_index + per_page, number_of_genomes),
                 'actual_current':current_page,
                 'genome_slice':genomes_slice,
                 'genome_count':number_of_genomes,
                 'form_data':form_data,
                 'number_of_pages':number_of_pages,
               })
    return HttpResponse( t.render(c) )

def genome_new_single(request, genome_id):
    # Load the genome browsing form
    from forms import GenomeSingleForm

    try:
        genome = Genome_Stats.objects.get(genome_id=genome_id)
    except Exception:
        #TODO: NO RESULTS FOUND
        return HttpResponse("Genome not found")
     
    ## This block is /exactly/ the same code as before
    # consider rewriting this into a function def instead
    # also, things like order_by and per_page should possibly
    # be session variables and not request variables . . .

    if(request.method == 'POST'):
        form_data=GenomeSingleForm(request.POST)
    else:
        initial_data={'current_page':1,
                      'order_by':'accession',
                      'order_dir':'ASC',
                      'per_page':10}
        form_data=GenomeSingleForm(initial_data)

    if form_data.is_valid():
        current_page=form_data.cleaned_data['current_page']
        order_by=form_data.cleaned_data['order_by']
        order_dir=form_data.cleaned_data['order_dir']
        per_page=int(form_data.cleaned_data['per_page'])
    else:
        current_page=int(1)
        order_by='genome_name'
        order_dir='ASC'
        per_page=int(10)
    
    order = order_by
    if order_dir == 'DSC':
        order = '-' + order
    
    accessions = Replicon_Stats.objects.filter(genome_id=genome_id).order_by(order)
    number_of_accessions = accessions.count()

    # Same code again... session variablez plz
    number_of_pages = (number_of_accessions / per_page) + 1
    if( number_of_pages < current_page ):
        current_page = number_of_pages

    first_index = (current_page-1) * per_page
    if( accessions ):
        accession_slice = accessions[first_index : first_index + per_page]
    else:
        accession_slice = None

    t = loader.get_template('genomes_new/single.html')
    c = RequestContext(request, {
                 'genome':[ genome ],
                 'start_index':first_index + 1,
                 'end_index': min(first_index + per_page, number_of_accessions),
                 'actual_current':current_page,
                 'accession_slice':accession_slice,
                 'accession_count':number_of_accessions,
                 'form_data':form_data,
                 'number_of_pages':number_of_pages,
               })
    return HttpResponse( t.render(c) )

