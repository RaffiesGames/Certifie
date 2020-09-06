from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
    
    def clean(self): #this function checks if email is unique
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email exists")
       return self.cleaned_data

class CertiData(forms.Form):
    Choices = (('0','1'),('1','2'),('2','3')) 
    pictureList = ["{{ cert_objects.image1.url }}", "{{ cert_objects.image2.url }}", "{{ cert_objects.image3.url }}"]	
    Sign_No = forms.CharField(label="Number of Signatures:", widget=forms.Select(attrs = {'onchange' : "var s1 = document.getElementById('id_Sign_No'); var val = s1.options[s1.selectedIndex].value; var pic_src = pictureList[val]; document.getElementById('DisplayPic').src = pic_src;"}, choices=Choices))
    ExcelData =  forms.FileField(label="Upload Excel File:")
