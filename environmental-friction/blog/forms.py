from django.forms import ModelForm

from .models import Post


class QuickDraftForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
