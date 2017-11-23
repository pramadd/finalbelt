from __future__ import unicode_literals

from django.db import models
from datetime import datetime,date
# Create your models here.
import bcrypt
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')


class UserManager(models.Manager):

#validating registration
    def validatereg(self,postData):
        errors = {}
        if len(postData['first_name']) < 3 :
            errors['first_name'] = "first name must be atleast 3 characters"

        if len(postData['alias']) < 3 :
            errors['alias'] = "last name must be atleast 3 characters"

        if not EMAIL_REGEX.match(postData['email']):  
            errors['email'] = "Invalid email Address!"

        if len(postData['password']) < 8 :
            errors['password'] = "password must be atleast 8 characters"

        if postData['confirm_password'] != postData['password']:
            errors['confirm_password'] = "passwords does not match"

        if len(postData['first_name']) < 1 or len(postData['alias']) < 1  or len(postData['email']) < 1 or  len(postData['password']) < 1  or len(postData['confirm_password']) < 1 :
            errors['empty'] = "Fields cant be empty"

        return errors


#validating login
    def validatelogin(self,postData):
        errors = {}
        hashed_password = postData['password'].encode()

        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) < 1 :
            errors['email'] = "Invalid email Address!"

        if len(postData['password']) < 8 :
            errors['password'] = "password must be atleast 8 characters"

        try:
            user = User.objects.get(email = postData['email'])    
            if (user):
                if bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
                    print "succesfully logged in"
                else:
                    errors['password']= "password do not match"

        except:
            errors['email_not_exist'] = "email doesn't exist"

        return errors    

class TravelManager(models.Manager):

#validating travel  
    def validatetravel(self,postData,user_id):
        errors = {}

        if len(postData['destination']) or len(postData['description']) or len(postData['datefrom']) or len(postData['dateto']) < 1 :
            errors['empty'] = "Fields cannot be empty! "

        destination = postData['destination']
        description = postData['description']
        datefrom = datetime.strptime(postData['datefrom'], '%Y-%m-%d').date()
        print datefrom
        dateto = datetime.strptime(postData['dateto'], '%Y-%m-%d').date()
        todaydate = datetime.now().date()
        user = User.objects.get(id=user_id)

        if datefrom or dateto < todaydate :
            errors['dates'] = " dates should be futur -dated"

        # from datetime import datetime, date
        # date_input = input('Date (mm/dd/yyyy): ')
        # try:
        #     valid_date = datetime.strptime(date_input, '%m/%d/%Y').date()
        #     if not (date(2014, 1, 1) <= valid_date <= date(2014, 8, 7)):
        #         raise ValueError('Date out of range')
        # except ValueError:
        # print('Invalid date!')


        # datefrom = datetime.strptime('datefrom', '%m/%d/%Y').date()
        # dateto = datetime.strptime('dateto', '%m/%d/%Y').date()

        if dateto < datefrom :
            errors['dateto'] = "enter a valid future date"

        else:
            print "******* inside save "
            trip = Travel.objects.create(destination = destination ,description = description ,datefrom = datefrom ,dateto = dateto,user = user)
           # request.session['id'] = user.id
            trip.users.add(user)
            trip.save()
            return True






class User(models.Model):
    first_name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length=255)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class Travel(models.Model):
    destination =  models.CharField(max_length = 255)
    description = models.TextField()
    datefrom = models.DateTimeField()
    dateto = models.DateTimeField()
    user = models.ForeignKey(User,related_name = "trips")
    #one user can create many trips
    users = models.ManyToManyField(User,related_name ="userstrips")
    #one user can have many trips & each trip can have many users
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TravelManager()