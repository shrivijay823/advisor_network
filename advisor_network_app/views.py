import jwt,datetime
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect, response
from django.contrib.auth import authenticate,logout,login
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import never_cache
from .models import Advisor, booking
from django.urls import reverse
# Create your views here.
def error_404(request, exception):
        return render(request,'advisor_network_app/page404.html')

def Check_Autherized(request,user_id):
    token=request.COOKIES.get('jwt')
    if not token:
        logout(request)
        return False
    if token:
        try:
            payload=jwt.decode(token,'secret',algorithms='HS256')
            if payload['id']!=user_id:
                print('user not matching')
                logout(request)
                return False
            else:return True
        except jwt.exceptions.ExpiredSignatureError:
            logout(request)
            return False


class signinupview(View):
    def get(self,request,auth):
        if request.user.is_authenticated:
            user=User.objects.filter(username=request.user.username)[0]
            if user.is_superuser or auth=='logout':
                logout(request)
                response=HttpResponseRedirect(reverse('advisor_network_app:signupin',kwargs={'auth':'login'}))
                response.delete_cookie('jwt')
                return response
            elif auth=='login':
                return HttpResponseRedirect(reverse('advisor_network_app:advview',kwargs={'id':request.user.id}))
            elif auth=='register':
                logout(request)
                return render(request,'advisor_network_app/signup.html')
            else:
                return render(request,'advisor_network_app/page404.html')
        else:
            if auth=='login':
                return render(request,'advisor_network_app/signin.html')
            elif auth=='register':
                return render(request,'advisor_network_app/signup.html')
            else:
                return render(request,'advisor_network_app/page404.html')
    @never_cache       
    def post(self,request,auth):
        form=request.POST
        op=form['operation']
        if op=='signup':
            user=User.objects.filter(username=form['usnm'])
            if user:
                return render(request,'advisor_network_app/signup.html',{'msg':'Account Already Exist!'})
            else:    
                myuser=User.objects.create_user(username=form['usnm'],email=form['email'],password=form['pwd'],first_name=form['flnm'],is_staff=1)
                myuser.save()
                user = authenticate(request, username=form['usnm'], password=form['pwd'])
                if user is not None:
                    login(request, user)
                    payload={
                    'id':myuser.id,
                    'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
                    'iat':datetime.datetime.utcnow()
                    }
                    token=jwt.encode(payload,'secret',algorithm='HS256')
                    response=HttpResponseRedirect(reverse('advisor_network_app:advview',kwargs={'id':myuser.id}))
                    response.set_cookie(key='jwt',value=token,httponly=True)
                    return response
                else:
                    return HttpResponse('error!')
        else:
            myuser=User.objects.filter(username=form['usnm'])
            if len(myuser)==0:
                print(len(myuser))
                return render(request,'advisor_network_app/signin.html',{'msg':'Username or password is incorrect','op':'signin'})
            if check_password(form['pwd'],myuser[0].password) and not myuser[0].is_superuser:
                user = authenticate(request, username=form['usnm'], password=form['pwd'])
                if user is not None:
                    login(request, user)
                    payload={
                    'id':myuser[0].id,
                    'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
                    'iat':datetime.datetime.utcnow()
                    }
                    
                    token=jwt.encode(payload,'secret',algorithm='HS256')
                    response=HttpResponseRedirect(reverse('advisor_network_app:advview',kwargs={'id':myuser[0].id}))
                    response.set_cookie(key='jwt',value=token,httponly=True)
                    return response
                else:
                   return HttpResponse('error!') 
            else:
                return render(request,'advisor_network_app/signin.html',{'msg':'Username or password is incorrect','op':'signin'})    

class index(View):
    @never_cache
    def get(self,request,id=0):
        if not Check_Autherized(request,id):
            return HttpResponseRedirect(reverse('advisor_network_app:signupin',kwargs={'auth':'login'}))
        token=request.COOKIES.get('jwt')
        payload=jwt.decode(token,'secret',algorithms='HS256')
        user=User.objects.filter(id=payload['id'])[0]
        if user.is_superuser:
            response=HttpResponseRedirect(reverse('advisor_network_app:signupin',kwargs={'auth':'login'}))
            response.delete_cookie('jwt')
            return response
        else:
            return HttpResponseRedirect(reverse('advisor_network_app:advview',kwargs={'id':payload['id']}))
    
    def advview(request,id):
        if not Check_Autherized(request,id):
            return HttpResponseRedirect(reverse('advisor_network_app:signupin',kwargs={'auth':'login'}))
        token=request.COOKIES.get('jwt')
        payload=jwt.decode(token,'secret',algorithms='HS256')
        user=User.objects.filter(id=payload['id'])[0]
        if user.is_superuser:
            response=HttpResponseRedirect(reverse('advisor_network_app:signupin',kwargs={'auth':'login'}))
            response.delete_cookie('jwt')
            return response
        else:
            adv=Advisor.objects.all()
            return render(request,'advisor_network_app/userpage.html',{'user_id':user.id,'adv':adv})
        
    def addadv(request):
        if request.method=='POST':
            propic = request.FILES['propic'] if 'propic' in request.FILES else False
            if propic:
                adv=Advisor(name=request.POST['name'],dp=propic)
            else:
                adv=Advisor(name=request.POST['name'])
            adv.save()
            return HttpResponseRedirect(reverse('advisor_network_app:adminview'))
        elif request.user.is_superuser:
            return render(request,'advisor_network_app/advexp.html',)
        else:
            return HttpResponseRedirect(reverse('advisor_network_app:adminview'))

    def bookcall(request,uid,aid):
        if not Check_Autherized(request,uid):return HttpResponseRedirect(reverse('advisor_network_app:signupin',kwargs={'auth':'login'}))
        if request.method == 'POST':
            form=request.POST
            datetime=form['date']+" "+form['time']
            bk=booking(bktime=datetime,advisor=Advisor.objects.get(id=aid),user=User.objects.get(id=uid))
            bk.save()
            return HttpResponseRedirect(reverse('advisor_network_app:advview',kwargs={'id':request.user.id}))
        else:
            adv=Advisor.objects.filter(id=aid)
            return render(request, 'advisor_network_app/book.html', {'adv':adv[0]})
        
    def allbooks(request,uid):
        if not Check_Autherized(request,uid):return HttpResponseRedirect(reverse('advisor_network_app:signupin',kwargs={'auth':'login'}))
        bk=booking.objects.filter(user_id=uid)
        adv=Advisor.objects.all()
        return render(request,'advisor_network_app/allbooks.html',{'bkings':bk,'adv':adv})


class adminview(View):
    def get(self,request):
        if request.user.is_authenticated:
            user=User.objects.filter(username=request.user.username)[0]
            if user.is_superuser:
                return HttpResponseRedirect(reverse('advisor_network_app:adminview'))
            else:
                return render(request,'advisor_network_app/adminlogin.html')
        else:
            adv=None
            return render(request,'advisor_network_app/adminlogin.html',{'adv':adv})
    @never_cache
    def post(self,request):
        form=request.POST
        admin=User.objects.filter(username=form['usnm'])
        if len(admin)==0:
            return render(request,'advisor_network_app/adminlogin.html',{'msg':'Username or password is incorrect',})

        if check_password(form['pwd'],admin[0].password) and admin[0].is_superuser:
                if request.user.is_authenticated:logout(request)
                user = authenticate(request, username=form['usnm'], password=form['pwd'])
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('advisor_network_app:adminview'))
                else:
                   return HttpResponse('error!') 
        else:
            return render(request,'advisor_network_app/adminlogin.html',{'msg':'Username or password is incorrect',})
    
    def adminpage(request):
        if request.user.is_authenticated:
            user=User.objects.filter(username=request.user.username)[0]
            if user.is_superuser:
                adv=Advisor.objects.all()
                return render(request,'advisor_network_app/userpage.html',{'adv':adv})
            else:
                return HttpResponseRedirect(reverse('advisor_network_app:adminlogin'))
        else:
            return HttpResponseRedirect(reverse('advisor_network_app:adminlogin'))

    def logout(request):
        logout(request)
        response=HttpResponseRedirect(reverse('advisor_network_app:adminlogin'))
        response.delete_cookie('jwt')
        return response