from django.shortcuts import render,redirect
from django.http import HttpResponse
from .connectMongo import *
from .jwtToken import *
# Create your views here.

def home(request):
    proList=listAllProducts()
    productList=[]
    try:
        cat=request.GET['category']
        for pro in proList:
            if pro['category']==cat:
                productList.append(pro)
    except:
        productList=proList

    
    for product in productList:
        r=0
        for i in product['rates']:
            r+=i['point']
        if len(product['rates']) != 0:
            product['rating']=r/len(product['rates'])
        else:
            product['rating']=0
    try:   
        token=request.COOKIES.get('JWT_token')
        token_stat=verification(token)
        if token_stat['stat']:
            if token_stat['token']['username']=='admin':
               return render(request,'home.html',{'isLoginned':1,'products':productList,'isAdmin':1}) 
            return render(request,'home.html',{'isLoginned':1,'products':productList})
        else:
            return render(request,'home.html',{'isLoginned':0,'products':productList})
    except:
        return render(request,'home.html',{'isLoginned':0,'products':productList})


def productPage(request):
    try:
        product=showProduct(request.GET['id'])
        if product=={}:
            return redirect('/')
        r=0
        for i in product['rates']:
            r+=i['point']
        if len(product['rates']) != 0:
            product['rating']=r/len(product['rates'])
        else:
            product['rating']=0
        return render(request,"product.html",{'product':product})
    except:
        return redirect('/')


def add(request):
    val1=int(request.POST['val1'])
    val2=int(request.POST['val2'])
    res=val1+val2
    return render(request,'result.html',{'result':val1+val2})



def loginPage(request):
    try:
        if request.GET['status']=='1' :
            return render(request,'login.html',{'status':1})
        elif request.GET['status']=='2':
            return render(request,'login.html',{'status':2})
        elif request.GET['status']=='3':
            return render(request,'login.html',{'status':3})
        else:
            return render(request,'login.html',{'status':0})
    except:
        return render(request,'login.html',{'status':0})



def loginAttemp(request):
    if request.POST['username']=="":
        return redirect('/login?status=2')
    username=request.POST['username']
    password=request.POST['password'] 
    status=isCredentialsCorrect(username,password)
    if status:
        token=create_access_token(username)
        response =redirect('/')
        response.set_cookie(key="JWT_token",value=token)
        return response
    return redirect('/login?status=1')

def logout(request):
    response =redirect('/login')
    response.set_cookie(key="JWT_token",value="")
    return response








def createAccount(request):
    username=request.POST['username']
    password=request.POST['password']
    status=addUser(username,password)
    if(status == 0):
        return redirect('/admin?createacc=0')
    else:
        return redirect('/admin?createacc=1')
    
def deleteAccount(request):
    username=request.POST['username']
    x=deleteAccountFromDatabase(username)
    if x==0:
        return redirect('/admin?statusdeleteUser=0')
    return redirect('/admin?statusdeleteUser=1')

def deleteProduct(request):
    name=request.POST['name']
    x=deleteProductFromDatabase(name)
    if x==0:
        return redirect('/admin?statusdeleteProduct=0')
    return redirect('/admin?statusdeleteProduct=1')



def profilePage(request):
    try:
        token=request.COOKIES.get('JWT_token')
        token_stat=verification(token)
        if token_stat['stat']:
            username=token_stat['token']['username']
            user_data=showUser(username)
            averageRating=0
            for i in user_data['rates']:
                averageRating+=i['point']
            if len(user_data['rates'])!=0:
                averageRating/=len(user_data['rates'])
            return render(request,'profile.html',{'username':user_data['username'],'averageRating':averageRating,'reviews':user_data['reviews']})
        else:
            return redirect('/login?status=3')
    except:
        return redirect('/login')
    

def adminPage(request):
    token=request.COOKIES.get('JWT_token')
    token_stat=verification(token)
    if token_stat['stat']:
        if token_stat['token']['username']=='admin':
            try :
                return render(request,'admin.html',{'deleteUserS':int(request.GET['statusdeleteUser'])})
            except:
                x=0
            try :
                return render(request,'admin.html',{'deleteProductS':int(request.GET['statusdeleteProduct'])})
            except:
                x=0
            try :
                return render(request,'admin.html',{'addProductS':int(request.GET['statusaddProduct'])})
            except:
                x=0
            try:
                return render(request,'admin.html',{'createaccstatus':int(request.GET['createacc'])})
            except:
                return render(request,'admin.html')
    return render(request,"403.html",status=403)
    

def addProduct(request):
    name=request.POST['name']
    description=request.POST['description']
    price=request.POST['price']
    seller=request.POST['seller']
    image=request.POST['imageurl']
    battery_life=request.POST['battery_life']
    age=request.POST['age']
    size=request.POST['size']
    material=request.POST['material']
    category=request.POST['category']
    stat=addProducttodb(name,description,price,seller,image,battery_life,age,size,material,category)

    return redirect('/admin?statusaddProduct='+str(stat))

def addComment(request):
    stat=verification(request.COOKIES.get('JWT_token'))
    if stat['stat']==0:
        return redirect('/login')
    name=request.POST['id']
    comment=request.POST['comment']
    review(name,comment,stat['token']['username'])
    return redirect('/product?id='+name)

def givePoint(request):
    stat=verification(request.COOKIES.get('JWT_token'))
    if stat['stat']==0:
        return redirect('/login')
    name=request.POST['id']
    point=request.POST['point']
    rate(name,int(point),stat['token']['username'])
    return redirect('/product?id='+name)
