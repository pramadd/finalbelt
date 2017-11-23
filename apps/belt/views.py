from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
# from .models import User
from django.contrib import messages
from .models import *
import bcrypt



def index(request):
    return render(request,'belt/index.html')

def register(request):

    first_name = request.POST['first_name']
    alias =  request.POST['alias']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    date = request.POST['date']
    errors = User.objects.validatereg(request.POST)


    #errors
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    else:
        
         #hashing pswd
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = first_name, alias = alias, email = email, password = hashed_password,date = date )
        
        request.session['id'] = user.id
        #session
        

        return redirect('/travels')


    #date of birth 
    minyear = 1900
    maxyear = datetime.date.today().year
    print datetime.date.today().year
    mydate = '12/12/2000'
    dateparts = mydate.split('/')
    try:
        if len(date) != 10:
           flash("Invalid date format")
        if int(date[2]) > maxyear or int(date[2]) < minyear:
           flash("Year out of range")
        dateobj = datetime.date(int(date[2]),int(date[1]),int(date[0]))
    except:
       return errors


def login(request):

    email = request.POST['email']
    password = request.POST['password']

    errors = User.objects.validatelogin(request.POST)
   
    #errors
    if len(errors):
        print "We have errors", errors
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    else:
        user = User.objects.get(email= request.POST['email'])

        request.session['id'] = user.id
        #session

        return redirect('/travels')


def travels(request):
    if 'id' not in request.session:
        return redirect('/')

    else:
        user = User.objects.get(id=request.session['id'])
        print user.id
        context={
            # 'user' : User.objects.get(id=request.session['id']),
            # 'travel' : Travel.objects.get(id = request.session['id']),
            'your_trip' : Travel.objects.filter(users = user),
            # print "your trips"
            'other_user' : Travel.objects.all().exclude(users = user)
            # print "other user trips"

        }
    
    # return render(request,'belt/success.html',{"user" : User.objects.get(id=id)})
    return render(request,'belt/success.html',context)

def addplan(request):
    return render(request,'belt/addplan.html')

def add (request):
    destination =  request.POST['destination']
    description = request.POST['description']
    datefrom = request.POST['datefrom']
    dateto = request.POST['dateto']
    user_id = request.session['id']
    # errors = Travel.objects.validatetravel(request.POST, user_id)


    if 'id' in request.session:
        user_id = request.session['id']
        print "inside add"
        travel = Travel.objects.validatetravel(request.POST, user_id)
        print travel
        

        if travel == False:
            for error in travel[1]:
                # messages.error(request, error, extra_tags=tag)
                messages.error(request,error[1])
                return redirect('/add')
        else:
            return redirect('/travels')        
    return redirect('/travels')


def join(request,id):
    user = User.objects.get(id=request.session['id'])
    travel = Travel.objects.get(id = id)
    travel.users.add(user)
    
    return redirect('/travels')


def destination(request,id):
    context= {
        'travel' : Travel.objects.get(id = id),

    }
    return render(request,'belt/destination.html',context)



def logout(request):
    request.session.clear()
    return redirect('/')