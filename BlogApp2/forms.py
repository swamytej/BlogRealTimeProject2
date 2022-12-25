from django import forms
from BlogApp2.models import Comment,Post

class Emailsendform(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comments =forms.CharField(required=False,widget=forms.Textarea)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields =('name','email','body')

from django.contrib.auth.models import User
class signupform(forms.ModelForm):
    class Meta:
        model= User
        fields = ['first_name','last_name','password','username','email']

class postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'