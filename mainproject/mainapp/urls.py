from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('loguser/',views.loguser,name='loguser'),
    path('forgot/',views.forgotpassword,name='forgot'),
    path('signup_otp/',views.Signup_otp_check,name='signup_otp'),
    path('login_otp/',views.Login_otp_check,name='login_otp'),
    path('forgot_otp/',views.Forgot_otp_check,name='forgot_otp'),
    path('logout/',views.logout,name='logout'),
    path('editprof/',views.create_profile,name='profile'),
    path('post/',views.my_post,name='post'),
    path('follow/',views.Follow,name='follow'),
    path('like/',views.like_check,name='like'),
    path('search/',views.Search,name='search'),
    path('prof/',views.Other_profile,name='Other_profile'),
    path('showcomment/<str:post_id>',views.Showcomment,name='showcomment'),
    path('createcomment/',views.Createcomment,name='createcomment'),
    path('save/',views.handle_compressed_image,name='save_post'),
    path('ownprofile/',views.Own_profile,name='Own_profile'),
    path('deletepic/',views.Deletepic,name='Deletepic'),
    
]

