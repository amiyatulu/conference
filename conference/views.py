import csv
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from conference.models import RegistrationForm, mailing, Registration, \
    AmountReceived


def conferencehome(request):
    return render(request,'conference/home.html')


def sponsors(request):
    return render(request,'conference/sponsors.html')

def advisory(request):
    return render(request,'conference/advisory.html')
def speakers(request):
    return render(request,'conference/speakers.html')

def registrationform(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            registration = form.save()
            regid = registration.id
            regnumber = "GA" + str(regid).zfill(3)
            registration.registration_number = regnumber
            registration.save()
            mailing(registration)
            request.session["has_registered"] =  regnumber
            return HttpResponseRedirect(reverse('conference:registrationsuccessful'))
    else:
        form = RegistrationForm(auto_id='id_%s')
    return render(request,'conference/registration.html',{'form':form,
                                                          })
def registrationsuccessful(request):
    if not request.session.get('has_registered',False):
        return HttpResponse("Page Not Found.")
    else:
        regnumber = request.session['has_registered']
        return render(request, 'conference/registrationsuccessful.html',{'regnumber':regnumber,})
def contact(request):
    return render(request,'conference/contact.html')

def registrationdetails(request):
    return render(request,'conference/registrationdetails.html')


def travel(request):
    return render(request,'conference/travel.html')
def registrationclosed(request):
    return render(request,'conference/registrationclosed.html')
def schedule(request):
    return render(request,'conference/schedule.html')


def download_csv(request):
    if not request.user.is_staff:
        raise PermissionDenied
    queryset = Registration.objects.all()
    opts = queryset.model._meta
    
    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
    

def download_csv_received(request):
    if not request.user.is_staff:
        raise PermissionDenied
    queryset = AmountReceived.objects.all()
    opts = queryset.model._meta
    
    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=amountreceived.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response   
        

def plotpcashift(request, chrid):
    f = open("/media/d/bioinfolab/pca/pca homer/checker2/chr"+ chrid + "_all_resolutions", 'r')
    kb1000 = []
    kb500 = []
    kb250 = []
    kb100 = []
    kb50 = []
    for line in f:
        line = line.replace("\n", "")
        arry = line.split("\t")
        try:
            if arry[3]:
                kb1000.append(int(arry[3]))
        except:
            pass
        try:
            if arry[8]:
                kb500.append(int(arry[8]))
        except:
            pass
        try:
            if arry[13]:
                kb250.append(int(arry[13]))
        except:
            pass
        try:
            if arry[18]:
                kb100.append(int(arry[18]))
        except:
            pass
        try:
            if arry[23]:
                kb50.append(int(arry[23]))
        except:
            pass
                
        
    return render(request, 'conference/plotpcashift.html',{'kb1000':kb1000, 'kb500':kb500, 'kb250':kb250, 'kb100':kb100,'kb50':kb50})

def plotpcashift2(request, chrid):
    f = open("/media/d/bioinfolab/pca/pca homer/checker3/chr"+ chrid + "_all_resolutions", 'r')
    kb1000 = []
    kb500 = []
    kb250 = []
    kb100 = []
    kb50 = []
    kb25 = []
    mb = []
    for line in f:
        line = line.replace("\n", "")
        arry = line.split("\t")
        try:
            if arry[0]:
                mb.append(int(arry[0]))
        except:
            pass
                
        try:
            if arry[4]:
                kb1000.append(int(arry[4]))
        except:
            pass
        try:
            if arry[9]:
                kb500.append(int(arry[9]))
        except:
            pass
        try:
            if arry[14]:
                kb250.append(int(arry[14]))
        except:
            pass
        try:
            if arry[19]:
                kb100.append(int(arry[19]))
        except:
            pass
        try:
            if arry[24]:
                kb50.append(int(arry[24]))
        except:
            pass
        try:
            if arry[29]:
                kb25.append(int(arry[29]))
        except:
            pass
        
    return render(request, 'conference/plotpcashift2.html',{'kb1000':kb1000, 'kb500':kb500, 'kb250':kb250, 'kb100':kb100,'kb50':kb50,'kb25':kb25, 'mb':mb})
        
    
def plotpcashift2color(request, chrid):
    f = open("/media/d/bioinfolab/pca/pca homer/checker4differentswitch/chr"+ chrid + "_all_resolutions", 'r')
    kb1000 = []
    kb500 = []
    kb250 = []
    kb100 = []
    kb50 = []
    kb25 = []
    mb = []
    for line in f:
        line = line.replace("\n", "")
        arry = line.split("\t")
        try:
            if arry[0]:
                mb.append(int(arry[0]))
        except:
            pass
                
        try:
            if arry[4]:
                kb1000.append(int(arry[4]))
        except:
            pass
        try:
            if arry[9]:
                kb500.append(int(arry[9]))
        except:
            pass
        try:
            if arry[14]:
                kb250.append(int(arry[14]))
        except:
            pass
        try:
            if arry[19]:
                kb100.append(int(arry[19]))
        except:
            pass
        try:
            if arry[24]:
                kb50.append(int(arry[24]))
        except:
            pass
        try:
            if arry[29]:
                kb25.append(int(arry[29]))
        except:
            pass
        
    return render(request, 'conference/plotpcashift2color.html',{'kb1000':kb1000, 'kb500':kb500, 'kb250':kb250, 'kb100':kb100,'kb50':kb50,'kb25':kb25, 'mb':mb})
        
def plotpcashift2color2(request, chrid):
    f1000 = open("/media/d/bioinfolab/pca/pca homer/checker1mb/chr"+ chrid + "_1mb_resolutions", 'r')
    f500 = open("/media/d/bioinfolab/pca/pca homer/checker1mb/chr"+ chrid + "_500kb_resolutions", 'r')
    f250 = open("/media/d/bioinfolab/pca/pca homer/checker1mb/chr"+ chrid + "_250kb_resolutions", 'r')
    f100 = open("/media/d/bioinfolab/pca/pca homer/checker1mb/chr"+ chrid + "_100kb_resolutions", 'r')
    f50 = open("/media/d/bioinfolab/pca/pca homer/checker1mb/chr"+ chrid + "_50kb_resolutions", 'r')
    f25 = open("/media/d/bioinfolab/pca/pca homer/checker1mb/chr"+ chrid + "_25kb_resolutions", 'r')
    kb1000 = []
    kb500 = []
    kb250 = []
    kb100 = []
    kb50 = []
    kb25 = []
    mb = []
    for line in f1000:
        line = line.replace("\n", "")
        arry = line.split("\t")
        mb.append(arry[0])
        kb1000.append(int(arry[1]))
    for line in f500:
        line = line.replace("\n", "")
        arry = line.split("\t")
        kb500.append(int(arry[1]))
    
    ln = len(mb)*2
    if len(kb500) != ln:
        kb500 += [0] * (ln - len(kb500))
    
    for line in f250:
        line = line.replace("\n", "")
        arry = line.split("\t")
        kb250.append(int(arry[1]))
    ln = len(mb)*4
    if len(kb250) != ln:
        kb250 += [0] * (ln-len(kb250))
    
    for line in f100:
        line = line.replace("\n", "")
        arry = line.split("\t")
        kb100.append(int(arry[1]))
        
    ln = len(mb)*10
    if len(kb100) != ln:
        kb100 += [0] * (ln-len(kb100))
        
    for line in f50:
        line = line.replace("\n", "")
        arry = line.split("\t")
        kb50.append(int(arry[1]))
    
    ln = len(mb)*20
    if len(kb50) != ln:
        kb50 += [0] * (ln-len(kb50))
        
    for line in f25:
        line = line.replace("\n", "")
        arry = line.split("\t")
        kb25.append(int(arry[1]))
        
    ln = len(mb)*40
    if len(kb25) != ln:
        kb25 += [0] * (ln-len(kb25))
        
    return render(request, 'conference/plotpcashift2color.html',{'kb1000':kb1000, 'kb500':kb500, 'kb250':kb250, 'kb100':kb100,'kb50':kb50,'kb25':kb25, 'mb':mb})
        


        
    
    