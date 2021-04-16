from rest_framework import serializers
from django.forms import ModelForm, EmailField, CharField, DateInput
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from . import models


#Сериалайзер Юзера
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(username=validated_data["username"], first_name = validated_data["first_name"], last_name = validated_data["last_name"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name','last_name','username','password')

# Сериалайзер пациента
class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=True)

    class Meta:
        model = models.Patient
        fields = ("pk", "user", "mobile", "birthday")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        patient = models.Patient.objects.create(
            mobile = validated_data["mobile"],
            birthday = validated_data["birthday"],

            user=user
        )
        return patient



class PatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient
        fields = ("pk", "user", "mobile", "birthday")



#Сериалайзер Доктора
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Doctor
        fields = ('pk','user', 'address','mobile','department','status','appointment_duration','profile_pic', )



#Сериализаторы очередей
class DoctorqueueSerializer(serializers.ModelSerializer):
    doctor = serializers.SlugRelatedField(write_only=False, slug_field='pk', queryset = models.Doctor.objects.all())
    class Meta:
        model = models.Doctorqueue
        fields = ('pk','doctor')


# Сериализатор места в очереди
class MembershipSerializer(serializers.ModelSerializer):
    doctorqueue = serializers.SlugRelatedField(write_only=False, slug_field='doctor', queryset = models.Doctorqueue.objects.all())
    class Meta:
        model = models.Membership
        fields = ('pk','patient','Doctorqueue','date_joined','membershipId')



class UsersMembershipSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    Doctorqueue = serializers.SlugRelatedField(read_only=True, slug_field='pk')
    class Meta:
        model = models.Membership
        fields = ('pk','patient','Doctorqueue','date_joined','membershipId', 'user', 'status')




class CreateMembershipSerializer(serializers.ModelSerializer):

    Doctorqueue = serializers.SlugRelatedField(write_only=False, slug_field='pk', queryset = models.Doctorqueue.objects.all())
    patient = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Membership
        fields = ('pk','patient','Doctorqueue')

    def create(self, validated_data):
        user= validated_data.pop("patient")

        patient = models.Patient.objects.get(user = user)

        pk = validated_data['Doctorqueue']
        print(pk)
        if(len(models.Doctorqueue.objects.get(pk = pk).patients.all()) == 0):
            membershipId = 0
        else:
            docqueue = models.Doctorqueue.objects.filter(pk = pk).first()
            objects = models.Membership.objects.filter(Doctorqueue = docqueue, status = 0)
            membershipId = len(objects)
        status = 0
        docque =  models.Doctorqueue.objects.filter(pk = pk).first()

        membership = models.Membership.objects.create(
            patient=patient,
            status=status,
            membershipId= membershipId,
            Doctorqueue =docque
        )
        return membership


    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # Doctorqueue = models.ForeignKey(Doctorqueue, on_delete=models.CASCADE)
    # date_joined = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    # status= models.PositiveIntegerField(null=True, default=0)
    # membershipId = models.PositiveIntegerField(null=True)

    # def save(self, patient, doctor_id):
    #     obj = super(queueForm, self).save(commit=False)
    #     obj.patient = patient
    #     try:
    #         doctor = models.Doctor.objects.get(id = doctor_id)
    #     except models.Doctor.DoesNotExist:
    #         doctor = None
    #
    #     print(len(models.Doctorqueue.objects.get(doctor = doctor).patients.all()))
    #     if(len(models.Doctorqueue.objects.get(doctor = doctor).patients.all()) == 0):
    #         obj.membershipId = 0
    #     else:
    #         docqueue = models.Doctorqueue.objects.filter(doctor = doctor).first()
    #         objects = models.Membership.objects.filter(Doctorqueue = docqueue, status = 0)
    #         obj.membershipId = len(objects)
    #     obj.status = 0
    #     print(obj.membershipId)
    #     return obj.save()
