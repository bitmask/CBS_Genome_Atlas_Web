from django.db import models

# Create your models here.

class Genome_Stats(models.Model):
    genome = models.IntegerField(primary_key=True)
    tax_id = models.IntegerField()
    bioproject_id = models.IntegerField()
    genome_name = models.CharField(max_length=200)
    score = models.FloatField()
    chromosome_count = models.IntegerField()
    plasmid_count = models.IntegerField()
    total_bp = models.IntegerField()
    gene_count = models.IntegerField()
    percent_at = models.FloatField()

    def __unicode__(self):
        return self.genome_id
    
class Replicon(models.Model):
    replicon_id = models.IntegerField(primary_key=True)
    accession = models.CharField(max_length=200)
    version = models.IntegerField()
    genome = models.ForeignKey(Genome_Stats)
    replicon_type = models.CharField(max_length=200)

    def __unicode__(self):
        return self.accession
