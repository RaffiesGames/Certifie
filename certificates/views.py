from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .form import CertiData,CreateUserForm
from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd
import shutil
import logging
from django.contrib import messages 
import ast
import glob

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create your views here.
from .models import certificate,font
from .decorators import unauthenticated_user



#user accounts section


@unauthenticated_user
def userlogin(request):
    context = {}
    return render(request, "login.html", context)
        
        
def userlogout(request):
    logout(request)
    return redirect('userlogin')



#user account ends here

#this is called 'home'
@login_required(login_url='userlogin')
def certificate_list_view(request):
    cert_objects = certificate.objects.all()
    font1 = font.objects.get(font_id = 1)
    #print(font1.font_id)
    context = {
        'cert_objects': cert_objects
    }

    return render ( request, "album.html", context)


@login_required(login_url='userlogin')
def next_post(request, certid):
    c_id= certid
    cert_objects = certificate.objects.get(cert_id = c_id)
    print(cert_objects.name,cert_objects.desc)
    submitted = False
    context = { 'cert_objects': cert_objects, 
                'form': CertiData(request.POST, request.FILES), 
                'submitted': submitted }

    if request.method == 'POST':
        form = CertiData(request.POST, request.FILES)
        if form.is_valid():
                  
            script_dir = os.getcwd()
        
            Sign_Count = int(request.POST['Sign_No'])+1

            ExcelData = request.FILES['ExcelData']
            info = pd.read_excel(ExcelData, header=None)
            x = info.values.tolist()

            if Sign_Count == 1:
                imgfile=str(cert_objects.image1.url)
                for i in range(0, len(x)):
                    x[i].append(" ")
                    x[i].append(" ")
                    x[i].append(" ")
                    x[i].append(" ")
            if Sign_Count == 2:
                imgfile=str(cert_objects.image2.url)
                for i in range(0, len(x)):
                    x[i].append(" ")
                    x[i].append(" ")
            if Sign_Count == 3:
                imgfile=str(cert_objects.image3.url)
            
            path=script_dir+imgfile
            
            FontFile = str(cert_objects.font_used.font_file)          
            Name_Font = ImageFont.truetype(FontFile, int(cert_objects.font_size2))
            Other_Font = ImageFont.truetype(FontFile, int(cert_objects.font_size1))


        
            box = '['+cert_objects.dimensions+']'
            bounding_box = ast.literal_eval(box)       
            
            for info in x:

                img = Image.open(path)     
                d = ImageDraw.Draw(img)
                i=0
                for box in bounding_box:
                    if(i!=1 and i!=3):
                        if(i==0 or i==4):
                            Font_Used = Name_Font
                        else:
                            Font_Used = Other_Font
                        x1,y1,x2,y2=box
                        w, h = d.textsize(info[i], font=Font_Used)
                        x = (x2 - x1 - w)/2 + x1
                        y = (y2 - y1 - h)/2 + y1
                        d.text((x,y), info[i], align='center', font = Font_Used, fill=(0,0,0))
                        i = i+1
                    else:
                        Font_Used = Other_Font
                        x1,y1,x2,y2 = box
                        w, h = d.textsize(info[i], font=Font_Used)
                        x = x1
                        y = (y2 - y1 - h)/2 + y1
                        d.text((x,y), info[i], align='center', font = Font_Used, fill=(0,0,0))
                        i = i+1

                img.save(script_dir+"/Generated_Images/"+info[0]+".png")
            shutil.make_archive(script_dir+'/Certifie Files', 'zip', script_dir+'/Generated_Images/')            
     
            To_Email = request.user.email
            From_Email = 'certifiewebsite@gmail.com'
            password = 'tpardbizbwjtrdqn'
            
            message = MIMEMultipart()
            message['Subject'] = "Your Generated Certificates from Certifie!"
            message['To'] = To_Email
            message['From'] = From_Email

            zipfile = "Certifie Files.zip"

            with open(zipfile, "rb") as attachment:
                part2 = MIMEBase("application", "octet-stream")
                part2.set_payload(attachment.read())

            encoders.encode_base64(part2)

            part2.add_header("Content-Disposition",
                              f"attachment; filename= {zipfile}")

            textwrite = "Thanks for using Certifie!"
            
            part1 = MIMEText(textwrite, "plain")

            message.attach(part1)
            message.attach(part2)
            text = message.as_string()

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(From_Email, password)
                server.sendmail(From_Email, To_Email, text)

            return HttpResponseRedirect("/success")

        else:
            messages.error(request, "Error")

    return render ( request, "next2.html", context) 


@login_required(login_url='userlogin')
def generate(request):
    # Called after sending email to delete images created and zip file so we dont store any data
    context={} 
    path = os.getcwd()
    folder = path+"/Generated_Images/"
    shutil.rmtree(folder)
    os.mkdir(folder)
    zip_path = path+"/Certifie Files.zip"
    os.remove(zip_path)

    return render(request, 'success.html', context)


"""
#user stuff
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account was created for ' + user)

                return redirect('userlogin')
        
    context = { 'form' : form }
    return render(request, "register.html", context)
    
    @unauthenticated_user
    def userlogin(request):
        context = {}
        if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request,username=username,password=password)

                if user is not None:
                    login(request,user)
                    return redirect('home')
                else: 
                    messages.info(request,'Username OR Password is incorrect.')
                    return render(request, "login.html", context)

        return render(request, "login.html", context)"""

"""
def form_data(request):
    context = {}
    return render(request, "form.html", context)

def home(request):
    cert_objects = certificate.objects.all()
    font1 = font.objects.get(font_id = 1)
    #print(font1.font_id)
    context = {
        'cert_objects': cert_objects
    }
    return render(request,'album.html',context)"""
