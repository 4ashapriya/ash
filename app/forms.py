from django import forms
from .models import BulkUser


class StudentBulkUploadForm(forms.ModelForm):
  class Meta:
    model = BulkUser
    fields = ("csv_file",)