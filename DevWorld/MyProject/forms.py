from django.forms import ModelForm
from .models import Project, Review
from django import forms


class MyProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','featured_image', 'description', 'demo_link', 'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(MyProjectForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add title'})
        # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': 'Add description'})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            "value": 'Place your vote',
            "body": "Add a comment"
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add title'})
        # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': 'Add description'})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



