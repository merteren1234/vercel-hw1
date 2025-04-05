from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('add',views.add,name='home'),
    path('loginAttemp',views.loginAttemp,name='home'),
    path('login',views.loginPage,name='loginPage'),
    path('admin/createAccount',views.createAccount,name='registerPage'),
    path('profile',views.profilePage,name='profilePage'),
    path('logout',views.logout,name='logout'),
    path('admin/',views.adminPage),
    path('admin/addProduct',views.addProduct,name='addProduct'),
    path('product',views.productPage,name='productPage'),
    path('addComment',views.addComment,name='addComment'),
    path('givePoint',views.givePoint,name='givePoint'),
    path('admin/deleteAccount',views.deleteAccount,name='deleteAccount'),
    path('admin/deleteProduct',views.deleteProduct,name='deleteProduct'),
]
