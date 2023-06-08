from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def add_receipe(request):
    if request.method == 'POST':
        data=request.POST
        receipe_image=request.FILES.get('receipe_image')
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
        Receipe.objects.create(
            receipe_image=receipe_image,
            receipe_description=receipe_description,
            receipe_name=receipe_name,
        )
        return redirect('/get_receipe/')
    query_set=Receipe.objects.all()
    context ={'receipes' : query_set }
    return render(request,'home/add_receipe.html',context)

@login_required(login_url="/login/")
def get_receipe(request):
    query_set=Receipe.objects.all()
    query_set = query_set.order_by('-id')
    if request.GET.get('search'):
        query_set=query_set.filter(receipe_name__icontains = request.GET.get('search'))
    context ={'receipes' : query_set }
    return render(request,'home/receipe.html',context)

@login_required(login_url="/login/")
def delete_receipe(request , id):
    query_set=Receipe.objects.get(id = id)
    query_set.delete()
    return redirect('/get_receipe/')

@login_required(login_url="/login/")
def update_receipe(request, id):
    query_set = Receipe.objects.get(id=id)
    print( query_set)
    if request.method == 'POST':
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = request.POST.get('receipe_name')
        receipe_description = request.POST.get('receipe_description')
        if receipe_image:
            query_set.receipe_image = receipe_image
        query_set.receipe_name = receipe_name
        query_set.receipe_description = receipe_description
        print(query_set)
        query_set.save()
        return redirect('/get_receipe/')
    context = {'receipe': query_set}
    return render(request, 'home/update_receipe.html', context)

def login_page(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password = request.POST.get('user_password')

        if not User.objects.filter(username = username ).exists():
            messages.error(request,"invalid credentials")
            return redirect('/login')

        user =authenticate(username=username,password=password)
        if user is None:
            messages.error(request,"invalid password")
            return redirect('/login')
        else:
            login(request,user)
            return redirect('/get_receipe')
    return render(request,'home/login.html')

@login_required(login_url="/login/")
def logout_page(request):
    logout(request)
    return redirect('/login')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username =request.POST.get('username')
        user_password = request.POST.get('user_password')

        user=User.objects.filter(username = username)
        if user.exists():
            messages.info(request,"Username taken by already by someone else")
            return redirect('/register')

        user = User.objects.create(
            first_name =first_name,
            last_name=last_name,
            username=username
        ) 
        user.set_password(user_password)
        user.save()
        messages.info(request,"Sucessfully registration")
        return redirect('/register')
    return render(request,'home/register.html')
       

