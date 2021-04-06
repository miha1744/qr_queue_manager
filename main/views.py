from django.shortcuts import render, redirect, get_object_or_404, reverse
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy, reverse
from datetime import datetime, timedelta,date
from .models import  Patient, Doctor
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
# Create your views here.




# Doctor Registration
class CreateDoctorView(CreateView):
    form_class = forms.DoctorRegisterForm
    success_url = reverse_lazy("login")
    template_name = "register.html"
