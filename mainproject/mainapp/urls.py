from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('loguser/',views.loguser,name='loguser'),
    path('otp/',views.otp_check,name='otp'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.create_profile,name='profile'),
    path('post/',views.my_post,name='post'),
    path('view_profile/<str:name>',views.view_profile,name='post'),
    path('follow/',views.Follow,name='follow'),
    path('like/',views.like_check,name='like'),
    path('search/',views.Search,name='search'),
    path('prof/',views.Own_profile,name='own_profile'),
    path('showcomment/<str:post_id>',views.Showcomment,name='showcomment'),
    path('createcomment/',views.Createcomment,name='createcomment'),
    path('save/',views.handle_compressed_image,name='save_post'),
    path('editprof/',views.Own_edit_profile,name='own_edit_profile'),
    path('deletepic/',views.Deletepic,name='Deletepic'),
    path('forgot/',views.forgotpassword,name='forgot'),
    path('forgot_otp/',views.forgot_otp_check,name='forgot_otp'),
]

