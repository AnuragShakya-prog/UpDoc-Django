from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.keys():
            
            self.fields[field].widget.attrs.update({"class":"form-control"})


    class Meta:
        model=User

        fields=["username","password1","password2"]

        labels={"username":"Username-C"}



