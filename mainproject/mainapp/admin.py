from django.contrib import admin
from .models import CustomUser,OTP,Profile,demo,Post,Followerscount,Like_post,Comment

# Register your models here.

#Register Custom user
admin.site.register(CustomUser)

admin.site.register(OTP)
admin.site.register(Profile)
admin.site.register(demo)
admin.site.register(Post)
admin.site.register(Followerscount)
admin.site.register(Like_post)
admin.site.register(Comment)
