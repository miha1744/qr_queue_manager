from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import datetime

departments=[('Кардиолог','Кардиолог'),
('Дерматолог','Дерматолог'),
('Терапевт','Терапевт'),
('Хирург','Хирург'),
('Оториноларинголог','Оториноларинголог'),
('Офтальмолог','Офтальмолог'),
('Онколог','Онколог'),
('Психотерапевт','Психотерапевт'),
('Педиатр','Педиатр'),
('Кардиолог','Кардиолог'),
('Ревматолог','Ревматолог'),
('Невролог','Невролог'),
]
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(default= "NoneImage.jpg",null=True, blank=True)
    qr_code = models.ImageField(upload_to='images/qr_codes',default= "NoneImage.jpg", blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    appointment_duration = models.TimeField()
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id

    def save(self, *args, **kwargs):
        if(self.pk != None):
            qrcode_img = qrcode.make(self.pk)
            canvas = Image.new('RGB',(290,290), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            fname = f'qr_code-{self.pk}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save =False)
            canvas.close()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='images/profile-pic/PatientProfilePic',default= "NoneImage.jpg",null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    birthday = models.DateField(u'Day of the event', help_text=u'Day of the event')
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=True)



    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name




class Doctorqueue(models.Model):
    doctor = models.OneToOneField(Doctor,on_delete = models.CASCADE, primary_key = True )
    patients = models.ManyToManyField(Patient, through='Membership')



class Membership(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Doctorqueue = models.ForeignKey(Doctorqueue, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    status= models.PositiveIntegerField(null=True, default=0)
    membershipId = models.PositiveIntegerField(null=True)
    class Meta:
        ordering = ('membershipId',)











class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=True)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)
