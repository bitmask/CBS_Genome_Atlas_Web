from django.db import models
from django.db.models.base import ModelBase


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

    def __unicode__(self):
        return self.genome_id

class Replicon_Stats(models.Model):
    replicon_id = models.IntegerField(primary_key=True)
    accession = models.CharField(max_length=200)
    version = models.IntegerField()
    genome = models.ForeignKey(Genome_Stats)
    replicon_type = models.CharField(max_length=200)
    stat_size_bp = models.IntegerField()
    gene_density = models.FloatField()
    stat_perc_at = models.FloatField()
    stat_number_of_genes = models.IntegerField()
    rrna_count_accession = models.IntegerField()
    trna_count_accession = models.IntegerField()

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
