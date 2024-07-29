from django import forms


class UploadBucketObjectForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput)
