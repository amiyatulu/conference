from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from django.db import models
from django.forms.models import ModelForm
from django.utils.timezone import utc
import datetime
import os


class Registration(models.Model):
    registration_number = models.CharField(max_length=100,null = True,blank=True)
    SALUTATION_TYPE = (
        ('Mr', 'Mr.'),
        ('Ms', 'Ms.'),
        ('Dr', 'Dr.'),
        ('Prof','Prof.'),
    )
    salutation = models.CharField(max_length=10, choices=SALUTATION_TYPE, verbose_name = "", blank=False, default='Mr')
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null = True, blank = True)
    last_name = models.CharField(max_length=100)
    POSITION_TYPE = (
        ('stud','Student'),
        ('staf','Staff Scientist'),
        ('prof','Professor'),
                     )
    position = models.CharField(max_length=20, choices=POSITION_TYPE)
    GENDER_TYPE = (
            ('M','Male'),
            ('F','Female'),
                   
                   )
    gender = models.CharField(max_length=2, choices=GENDER_TYPE, blank=False, default="M")
    AFFILIATION_TYPE = (
                        ('ACA','Academic'),
                        ('COR','Corporate'),
                        
                        )
    affiliation = models.CharField(max_length=5, choices=AFFILIATION_TYPE) 
    institution = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, null=True,blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100, verbose_name="pin")
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    bank = models.CharField(max_length=100, verbose_name="bank Name")
    branch = models.CharField(max_length=100)
    check_number = models.CharField(max_length=100, verbose_name= "check Number (Please mention transaction reference number in case of Online Transfer)")
    abstract = models.FileField(upload_to="abstracts",null=True,blank=True)
    comment = models.TextField( null=True,blank=True, verbose_name = "comment (Any comment or queries that you may have)")
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    def clean(self):
        acceptedfile = self.abstract
        if acceptedfile:
            if acceptedfile.size > 30*1024*1024:
                raise ValidationError("You have uploaded a file larger than 30Mb")
            extension = os.path.splitext(acceptedfile.name)[1]
            if extension.lower() not in ['.docx','.doc','.pdf']:
                raise ValidationError("Only docx,doc,pdf file formats are allowed")  
            
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.create_time == None:
            self.create_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.update_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        super(Registration, self).save(*args, **kwargs)
    def __unicode__(self):
        return self.registration_number + " " +self.first_name + " " + self.last_name
    
    
class RegistrationForm(ModelForm):
    
    class Meta:
        model = Registration
        exclude = ['create_time','update_time','registration_number']
        widgets = {
                   'gender':forms.RadioSelect
                   }

class paymentReceived(models.Model):
    registration = models.ForeignKey(Registration)
    PAYMENT = (
            ('Y','Yes'),
            ('N','No'),
                   
                   )
    payment_received = models.CharField(max_length=2, choices=PAYMENT, blank=False, default="N")
    comment = models.TextField( null=True,blank=True)
    def __unicode__(self):
        return self.registration.first_name + " " + self.registration.last_name
    
class AmountReceived(models.Model):
    registration = models.ForeignKey(Registration, primary_key=True)
    PAYMENT = (
            ('Y','Yes'),
            ('N','No'),
                   
                   )
    payment_received = models.CharField(max_length=2, choices=PAYMENT, blank=False, default="N")
    PAYMENT_TYPE = (
                    ('D', 'Check or DD'),
                    ('O', 'Online Transaction'),
                    ('C', 'Cash')
                    )
    payment_type = models.CharField(max_length=2, choices=PAYMENT_TYPE, blank=False)
    amount = models.IntegerField()
    transcation_no = models.CharField(max_length=100)
    comment = models.TextField( null=True,blank=True)
    def __unicode__(self):
        return self.registration.registration_number+ " " + self.registration.first_name + " " + self.registration.last_name
    
        

def mailing(reg):
    my_host = "smtp.webfaction.com"
    my_username = "conference"
    my_password = "@stemcell#"
    connection = get_connection(host=my_host,
                                username= my_username,
                                password= my_password,
                                )
    
    fullname = (reg.first_name + " " + reg.middle_name + " " + reg.last_name).encode('utf-8')
    parameters = {"salutation":reg.salutation.encode('utf-8'), "firstname":reg.first_name.encode('utf-8'), "conferenceid":reg.registration_number.encode('utf-8'),
                  "fullname": fullname, "institution": reg.institution.encode('utf-8'), "department": reg.department.encode('utf-8'), 
                  "address1":reg.address_1.encode('utf-8'), "address2": reg.address_2.encode('utf-8'), "city":reg.city.encode('utf-8'),
                  "state": reg.state.encode('utf-8'), "zip": reg.zip.encode('utf-8'), "country": reg.country.encode('utf-8'),
                  "phone":reg.phone.encode('utf-8'),"email":reg.email.encode('utf-8'), "bank":reg.bank.encode('utf-8'),
                  "branch":reg.branch.encode('utf-8'),"check":reg.check_number.encode('utf-8')
                   }
    message = """<body style="width:800px;
 background-color:#ECECEC;">
<img width="800px" src="http://jplab.webfactional.com/header.png"/>

<p  style="color:gray;font-size:20px;padding-left:30px;"> Dear %(salutation)s. %(firstname)s, <br>
Your registration details are: <br><br>
<b>Conference Id: %(conferenceid)s </b><br>
Name: %(fullname)s<br>
Institution: %(institution)s <br>
Department: %(department)s <br>
Address 1: %(address1)s <br>
Address 2: %(address2)s <br>
City: %(city)s <br>
State: %(state)s <br>
Zip: %(zip)s <br>
Country: %(country)s <br>
Phone: %(phone)s <br>
Email: %(email)s <br>
Bank Name: %(bank)s <br>
Branch: %(branch)s <br>
Check Number: %(check)s <br>

<br>
<br>

<div style="padding-left:30px">
<h2 style="color: #9a9661; font-size:35px;font-weight:bold;font-family: HelveticaNeue, sans-serif;margin-left:80px;">Topics </h2>
<p style="color:#00c4fa;font-weight:bold;font-size:25px;">Transcriptional Control<br>
Nuclear Architecture and Dynamics<br>
Biology of Noncoding RNAs<br>
Epigenetics<br>
Gene Regulatory Networks and Cell Fate<br>
Cell Reprogramming<br>
Genome Dysregulation and Disease</p>



 <p  style="text-align:center;background-color:#043948;font-family: HelveticaNeue, sans-serif;color:white; padding:10px;"> School of Life
                              Sciences<br>
                              University of Hyderabad <br>
                              Gachibowli, Hyderabad 500046, India <br>
                              Phone: +91 40 2313 4580<br>
                              <br>
                              <a href="http://www.genomearchitecture.in" style="color: #e7cba3; text-decoration: none; font-weight: bold;">www.genomearchitecture.in</a>
                            </p>


</body>""" % parameters
    msg = EmailMessage("Thank You For Registration", message, 'conference@genomearchitecture.in',[reg.email.encode('utf-8')],connection = connection)
    msg.content_subtype = "html"
    msg.send()
    
    
