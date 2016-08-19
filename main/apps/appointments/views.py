from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import User, Appointment
from datetime import datetime
# Create your views here.
def index(request):
    return render(request, 'appointments/index.html')

def register(request):
    check = User.userManager.checkreg(request.POST['name'], request.POST['email'], request.POST['dob'], request.POST['pass'], request.POST['conf_pass'])

    if check == True:
        passinput = request.POST['pass'].encode()
        hashed = bcrypt.hashpw(passinput, bcrypt.gensalt())
        User.objects.create(name=request.POST['name'], email=request.POST['email'], dob=request.POST['dob'], password=hashed)
        return redirect('/')
    else:
        for error in check:
            messages.error(request, error)
        return redirect('/')

def login(request):
    check = User.userManager.checklog(request.POST['loginemail'], request.POST['loginpass'])

    if check[0] == True:
        request.session['user']=check[1].id
        return redirect('/appointments')
    else:
        for error in check:
            messages.error(request, error)
        return redirect ('/')

def appointments(request):
    if not 'user' in request.session:
        return redirect('/')
    now = datetime.now()
    now = now.replace(hour=23, minute=59)
    user = User.objects.get(id=request.session['user'])
    today = Appointment.objects.filter(created_by=User.objects.get(id=request.session['user']), date=now)
    other = Appointment.objects.filter(created_by=User.objects.get(id=request.session['user']), date__gt=now)
    context = {
        'user':user,
        'today':today,
        'other':other,
    }
    return render(request, 'appointments/appointments.html', context)

def logout(request):
    del request.session['user']
    return redirect('/')

def delete(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return redirect('/appointments')

def edit(request, id):
    if not 'user' in request.session:
        return redirect('/')
    appointment = Appointment.objects.get(id=id)
    if appointment.created_by != User.objects.get(id=request.session['user']):
        return redirect('/')
    print appointment.date
    date = str(appointment.date)
    time = str(appointment.time)
    context ={
        'appointment':appointment,
        'date':date,
        'time':time,
    }
    return render(request, 'appointments/edit.html', context)

def update(request, id):
    check = Appointment.appointmentManager.addcheck(request.POST['date'], request.POST['time'], request.POST['task'])
    if check == True:
        appointment = Appointment.objects.filter(id=id)
        appointment.update(task=request.POST['task'], time = request.POST['time'], date=request.POST['date'], status = request.POST['status'])
        return redirect('/appointments')
    else:
        for error in check:
            messages.error(request, error)
        return redirect ('/edit/'+str(id))

def add(request):
    print request.POST['time']
    check = Appointment.appointmentManager.addcheck(request.POST['date'], request.POST['time'], request.POST['tasks'])
    if check == True:
        Appointment.objects.create(task=request.POST['tasks'], time = request.POST['time'], date= request.POST['date'], status='Pending', created_by = User.objects.get(id=request.session['user']))
        return redirect('/appointments')
    else:
        for error in check:
            messages.error(request, error)
        return redirect ('/appointments')
