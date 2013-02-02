from django.db import models
from django.db.models.base import ModelBase
import math

class Tax_Stats(models.Model):
    row_id = models.IntegerField(primary_key=True)
    tax_id = models.IntegerField()
    bioproject_id = models.IntegerField()
    genome_name = models.CharField(max_length=200)
    score_sum = models.FloatField()
    score_nonstd_sum = models.FloatField()
    score_contig_sum = models.FloatField()
    chromosome_count = models.IntegerField()
    plasmid_count = models.IntegerField()
    replicon_count = models.IntegerField()
    contig_count = models.IntegerField()
    total_bp = models.BigIntegerField()
    nonstd_bp = models.BigIntegerField()
    gene_count = models.IntegerField()
    at_bp = models.BigIntegerField()
    modify_date = models.DateField()
    trna_count = models.BigIntegerField()
    rrna_count = models.BigIntegerField()
    genome_id = models.IntegerField()
    accession = models.CharField(max_length=20)
    version = models.IntegerField()
    genome_count = models.IntegerField()
    tax_name = models.CharField(max_length=200)

    def _get_percent_at(self):
        "Returns compound of at_bp and total_bp"
        return "{0:2.2f}".format(float(self.at_bp * 100L)/float(self.total_bp))
    percent_at = property(_get_percent_at)

    def _get_gene_density(self):
        "Returns gene density as genes per Kb"
        if(self.gene_count and self.total_bp):
            return "{0:2.2f}".format(float(1000L*self.gene_count)/float(self.total_bp))
        else:
            return "0.00"
    gene_density = property(_get_gene_density)

    def _get_score(self):
        """
        Returns genome score:
        greatest(0.1, 1-0.2*ceiling((1000000*greatest(0, (coalesce(contig.contig_count, 0) - count(replicon.accession)))/sum(stat_size_bp))/25)) as score_contig,
        greatest (0.1, 1 - (1- greatest (0.1, 1+.1*(0-ceiling(100*sum(stat_number_nonstd_bases)/sum(stat_size_bp)))) ) - (1 - greatest(0.1, 1-0.2*ceiling((1000000*greatest(0, (coalesce(contig.contig_count, 0) - count(replicon.accession)))/sum(stat_size_bp))/25)))) as score
        """
        my_contig_count = float(self.contig_count) if self.contig_count else 0
        my_percent_nonstd = float(self.nonstd_bp * 100)/float(self.total_bp)
        my_replicon_count = float(self.replicon_count) if self.replicon_count else 0
        my_total_bp = float(self.total_bp) if self.total_bp else 0
        error_nonstd = .1* math.ceil(my_percent_nonstd)
        contigs_per_replicon = my_contig_count / my_replicon_count
        error_contigs = .2 * math.ceil( 1000000 * contigs_per_replicon / my_total_bp) / 25
        score = max(0.1, 1 - min(1, error_nonstd) - min(1, error_contigs))
        return "{0:1.1f}".format(score)

    score = property(_get_score)

class Genome_Stats(models.Model):
    genome_id = models.IntegerField(primary_key=True)
    tax_id = models.IntegerField()
    bioproject_id = models.IntegerField()
    genome_name = models.CharField(max_length=200)
    score = models.FloatField()
    chromosome_count = models.IntegerField()
    plasmid_count = models.IntegerField()
    total_bp = models.IntegerField()
    gene_count = models.IntegerField()
    gene_density = models.FloatField()
    percent_at = models.FloatField()
    modify_date = models.DateField()
    trna_count = models.BigIntegerField()
    rrna_count = models.BigIntegerField()
    accessions = models.CharField(max_length=1000)
    percent_nonstd_bp = models.FloatField()
    nonstd_bp = models.IntegerField()
    contig_count = models.FloatField()
    
    def _get_accession_list(self):
        return str(self.accessions).split(" ")

    accession_list = property(_get_accession_list)
    
    def _get_percent_non_std(self):
        return int(math.ceil(self.nonstd_bp/self.total_bp))

    percent_nonstd_bp2 = property(_get_percent_non_std)

    def __unicode__(self):
        return self.genome_id

class Replicon_Stats(models.Model):
    
    replicon_id = models.IntegerField(primary_key=True)
    accession = models.CharField(max_length=200)
    version = models.IntegerField()
    genome = models.ForeignKey(Genome_Stats)
    replicon_type = models.CharField(max_length=200)
    stat_size_bp = models.IntegerField()
    stat_number_nonstd_bases = models.IntegerField()
    stat_number_of_contigs = models.IntegerField()
    gene_density = models.FloatField()
    stat_perc_at = models.FloatField()
    stat_number_of_genes = models.IntegerField()

    rrna_count_accession = models.IntegerField()
    trna_count_accession = models.IntegerField()

    def _get_score(self):
        """
        Returns genome score:
        greatest(0.1, 1-0.2*ceiling((1000000*greatest(0, (coalesce(contig.contig_count, 0) - count(replicon.accession)))/sum(stat_size_bp))/25)) as score_contig,
        greatest (0.1, 1 - (1- greatest (0.1, 1+.1*(0-ceiling(100*sum(stat_number_nonstd_bases)/sum(stat_size_bp)))) ) - (1 - greatest(0.1, 1-0.2*ceiling((1000000*greatest(0, (coalesce(contig.contig_count, 0) - count(replicon.accession)))/sum(stat_size_bp))/25)))) as score
        """
        my_contig_count = float(self.stat_number_of_contigs) if self.stat_number_of_contigs else 0
        my_percent_nonstd = float(self.stat_number_nonstd_bases * 100)/float(self.stat_size_bp)
        #my_replicon_count = float(self.replicon_count) if self.replicon_count else 0
        my_total_bp = float(self.stat_size_bp) if self.stat_size_bp else 0
        error_nonstd = .1 * math.ceil( my_percent_nonstd )
        #contigs_per_replicon = my_contig_count / my_replicon_count
        error_contigs = .2 * math.ceil( 1000000 * my_contig_count / my_total_bp ) / 25
        score = max(0.1, 1 - min(1, error_nonstd) - min(1, error_contigs))
        return "{0:1.1f}".format(score)

    score = property(_get_score)

    def __unicode__(self):
        return self.accession

class tRNA(models.Model):
    id = models.IntegerField(primary_key=True)
    accession = models.CharField(max_length=200)
    version = models.IntegerField()
    start_location = models.IntegerField()
    end_location = models.IntegerField()
    complementary_strand = models.CharField(max_length=3)
    amino_acid = models.CharField(max_length=3)
    anti_codon = models.CharField(max_length=3)
    sequence = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.accession

class rRNA(models.Model):
    id = models.IntegerField(primary_key=True)
    accession = models.CharField(max_length=200)
    version = models.IntegerField()
    start_location = models.IntegerField()
    end_location = models.IntegerField();
    complementary_strand = models.CharField(max_length=3)
    molecule = models.CharField(max_length=3)
    score = models.IntegerField()
    sequence = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.accession


# for taxonomy databases

BOOLEAN = ( (0, 'No'), (1, 'Yes'))
RANKENUM =('class','family','forma','genus','infraclass','infraorder','kingdom','no rank','order','parvorder','phylum','species','species group','species subgroup','subclass','subfamily','subgenus','suborder','subphylum','subspecies','subtribe','superclass','superfamily','superkingdom','superorder','superphylum','tribe','varietas')

class TaxNamesWithoutAppNameBase(ModelBase):
    def __new__(cls, name, bases, attrs):
        model = super(TaxNamesWithoutAppNameBase, cls).__new__(cls, name, bases, attrs)
        model._meta.db_table = name.lower()
        return model

class Names(models.Model):
    __metaclass__ = TaxNamesWithoutAppNameBase
    tax_id = models.IntegerField(primary_key=True)
    name_txt = models.CharField(max_length=255)
    unique_name = models.CharField(max_length=255)
    name_class = models.CharField(max_length=255)


class TaxNodesWithoutAppNameBase(ModelBase):
    def __new__(cls, name, bases, attrs):
        model = super(TaxNodesWithoutAppNameBase, cls).__new__(cls, name, bases, attrs)
        model._meta.db_table = name.lower()
        return model

class Nodes(models.Model):
    __metaclass__ = TaxNodesWithoutAppNameBase
    tax_id = models.IntegerField(primary_key=True)
    parent_tax_id = models.IntegerField()
    rank = models.CharField(max_length=20)
    embl_code = models.CharField(max_length=10)
    division_id = models.IntegerField()
    inherited_div_flag = models.CharField(max_length=1, choices=BOOLEAN)
    genecode_id = models.IntegerField()
    inherited_GC_flag = models.CharField(max_length=1, choices=BOOLEAN)
    mitocondrial_gencode_id = models.IntegerField()
    inherited_MGC_flag = models.CharField(max_length=1, choices=BOOLEAN)
    genbank_hidden_flag = models.CharField(max_length=1, choices=BOOLEAN)
    hidden_subtree_root_flag = models.CharField(max_length=1, choices=BOOLEAN)


# for job administration

STATUS = ( ('Success', 'Success'), ('Failure', 'Failure'), ('In Progress', 'In Progress'), ('Aborted', 'Aborted') )

class Jobs(models.Model):
    log_id = models.IntegerField(primary_key=True)
    accession = models.CharField(max_length=20)
    version = models.IntegerField()
    step_name = models.CharField(max_length=50)
    step_status = models.CharField(max_length=20, choices = STATUS)
    step_start_time = models.DateField()
    job_name = models.CharField(max_length=50)
    job_uuid = models.CharField(max_length=50)
    job_status = models.CharField(max_length=20, choices = STATUS)
    job_start_time = models.DateField()
    
    def __unicode__(self):
        return str(self.log_id)
