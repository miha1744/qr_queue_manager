from django import forms
from django.contrib.auth.models import User
import datetime
from django.forms import ModelForm, EmailField, CharField, DateInput
from . import models
from django.contrib.admin import widgets
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput



#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        widgets = {
        'appointment_duration': TimePickerInput(),
        }
        fields=['address','mobile','department','status','appointment_duration','profile_pic']




#Для регистрации пациентов
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password' ]
        widgets = {
        'password': forms.PasswordInput(),
        }
class PatientForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    class Meta:
        model=models.Patient
        widgets = {
        'birthday': DatePickerInput( options={
                    "format": "DD.MM.YYYY", # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,

                } )
        }
        fields=['address','mobile','status','birthday','profile_pic']



class queueForm(forms.ModelForm):
    Doctorqueue=forms.ModelChoiceField(queryset=models.Doctorqueue.objects.all(),empty_label="Doctor Queue and Department", to_field_name="doctor")

    class Meta:
        model=models.Membership
        fields = ('Doctorqueue',)

    def save(self, patient, doctor_id):
        obj = super(queueForm, self).save(commit=False)
        obj.patient = patient
        try:
            doctor = models.Doctor.objects.get(id = doctor_id)
        except models.Doctor.DoesNotExist:
            doctor = None

        print(len(models.Doctorqueue.objects.get(doctor = doctor).patients.all()))
        if(len(models.Doctorqueue.objects.get(doctor = doctor).patients.all()) == 0):
            obj.membershipId = 0
        else:
            docqueue = models.Doctorqueue.objects.filter(doctor = doctor).first()
            objects = models.Membership.objects.filter(Doctorqueue = docqueue, status = 0)
            obj.membershipId = len(objects)
        obj.status = 0
        print(obj.membershipId)
        return obj.save()




class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']





