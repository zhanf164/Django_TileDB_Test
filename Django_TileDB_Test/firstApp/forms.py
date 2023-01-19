from django import forms

CHR_CHOICES = (("chr1", "chr1"), ("chr2","chr2"), ("chr3", "chr3"), ("chr4", "chr4"), ("chr5", "chr5"))

class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)

class RegionForm(forms.Form):
    chrom = forms.ChoiceField(choices=CHR_CHOICES)
    start = forms.CharField(max_length=20)
    stop = forms.CharField(max_length=20)