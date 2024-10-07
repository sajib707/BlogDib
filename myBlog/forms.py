from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Your Email"}
        ),   
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )


class BlogSearchForm(forms.Form):
    query = forms.CharField(
        label="Search",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search for articles"})
    )