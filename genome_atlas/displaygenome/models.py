from django.db import models
from django.db.models.base import ModelBase

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
