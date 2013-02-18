from django.template import Context, RequestContext, loader
from django.http import HttpResponse
import csv
from displaygenome.models import Genome_Stats, Replicon_Stats, Names, Nodes, Jobs, Tax_Stats

def on_request(request):
    t = loader.get_template('download.html')
    c = Context({
        })  
    return HttpResponse(t.render(c))


def genomes(request):
    genomes = Genome_Stats.objects.all().order_by('genome_id')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="genomeatlas_genomes.csv"'

    writer = csv.writer(response)
    writer.writerow(['genome_id', 'modify_date', 'tax_id', 'bioproject_id', 'genome_name', 'score', 'chromosome_count', 'plasmid_count', 'total_bp', 'gene_count', 'gene_density', 'percent_at', 'rrna_count', 'trna_count'])
    for g in genomes:
        name = g.genome_name
        newname = name.replace(',', ' ') # one genome has a comma in its name
        writer.writerow([g.genome_id, g.modify_date, g.tax_id, g.bioproject_id, newname, g.score, g.chromosome_count, g.plasmid_count, g.total_bp, g.gene_count, g.gene_density, g.percent_at, g.rrna_count, g.trna_count])

    return response

def replicons(request):
    replicons = Replicon_Stats.objects.all().order_by('accession')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="genomeatlas_replicons.csv"'

    writer = csv.writer(response)
    writer.writerow(['row_id', 'genome_id', 'accession', 'version', 'replicon_type', 'score', 'gene_density', 'percent_at', 'total_bp', 'gene_count', 'rrna_count', 'trna_count', 'nonstd_bp', 'at_bp', 'contig_count'])
    for r in replicons:
        writer.writerow([r.row_id, r.genome_id, r.accession, r.version, r.replicon_type, r.score, r.gene_density, r.percent_at, r.total_bp, r.gene_count, r.rrna_count, r.trna_count, r.nonstd_bp, r.at_bp, r.contig_count])
    return response



