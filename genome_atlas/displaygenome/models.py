from django.db import models
from django.db.models.base import ModelBase
import math

class Tax_Stats(models.Model):

    row_id = models.IntegerField(primary_key=True)
    tax_id = models.IntegerField()
    modify_date = models.DateField()
    tax_name = models.CharField(max_length=200)
    genome_count = models.IntegerField()
    score = models.FloatField()
    gene_density = models.FloatField()
    percent_at = models.FloatField()
    chromosome_count = models.IntegerField()
    plasmid_count = models.IntegerField()
    replicon_count = models.IntegerField()
    total_bp = models.BigIntegerField()
    gene_count = models.IntegerField()
    rrna_count = models.BigIntegerField()
    trna_count = models.BigIntegerField()
    contig_count = models.IntegerField()
    nonstd_bp = models.BigIntegerField()
    at_bp = models.BigIntegerField()

class Genome_Stats(models.Model):

    row_id = models.IntegerField(primary_key=True)
    genome_id = models.IntegerField(primary_key=True)
    modify_date = models.DateField()
    tax_id = models.IntegerField()
    bioproject_id = models.IntegerField()
    genome_name = models.CharField(max_length=200)
    score = models.FloatField()
    gene_density = models.FloatField()
    percent_at = models.FloatField()
    chromosome_count = models.IntegerField()
    plasmid_count = models.IntegerField()
    replicon_count = models.IntegerField()
    contig_count = models.IntegerField()
    total_bp = models.IntegerField()
    gene_count = models.IntegerField()
    rrna_count = models.BigIntegerField()
    trna_count = models.BigIntegerField()
    at_bp = models.BigIntegerField()
    nonstd_bp = models.IntegerField()
    percent_nonstd_bp = models.FloatField()
    
    def __unicode__(self):
        return self.genome_id

class Replicon_Stats(models.Model):

    row_id = models.IntegerField(primary_key=True)
    genome = models.ForeignKey(Genome_Stats)
    accession = models.CharField(max_length=200)
    version = models.IntegerField()
    replicon_type = models.CharField(max_length=200)
    score = models.FloatField()
    gene_density = models.FloatField()
    percent_at = models.FloatField()
    total_bp = models.BigIntegerField()
    gene_count = models.IntegerField()
    trna_count= models.BigIntegerField()
    rrna_count= models.BigIntegerField()
    nonstd_bp = models.BigIntegerField()
    at_bp = models.BigIntegerField()
    contig_count = models.IntegerField()


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
