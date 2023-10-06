from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .models import Docutor,Patient
from django.contrib import messages

from django.contrib.auth.hashers import make_password,check_password


from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
email_validator = EmailValidator(message='pankaj@gmail.com')

import re
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
# from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.
def home(request):
    return render(request,"home.html")

def register_docuter(request):
    try:
        if request.method == "POST":    
            data = request.POST
            name = data.get("name")
            email=data.get("email")
            phone = data.get("phone")
            degree = data.get("degree")
            experience = data.get("exp")
            specialization = data.get('spe')
            gender = data.get('gender')
            appoimentdate = data.get('date')
            photo = request.FILES.get('photo')
            address = data.get('address')
            password = make_password(data.get('password'))

            if Docutor.objects.filter(email = email).exists():
                messages.error(request,'Docutor already exists!')
                return redirect('/register_docuter/')
            
            if len(phone) != 10:
                messages.error(request,"Mobile number should be in 10 digit")
                return redirect('/register_docuter/')
            
            try:
                email_validator(email)
            except ValidationError:
                messages.error(request, "Invalid email address")
                return redirect("/register_docuter/")

            if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).*$', password):
                messages.error(request, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@#$%^&+=!)")
                return redirect("register_docuter")
                        
            user = Docutor.objects.create(
                name = name,
                email = email,
                phone = phone,
                degree = degree,
                experience = experience,
                specialzation = specialization,
                gender = gender,
                appoiment = appoimentdate,
                photo = photo,
                address = address,
                password = password
            )
            user.save()
            refresh = RefreshToken.for_user(user)
            token = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return JsonResponse({"message": "Registered Successfully!!", "token": token})
        return render(request,"register_docutor.html")
    except Exception as e:
        pass


def docuter(request):
    if request.session.get('name') is not None:
        patient_session = request.session.get('name', 'default_value')
        print(patient_session)
        patient = Patient.objects.get(Name = patient_session)
        print(patient.disease)
        request.session['id'] = patient.id
        if Docutor.objects.filter(specialzation__icontains = patient.disease):
            docutor = Docutor.objects.filter(specialzation__icontains = patient.disease)
            context = {
            'Docutors': docutor,
            'session': True
            }   
    else:
        docutor = Docutor.objects.all()
        context = {
            'Docutors': docutor,
            'session': False
        }
    return render(request,'docutor.html', context)

def donedocuter(request,id):
    try :
        docuter = Docutor.objects.get(id = id)
        patient_id = request.session.get('id', 'default_value')
        print("id :",patient_id)
        patient = Patient.objects.get(id = patient_id)
        print("patient name is :", patient.Name)
        patient.docutor = docuter
        patient.save()
        request.session.flush()
        return HttpResponse("your appoiment is done")
        
    except Exception as e:
        print(e)
        patient.delete()
        patient.save()
        return HttpResponse("cancel appoiment")
def add_patient(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        phone = data.get('phone')
        age = data.get('age')
        address = data.get('address')
        disase = data.get('disase')
        gender = data.get('gender')
        password = make_password(data.get('password'))
        photo = request.FILES.get('photo')

        patient = Patient.objects.create(
            Name = name,
            phone = phone,
            age = age,
            address = address,
            disease = disase,
            gender = gender,
            password = password,
            Photo = photo,
        )
        patient.save()
        request.session['name'] = name
        return redirect('/docuter/')
     
    return render(request,"add_patient.html")
