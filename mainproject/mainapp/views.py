from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser,OTP,Profile,demo,Post,Followerscount,Like_post,Comment
from django.contrib import auth
from django.contrib import messages
import random
import requests
import json
import email.utils as email_utils
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse,HttpResponseNotFound
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


#Default images
default_image = 'default.png'
default_cover_image ='default_cover_img.png'

# Create your views here.


#If 404 error occur serve this page
def page_not_found(request,exception):
    return render(request,'404.html')

@login_required(login_url='/loguser/')
def home(request):
    all_post=Post.objects.filter(postshow=True).all()
    all_post = list(all_post)
    random.shuffle(all_post)
    user_profile=Profile.objects.filter(user=request.user).first()
    return render(request,'home.html',{'profile':user_profile,'name':request.user,'all_post':all_post})

def send_otp(name,email,otp):
    url = "https://control.msg91.com/api/v5/email/send"
    payload = {
    'to': [{'name': name, 'email': email}],
    'from': {'name': 'pritimaya', 'email': 'suport@kapilasachhatrabasa.in'},
    'variables': {'name': name, 'OTP': otp},
    'domain': 'kapilasachhatrabasa.in',
    'template_id': 'SEND_OTP_FOR_VERIFICATION'
     }
    payload=json.dumps(payload)
    headers = {
       "Content-Type": "application/JSON",
       "Accept": "application/json",
       "authkey": "396373AgC8FX3CzNwJ645a623bP1"
        }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
       pass
    else :
       pass
    return None

def signup(request):
    if request.method=='POST':
        email=request.POST['email']
        #normalize email
        parsed_email = email_utils.parseaddr(email)[1]
        email = parsed_email.lower()
        
        #if this user is already blocked
        otp_object=OTP.objects.filter(email=email).first()
        if otp_object and otp_object.failed_attempts >= 3 and otp_object.locked_until > timezone.now():
            messages.info(request,'Account Has Been locked For 24 hours')
            return redirect('/signup/')
        
        password=request.POST['password']
        password_again=request.POST['password-again']
        name=request.POST['name']
        if not email or not password or not name or not password_again:
           messages.info(request,'Please fill all fields')
           return redirect('/signup/')

        if password!=password_again:
            messages.info(request,'Password Not Matched')
            return redirect('/signup/') 
        
        user=CustomUser.objects.filter(email=email).first()
        if user:
            messages.info(request,'THIS USER IS ALREADY EXIST')
            return redirect('/signup/')
        request.session['email'] =email
        request.session['password'] = password
        request.session['name']=name
        otp=random.randint(100000,999999)
        send_otp(name,email,otp)
        myotp=OTP.objects.filter(email=email).first()
        if myotp:
            myotp.otp=otp
            myotp.save()
        else:    
            OTP.objects.create(otp=otp,email=email)
        return redirect('otp')       
    return render(request,'signup.html')

def loguser(request):
    if request.method=='POST':
        email=request.POST['email']
        #normalize email
        parsed_email = email_utils.parseaddr(email)[1]
        email = parsed_email.lower()
        #check if user is blocked for 24 hours
        otp_object=OTP.objects.filter(email=email).first()
        if otp_object and otp_object.failed_attempts >= 3 and otp_object.locked_until > timezone.now():
            messages.info(request,'Account Has Been locked For 24 hours')
            return redirect('/loguser/')

        password=request.POST['password']
        user=CustomUser.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            request.session['email'] = email
            request.session['password'] = password
            otp=random.randint(100000,999999)
            otp_object=OTP.objects.filter(email=email).first()
            otp_object.otp=otp
            otp_object.save()
            send_otp('chiku',email,otp)
            return redirect('/otp/')
        messages.info(request,'PASSWORD OR EMAIL ID IS WRONG')
        return redirect('loguser')
    return render(request,'login.html')

        
def otp_check(request):
    if request.method=='POST':
        otp=request.POST['otp']
        mail=request.session.get('email')
        otp_object=OTP.objects.filter(email=mail).first()
        if otp_object and otp_object.failed_attempts >= 3 and otp_object.locked_until > timezone.now():
            messages.info(request,'Account Has Been locked For 24 hours')
            return redirect('otp')
        if otp_object:
            if otp_object.otp==otp:
                password=request.session.get('password')
                mymail=request.session.get('email')
                user=CustomUser.objects.filter(email=mymail).first()
                if user:
                    my_user=auth.authenticate(email=mymail,password=password)
                    auth.login(request,my_user)
                    #set otp attempts to 0
                    otp_object.failed_attempts = 0
                    otp_object.locked_until = None
                    otp_object.save()
                    return redirect('/')
                else:
                   my_user=CustomUser.objects.create_user(email=mymail,password=password)
                   otp_object.user=my_user
                   #set otp attempts to 0
                   otp_object.failed_attempts = 0
                   otp_object.locked_until = None
                   otp_object.save()
                   name=request.session.get('name')
                   Profile.objects.create(user=my_user,id=my_user.id,name=name)
                   my_user=auth.authenticate(email=mymail,password=password)
                   if my_user:
                      auth.login(request,my_user)
                      return render(request,'ownprofile.html')
            else:
                otp_object.failed_attempts += 1
                # Lock account for 24 hours
                if otp_object.failed_attempts == 3:
                    otp_object.locked_until = timezone.now() + timedelta(hours=24)
                    otp_object.save()
                    messages.info(request,'Account Has Been locked For 24 hours')
                    return redirect('otp')
                
                #if next 24 hour again give wrong otp handle here
                if otp_object.failed_attempts>3:
                    #1 failed attempt for this time
                    otp_object.failed_attempts = 1
                    otp_object.locked_until = None

                otp_object.save()
                if otp_object.failed_attempts==2:
                    messages.info(request,'Last Attempt')
                    return redirect('otp')
                
                messages.info(request,'OTP NOT MATCHED TRY again')
                return redirect('otp')
        messages.info(request,'MAIL IS INCORRECT')
        return redirect('otp')
 
    return render(request,'otp.html')    

@login_required(login_url='/loguser/')
def create_profile(request):
    if request.method=='POST':
      myprofile=Profile.objects.filter(user=request.user).first()
      #get the profile image
      if request.FILES.get('profile_image'):
        profile_image=request.FILES.get('profile_image')
      else:
        profile_image = default_image

      #get the cover image  
      if request.FILES.get('cover_image'):
        cover_image=request.FILES.get('cover_image')
        print(cover_image)
      else:
        cover_image = default_cover_image

      name=request.POST['name']  
      about=request.POST['about']
      school=request.POST['school']
      myprofile.profileimage=profile_image
      myprofile.backgroundimage=cover_image
      #if no name passed used signup time name
      name=name if name else myprofile.name
      myprofile.name=name
      myprofile.about=about
      myprofile.current_study=school
      myprofile.save()
      return JsonResponse({"message":"Success done"})
    
    #if user wants to edit his profile he will come here
    else:
        myprofile=Profile.objects.filter(user=request.user).first()
        name=myprofile.name
        about=myprofile.about
        school=myprofile.current_study
        context={
            'name':name,
            'about':about,
            'school':school
        }
        return render(request,'ownprofile.html',context)

@login_required(login_url='/loguser/')
def logout(request): 
        auth.logout(request)
        return redirect('/loguser/')

#forgot otp
def forgot_otp_check(request):
    if request.method=='POST':
        otp=request.POST['otp']
        password=request.POST['password'] 
        mail=request.session.get('email')
        otp_object=OTP.objects.filter(email=mail).first()
        if otp_object:
            if otp_object.otp==otp:
                user=CustomUser.objects.filter(email=mail).first()
                user.set_password(password)
                user.save()
                otp_object.failed_attempts=0
                otp_object.otp=random.randint(100000,999999)
                otp_object.save()
                my_user=auth.authenticate(email=mail,password=password)
                auth.login(request,my_user)
                return redirect('/')
            else:
                otp_object.failed_attempts+=1
                #reassign new otp after 3 failure attempt
                if otp_object.failed_attempts>=3:
                    otp_object.failed_attempts=0
                    otp_object.otp=random.randint(100000,999999)
                    otp_object.save()
                otp_object.save()
                messages.info(request,'OTP NOT MATCHED TRY AGAIN')
                return redirect('forgot_otp')
    return render(request,'forgototp.html')

#for got password
def forgotpassword(request):
    if request.method=='POST':
        email=request.POST["email"]
        parsed_email = email_utils.parseaddr(email)[1]
        email = parsed_email.lower()
        request.session['email'] =email
        user=CustomUser.objects.filter(email=email).first()
        if user:
            otp=random.randint(100000,999999)
            otp_object=OTP.objects.filter(email=email).first()
            otp_object.otp=otp
            otp_object.save()
            send_otp('chiku',email,otp)
            return redirect('forgot_otp')
        else:
           messages.info(request,'User Not Exist')
           return redirect('forgot')
    return render(request,'forgotpassword.html')    

@login_required(login_url='/loguser/')        
def my_post(request):
    return render(request, 'post.html') 

def view_profile(request,name):
    my_user=request.user
    person_profile=Profile.objects.filter(name=name).first()
    person_obj=person_profile.user
    follower_exist=Followerscount.objects.filter(follower=my_user,user=person_obj).first()
    allfollow=Followerscount.objects.filter(user=person_obj).all()
    allfollow=len(allfollow)
    user_profile=person_profile
    if follower_exist:
        button='UNFOLLOW'
    else:
        button='FOLLOW'    
    person_id=person_profile.user.id
    context={
        'person_id':person_id,
        'myuser':my_user,
        'button':button,
        'number':allfollow,
        'profile':user_profile

    }
    return render(request,'studentprofile.html',context)

@login_required(login_url='/loguser')
def Follow(request):
    current_user=request.user
    user_id=request.GET.get('myuser')
    user=CustomUser.objects.filter(id=user_id).first()
    user_profile=Profile.objects.filter(user=user).first()
    #user_name=user_profile.name
    follower_exist=Followerscount.objects.filter(follower=current_user,user=user).first()
    if follower_exist:   
        follower_exist.delete()
        return redirect(f'/prof/?myuser={user_id}')
    else:
        Followerscount.objects.create(follower=current_user,user=user)
        return redirect(f'/prof/?myuser={user_id}')

@login_required(login_url='/loguser')
def like_check(request):
    user=request.user
    like_id=request.GET.get('like_id')
    current_post=Post.objects.filter(id=like_id).first()
    like=Like_post.objects.filter(post_id=like_id,like_user=user).first()
    if like:
        like.delete()
        current_post.no_of_like-=1
        current_post.save()
    else:
        new_like=Like_post.objects.create(post_id=like_id,like_user=user)
        current_post.no_of_like+=1
        current_post.save()
    data = {
        'likes': current_post.no_of_like
    }
    return JsonResponse(data)

#Add comments
@login_required(login_url='/loguser')     
def Showcomment(request,post_id):
        user=request.user
        current_post=Post.objects.filter(id=post_id).first()
        allcomments=Comment.objects.filter(comment_post=current_post)
        recent_user=Profile.objects.filter(user=user).first()
        user=request.user
        context={
        'user':user,
        'allcomments':allcomments,
        'post_id':post_id,
        'recent_user':recent_user
        }
        return render(request,'comment.html',context)

#create comment
@login_required(login_url='/loguser') 
def Createcomment(request):
    if request.method=="POST":
        comment=request.POST['comment']
        post_id=request.POST['id']
        user=request.user
        user_profile=Profile.objects.filter(user=user).first()
        current_post=Post.objects.filter(id=post_id).first()
        Comment.objects.create(text=comment,comment_by=user_profile,comment_post=current_post)
        current_post.no_of_coment+=1
        user_profile.comment_by_user+=1
        current_post.save()
        user_profile.save()
        return JsonResponse({'success': True}) 

    
@login_required(login_url='/loguser')
def Search(request):
    if request.method=='POST':
        name=request.POST['searchname']
        users=Profile.objects.filter(name__icontains=name).all()
        return render(request,'search.html',{'profiles':users})
    else:
        return redirect('/')

@login_required(login_url='/loguser')    
def Own_profile(request):
    user_id=request.GET.get('myuser')
    uy=CustomUser.objects.filter(id=user_id).first()
    user_profile=Profile.objects.filter(user=uy).first()
    my_user=request.user
    #person_profile=Profile.objects.filter(name=n).first()
    person_obj=user_profile.user
    follower_exist=Followerscount.objects.filter(follower=my_user,user=person_obj).first()
    allfollow=Followerscount.objects.filter(user=person_obj).all()
    allfollow=len(allfollow)
    #if recent user is owner of recent pic
    if uy==my_user:
        button='EDIT PROFILE'
    else: 
      #if follow before   
      if follower_exist:
         button='UNFOLLOW'
      #if not follow before   
      else:
         button='FOLLOW'   
          
    person_id=user_profile.user.id
    context={
        'person_id':person_id,
        'myuser':my_user,
        'button':button,
        'number':allfollow,
        'profile':user_profile,
        'user':uy

    }    
    return render(request,'new_profile.html',context)
#Show your Own profile
@login_required(login_url='/loguser') 
def Own_edit_profile(request):
    uy=request.user
    user_profile=Profile.objects.filter(user=uy).first()
    allfollow=Followerscount.objects.filter(user=uy)
    allfollow=len(allfollow)
    posts=Post.objects.filter(Q(post_by=uy) & Q(postshow=True))
    context={
        'posts':posts,
        'number':allfollow,
        'profile':user_profile,
    }    
    return render(request,'owneditprofile.html',context)
#Delete a picture
@login_required(login_url='/loguser') 
def Deletepic(request):
    if request.GET.get('value'):
        ownuser=request.user
        value = request.GET.get('value')
        deletephoto=Post.objects.filter(Q(id=value) & Q(post_by=ownuser)).first()
        deletephoto.postshow=False
        deletephoto.save()
        return redirect('/')   
        

#handle compressed image
@login_required(login_url='/loguser')    
def handle_compressed_image(request):
    if request.method == "POST":
        current_profile=Profile.objects.filter(user=request.user).first()
        text_data = request.POST.get("text_data")
        image_data = request.FILES.get("image_data")
        Post.objects.create(my_post=image_data,post_by=request.user,poster_profile=current_profile,about=text_data)
        return JsonResponse({"message":"Success done"})
        


    