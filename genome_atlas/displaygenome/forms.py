from django import forms

per_page_selection   = (
                         (10 , '10'),
                         (25 , '25'),
                         (50 , '50'),
                         (100 ,'100'),
                       )

order_dir_selection  = (
                         ('ASC','Ascending'),
                         ('DSC','Descending'),
                       )

class TaxonomyForm(forms.Form):
# These fields are searchable for taxonomy nodes

    order_by_selection=(
                         ('modify_date', 'Modify Date'),
                         ('tax_id', 'Taxonomy ID'),
                         ('bioproject_id', 'Bioproject ID'),
                         ('genome_name', 'Genome Name'),
                         ('score','Genome Score'),
                         ('chromosome_count','Chromosomes'),
                         ('plasmid_count','Plasmids'),
                         ('percent_at','Percent AT'),
                         ('gene_count','Gene Count'),
                         ('gene_density','Gene Density'),
                         ('rrna_count','rRNA Count'),
                         ('trna_count','tRNA Count'),
                       )
    per_page=forms.ChoiceField(choices=per_page_selection, label='Results per page')
    order_by=forms.ChoiceField(choices=order_by_selection, label='Order by')
    order_dir=forms.ChoiceField(choices=order_dir_selection, label='Direction')
    current_page=forms.IntegerField(min_value=1, label='Page number')
    per_page.widget.attrs["onchange"]="this.form.submit()"

"""
class GenomeSingleForm(forms.Form):
    order_by_selection = (
                           ('accession','Accession Number'),
                           ('stat_size_bp', 'Length (bp)'),
                           ('stat_perc_at', 'Percent AT'),
                           ('stat_number_of_genes', 'Genes'),
                           ('replicon_type', 'Replicon Type'),
                           ('rrna_count_accession', 'rRNA count'),
                           ('trna_count_accession', 'tRNA count'),
                         )

    per_page=forms.ChoiceField(choices=per_page_selection, label='Results per page')
    order_by=forms.ChoiceField(choices=order_by_selection, label='Order by')
    order_dir=forms.ChoiceField(choices=order_dir_selection, label='Direction')
    current_page=forms.IntegerField(min_value=1, label='Page number')
    per_page.widget.attrs["onchange"]="this.form.submit()"
"""
