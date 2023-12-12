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

# Create your views here.


#If 404 error occur serve this page
def page_not_found(request,exception):
    return render(request,'404.html')

@login_required(login_url='/loguser/')
def home(request):
    all_post=Post.objects.all()
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
    print(response)
    if response.status_code == 200:
       print(response.text)
    else :
       print(response.text)
    return None

def signup(request):
    if request.method=='POST':
        email=request.POST['email']
        #normalize email
        parsed_email = email_utils.parseaddr(email)[1]
        email = parsed_email.lower()

        password=request.POST['password']
        name='chiku'
        user=CustomUser.objects.filter(email=email).first()
        if user:
            messages.info(request,'THIS USER IS ALREADY EXIST')
            return redirect('/signup/')
        request.session['email'] = email
        request.session['password'] = password
        otp=random.randint(100000,999999)
        print(otp)
        send_otp(name,email,otp)
        myotp=OTP.objects.filter(email=email).first()
        print(myotp)
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

        password=request.POST['password']
        print(email)
        user=CustomUser.objects.filter(email=email).first()
        print('no')
        if user and check_password(password, user.password):
            print('hy ok')
            request.session['email'] = email
            request.session['password'] = password
            otp=random.randint(100000,999999)
            print(otp)
            otp_object=OTP.objects.filter(email=email).first()
            print('noooooo')
            otp_object.otp=otp
            print('mgkgkg')
            otp_object.save()
            print('helo okkk')
            send_otp('chiku',email,otp)
            print('otp')
            return redirect('/otp/')
        print('hy')
        messages.info(request,'PASSWORD OR EMAIL ID IS WRONG')
        return redirect('loguser')
    return render(request,'login.html')

        
def otp_check(request):
    if request.method=='POST':
        otp=request.POST['otp']
        mail=request.session.get('email')
        print('okkkk')
        otp_object=OTP.objects.filter(email=mail).first()
        if otp_object:
            if otp_object.otp==otp:
                password=request.session.get('password')
                mymail=request.session.get('email')
                user=CustomUser.objects.filter(email=mymail).first()
                if user:
                    my_user=auth.authenticate(email=mymail,password=password)
                    auth.login(request,my_user)
                    return redirect('/')
                else:
                   my_user=CustomUser.objects.create_user(email=mymail,password=password)
                   otp_object.user=my_user
                   otp_object.save()
                   my_profile=Profile.objects.create(user=my_user,id=my_user.id)
                   my_user=auth.authenticate(email=mymail,password=password)
                   print('nhl')
                   if my_user:
                      auth.login(request,my_user)
                      return redirect('profile')
            else:
                messages.info(request,'OTP NOT MATCHED TRY again')
                return redirect('otp')
        messages.info(request,'MAIL IS INCORRECT')
        return redirect('otp')

    return render(request,'otp.html')    

@login_required(login_url='/loguser/')
def create_profile(request):
    myprofile=Profile.objects.filter(user=request.user).first()
    if request.method=='POST':
      print('hyyy')
      if request.FILES.get('compressed_image'):
        image=request.FILES.get('compressed_image')
        print('image load')
      else:
        image=myprofile.profileimage  
        print('image not load')
      name=request.POST['name']  
      about=request.POST['about']
      school=request.POST['school']
      myprofile.profileimage=image
      myprofile.name=name
      myprofile.about=about
      myprofile.current_study=school
      myprofile.save()
      print(' image created succefully')
      return redirect('/')
    return render(request, 'ownprofile.html',{'myprofile':myprofile})
  
@login_required(login_url='/loguser/')
def logout(request): 
        auth.logout(request)
        return redirect('/loguser/')

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
    print('okk')
    user_id=request.GET.get('myuser')
    print(user_id)
    user=CustomUser.objects.filter(id=user_id).first()
    user_profile=Profile.objects.filter(user=user).first()
    #user_name=user_profile.name
    follower_exist=Followerscount.objects.filter(follower=current_user,user=user).first()
    print(follower_exist,'no')
    if follower_exist:   
        follower_exist.delete()
        print('sucess')
        return redirect(f'/prof/?myuser={user_id}')
    else:
        Followerscount.objects.create(follower=current_user,user=user)
        print('done')
        return redirect(f'/prof/?myuser={user_id}')
    
@login_required(login_url='/loguser')
def home2nd(request):
    all_post=Post.objects.all()
    return render(request,'home2.html',{'all_post':all_post,'name':request.user})

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
        print('like remove')
    else:
        new_like=Like_post.objects.create(post_id=like_id,like_user=user)
        current_post.no_of_like+=1
        current_post.save()
        print('like')
    data = {
        'likes': current_post.no_of_like
    }
    return JsonResponse(data)

#Add comments
@login_required(login_url='/loguser')     
def Showcomment(request,post_id):
        post_id=post_id
        print(post_id)
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
        print("start")
        comment=request.POST['comment']
        post_id=request.POST['id']
        print(comment,post_id)
        user=request.user
        user_profile=Profile.objects.filter(user=user).first()
        current_post=Post.objects.filter(id=post_id).first()
        print(user_profile,current_post,'how')
        Comment.objects.create(text=comment,comment_by=user_profile,comment_post=current_post)
        user_profile.comment_by_user+=1
        user_profile.save()
        print("sucess") 
        return JsonResponse({'success': True}) 

    
@login_required(login_url='/loguser')
def Search(request):
    if request.method=='POST':
        name=request.POST['searchname']
        print(name)
        users=Profile.objects.filter(name__icontains=name).all()
        return render(request,'search.html',{'profiles':users})
    else:
        return redirect('/')

@login_required(login_url='/loguser')    
def Own_profile(request):
    user_id=request.GET.get('myuser')
    print(user_id)
    print(678)
    uy=CustomUser.objects.filter(id=user_id).first()
    print(uy)
    user_profile=Profile.objects.filter(user=uy).first()
    my_user=request.user
    print(my_user)
    print('neo')
    #person_profile=Profile.objects.filter(name=n).first()
    person_obj=user_profile.user
    follower_exist=Followerscount.objects.filter(follower=my_user,user=person_obj).first()
    allfollow=Followerscount.objects.filter(user=person_obj).all()
    allfollow=len(allfollow)
    print(allfollow)
    if follower_exist:
        button='UNFOLLOW'
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
    print('up to')
    return render(request,'new_profile.html',context)

#handle compressed image
@login_required(login_url='/loguser')    
def handle_compressed_image(request):
    if request.method == "POST":
        current_profile=Profile.objects.filter(user=request.user).first()
        text_data = request.POST.get("text_data")
        #print(text_data)
        #print('jio')
        image_data = request.FILES.get("image_data")
        Post.objects.create(my_post=image_data,post_by=request.user,poster_profile=current_profile,about=text_data)
        return JsonResponse({"message":"Success done"})
        


    