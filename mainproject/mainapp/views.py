from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, OTP, Profile, demo, Post, Followerscount, Like_post, Comment
from django.contrib import auth
from django.contrib import messages
import random
import requests
import json
import email.utils as email_utils
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse, HttpResponseNotFound
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


# Default images
default_image = 'default.png'
default_cover_image = 'default_cover_img.png'


# Home Page
@login_required(login_url='/loguser/')
def home(request):
    all_post = Post.objects.filter(postshow=True).all()
    all_post = list(all_post)
    random.shuffle(all_post)
    user_profile = Profile.objects.filter(user=request.user).first()
    return render(request, 'home.html', {'profile': user_profile, 'name': request.user, 'all_post': all_post})


'''FROM LINE 36 TO 374 CREDENTIAL RELATED LOGIC '''


# OTP Template For Signup OTP
def Signu_otp(name, email, otp):
    print(email)
    url = "https://control.msg91.com/api/v5/email/send"
    payload = {
        'to': [{'name': name, 'email': email}],
        'from': {'name': 'pritimaya', 'email': 'support@clasoc.com'},
        'variables': {'name': name, 'OTP': otp},
        'domain': 'clasoc.com',
        'template_id': 'template_signup'
    }
    payload = json.dumps(payload)
    headers = {
        "Content-Type": "application/JSON",
        "Accept": "application/json",
        "authkey": "396373AC78f3NtG6492a1a7P1"
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        print("sucess")
        return True
    else:
        print("none")
        return False

# OTP Template For Login OTP
def Login_otp(name, email, otp):
    print(email)
    url = "https://control.msg91.com/api/v5/email/send"
    payload = {
        'to': [{'name': name, 'email': email}],
        'from': {'name': 'pritimaya', 'email': 'support@clasoc.com'},
        'variables': {'name': name, 'OTP': otp},
        'domain': 'clasoc.com',
        'template_id': 'template_login'
    }
    payload = json.dumps(payload)
    headers = {
        "Content-Type": "application/JSON",
        "Accept": "application/json",
        "authkey": "396373AC78f3NtG6492a1a7P1"
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        print("sucess")
        return True
    else:
        print("none")
        return False

# OTP Template For Forgot OTP
def Forgot_otp(name, email, otp):
    print(email)
    url = "https://control.msg91.com/api/v5/email/send"
    payload = {
        'to': [{'name': name, 'email': email}],
        'from': {'name': 'pritimaya', 'email': 'support@clasoc.com'},
        'variables': {'name': name, 'OTP': otp},
        'domain': 'clasoc.com',
        'template_id': 'template_forgot_password'
    }
    payload = json.dumps(payload)
    headers = {
        "Content-Type": "application/JSON",
        "Accept": "application/json",
        "authkey": "396373AC78f3NtG6492a1a7P1"
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        print("sucess")
        return True
    else:
        print("none")
        return False

# Signup A User -->Go To Signup Page
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password_again = request.POST['password-again']
        if not email or not password or not name or not password_again:
            messages.info(request, 'Please Fill All Fields')
            return redirect('/signup/')

        if password != password_again:
            messages.info(request, 'Password Not Matched')
            return redirect('/signup/')

        # Normalize Email
        parsed_email = email_utils.parseaddr(email)[1]
        email = parsed_email.lower()

        otp_object = OTP.objects.filter(email=email).first()
        if otp_object and otp_object.failed_attempts >= 3 and otp_object.locked_until > timezone.now():
            messages.info(request, 'Account Has Been locked For 24 hours')
            return redirect('/signup/')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            messages.info(request, 'THIS USER IS ALREADY EXIST')
            return redirect('/signup/')
        request.session['email'] = email
        request.session['password'] = password
        request.session['name'] = name
        otp = random.randint(100000, 999999)
        # If OTP Not Sent Sucessfully
        if not Signu_otp(name, email, otp):
            messages.info(request, 'Please Give A Valid Email')
            return redirect('/signup/')

        myotp = OTP.objects.filter(email=email).first()
        if myotp:
            myotp.otp = otp
            myotp.save()
        else:
            OTP.objects.create(otp=otp, email=email)
        return redirect('signup_otp')
    return render(request, 'signup.html')

# Login A User -->Go To Login Page
def loguser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if not email or not password:
            messages.info(request, 'Please Fill All Fields')
            return redirect('/loguser/')

        # Normalize Email
        parsed_email = email_utils.parseaddr(email)[1]
        email = parsed_email.lower()
        otp_object = OTP.objects.filter(email=email).first()

        # Check If User Is Blocked For 24 Hours
        if otp_object and otp_object.failed_attempts >= 3 and otp_object.locked_until > timezone.now():
            messages.info(request, 'Account Has Been locked For 24 hours')
            return redirect('/loguser/')

        user = CustomUser.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            request.session['email'] = email
            request.session['password'] = password
            otp = random.randint(100000, 999999)
            otp_object = OTP.objects.filter(email=email).first()
            otp_object.otp = otp
            otp_object.save()
            user_profile = Profile.objects.get(user=user)
            # If OTP Not Sent Sucessfully
            if not Login_otp(user_profile.name, email, otp):
                messages.info(request, 'Please Give A Valid Email')
                return redirect('/loguser/')
            return redirect('login_otp')

        messages.info(request, 'PASSWORD OR EMAIL ID IS WRONG')
        return redirect('loguser')
    return render(request, 'login.html')

# Go To Forgot_Password Page
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST["email"]
        if not email:
            messages.info(request, 'Please Give An Email')
            return redirect('forgot')

        parsed_email = email_utils.parseaddr(email)[1]
        email = parsed_email.lower()
        request.session['email'] = email
        user = CustomUser.objects.filter(email=email).first()
        if user:
            otp = random.randint(100000, 999999)
            otp_object = OTP.objects.filter(email=email).first()
            otp_object.otp = otp
            otp_object.save()
            user_profile = Profile.objects.get(user=user)
            # if OTP Not Sent Sucessfully
            if not Forgot_otp(user_profile.name, email, otp):
                messages.info(request, 'Something Went Wrong')
                return redirect('forgot')

            return redirect('forgot_otp')
        else:
            messages.info(request, 'User Not Exist')
            return redirect('forgot')
    return render(request, 'forgotpassword.html')

# OTP Verification Logic During Signup Time
def Signup_otp_check(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        if not otp:
            messages.info(request, 'Please Give Otp')
            return redirect('otp')
        mail = request.session.get('email')
        password = request.session.get('password')
        name = request.session.get('name')
        if not mail or not password or not name:
            messages.info(request, 'Something Is Missing')
            return redirect('otp')
        otp_object = OTP.objects.filter(email=mail).first()
        user = CustomUser.objects.filter(email=mail).first()
        if otp_object:
            if not user and otp_object.otp == otp:
                my_user = CustomUser.objects.create_user(
                    email=mail, password=password)
                otp_object.user = my_user
                otp_object.failed_attempts = 0
                otp_object.locked_until = None
                otp_object.save()
                Profile.objects.create(user=my_user, id=my_user.id, name=name)
                my_user = auth.authenticate(email=mail, password=password)
                if my_user:
                    auth.login(request, my_user)
                    return render(request, 'owneditprofile.html')

            # If Wrong OTP Given
            elif not user:
                otp_object.failed_attempts += 1
                # If Reach Max Attempt Auto Reset OTP
                if otp_object.failed_attempts >= 3:
                    otp_object.failed_attempts = 0
                    otp_object.otp = random.randint(100000, 999999)
                otp_object.save()
                messages.info(request, 'OTP NOT MATCHED TRY again')
                return redirect('signup_otp')

            # If User Already Exist
            else:
                messages.info(request, 'User Already Exist')
                return redirect('signup_otp')
        else:
            messages.info(request, 'Some Thing Went Wrong')
            return redirect('signup_otp')
    return render(request, 'otp.html')

# OTP Verification Logic During Login Time
def Login_otp_check(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        if not otp:
            messages.info(request, 'Please Give Otp')
            return redirect('login_otp')
        mail = request.session.get('email')
        password = request.session.get('password')
        if not mail or not password:
            messages.info(request, 'Something Is Missing')
            return redirect('login_otp')
        otp_object = OTP.objects.filter(email=mail).first()
        if otp_object:
            if otp_object.failed_attempts >= 3 and otp_object.locked_until > timezone.now():
                messages.info(request, 'Account Has Been locked For 24 hours')
                return redirect('login_otp')
            if otp_object.otp == otp:
                user = CustomUser.objects.filter(email=mail).first()
                # If User Already Exist Then Login User
                if user:
                    my_user = auth.authenticate(email=mail, password=password)
                    auth.login(request, my_user)
                    # Reset OTP Attempts
                    otp_object.failed_attempts = 0
                    otp_object.locked_until = None
                    otp_object.save()
                    return redirect('/')
                else:
                    messages.info(request, 'User Not Exist')
                    return redirect('login_otp')

            # If Wrong OTP Given
            else:
                otp_object.failed_attempts += 1
                # If Reach Max Attempt Lock Account For 24 Hours
                if otp_object.failed_attempts == 3:
                    otp_object.locked_until = timezone.now() + timedelta(hours=24)
                    otp_object.save()
                    messages.info(
                        request, 'Account Has Been locked For 24 hours')
                    return redirect('login_otp')

                # If After Next 24 Hour Again Give Wrong OTP Handle Here
                if otp_object.failed_attempts > 3:
                    # 1 Failed Attempt For This Attempt
                    otp_object.failed_attempts = 1
                    otp_object.locked_until = None
                otp_object.save()

                # Warn User Before Last Attempt
                if otp_object.failed_attempts == 2:
                    messages.info(request, 'Last Attempt')
                    return redirect('login_otp')
                messages.info(request, 'OTP NOT MATCHED TRY again')
                return redirect('login_otp')
        messages.info(request, 'Something Went Wrong')
        return redirect('login_otp')
    return render(request, 'otp.html')

# OTP Verification Logic During Forgot_Password Setup Time
def Forgot_otp_check(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        password = request.POST['password']
        if not otp or not password:
            messages.info(request, 'Please Fill All Fields')
            return redirect('forgot_otp')
        mail = request.session.get('email')
        if not mail:
            messages.info(request, 'Something Is Missing')
            return redirect('otp')
        otp_object = OTP.objects.filter(email=mail).first()
        if otp_object:
            if otp_object.otp == otp:
                user = CustomUser.objects.filter(email=mail).first()
                user.set_password(password)
                user.save()
                otp_object.failed_attempts = 0
                otp_object.otp = random.randint(100000, 999999)
                otp_object.save()
                my_user = auth.authenticate(email=mail, password=password)
                auth.login(request, my_user)
                return redirect('/')
            else:
                otp_object.failed_attempts += 1
                # Auto Reassign New OTP After 3 Failure Attempt
                if otp_object.failed_attempts >= 3:
                    otp_object.failed_attempts = 0
                    otp_object.otp = random.randint(100000, 999999)
                    otp_object.save()
                otp_object.save()
                messages.info(request, 'OTP NOT MATCHED TRY AGAIN')
                return redirect('forgot_otp')
        messages.info(request, 'Something Went Wrong')
        return redirect('forgot_otp')
    return render(request, 'forgototp.html')

# Log_Out Current User
@login_required(login_url='/loguser/')
def logout(request):
    auth.logout(request)
    return redirect('/loguser/')


'''FROM LINE 380 TO 490 USERS PROFILE RELATED LOGIC'''


# Create And Edit Profile
@login_required(login_url='/loguser/')
def create_profile(request):
    if request.method == 'POST':
        myprofile = Profile.objects.filter(user=request.user).first()

        # Get Profile And Cover Pic
        if request.FILES.get('profile_image'):
            profile_image = request.FILES.get('profile_image')
        else:
            profile_image = default_image
        if request.FILES.get('cover_image'):
            cover_image = request.FILES.get('cover_image')
        else:
            cover_image = default_cover_image

        name = request.POST['name']
        about = request.POST['about']
        school = request.POST['school']
        myprofile.profileimage = profile_image
        myprofile.backgroundimage = cover_image
        name = name if name else myprofile.name
        myprofile.name = name
        myprofile.about = about
        myprofile.current_study = school
        myprofile.save()
        return JsonResponse({"message": "Success done"})

    # Goto Edit_Profile Page
    else:
        myprofile = Profile.objects.filter(user=request.user).first()
        name = myprofile.name
        about = myprofile.about
        school = myprofile.current_study
        context = {
            'name': name,
            'about': about,
            'school': school
        }
        return render(request, 'owneditprofile.html', context)
    
# Visit Current User Profile
@login_required(login_url='/loguser')
def Own_profile(request):
    uy = request.user
    user_profile = Profile.objects.filter(user=uy).first()
    allfollow = Followerscount.objects.filter(user=uy)
    allfollow = len(allfollow)
    posts = Post.objects.filter(Q(post_by=uy) & Q(postshow=True))
    context = {
        'posts': posts,
        'number': allfollow,
        'profile': user_profile,
    }
    return render(request, 'ownprofile.html', context)

# Visit Other Users Profile
@login_required(login_url='/loguser')
def Other_profile(request):
    user_id = request.GET.get('myuser')
    user_profile = Profile.objects.filter(id=user_id).first()
    my_user = request.user
    person_obj = user_profile.user
    person_id = person_obj.id
    follower_exist = Followerscount.objects.filter(
        follower=my_user, user=person_obj).first()
    allfollow = Followerscount.objects.filter(user=person_obj).all()
    allfollow = len(allfollow)

    # Set Up Button For Show In Profile
    if person_obj == my_user:
        button = 'EDIT PROFILE'
    else:
        button = 'UNFOLLOW' if follower_exist else 'FOLLOW'

    context = {
        'person_id': person_id,
        'myuser': my_user,
        'button': button,
        'number': allfollow,
        'profile': user_profile,
        'user': person_obj
    }
    return render(request, 'other_profile.html', context)

# Search A User Profile
@login_required(login_url='/loguser')
def Search(request):
    if request.method == 'POST':
        name = request.POST['searchname']
        users = Profile.objects.filter(name__icontains=name).all()
        return render(request, 'search.html', {'profiles': users})
    else:
        return redirect('/')

# Follow A User Profile
@login_required(login_url='/loguser')
def Follow(request):
    current_user = request.user
    user_id = request.GET.get('myuser')
    user = CustomUser.objects.filter(id=user_id).first()
    user_profile = Profile.objects.filter(user=user).first()
    profile_id = user_profile.id
    follower_exist = Followerscount.objects.filter(
        follower=current_user, user=user).first()
    if follower_exist:
        follower_exist.delete()
        return redirect(f'/prof/?myuser={profile_id}')
    else:
        Followerscount.objects.create(follower=current_user, user=user)
        return redirect(f'/prof/?myuser={profile_id}')


'''FROM LINE 453 TO 479 POST IMAGE RELATED LOGIC'''


# Go To Image Post Page
@login_required(login_url='/loguser/')
def my_post(request):
    return render(request, 'post.html')


# Save Compressed Post Image
@login_required(login_url='/loguser')
def handle_compressed_image(request):
    if request.method == "POST":
        current_profile = Profile.objects.filter(user=request.user).first()
        text_data = request.POST.get("text_data")
        image_data = request.FILES.get("image_data")
        Post.objects.create(my_post=image_data, post_by=request.user,
                            poster_profile=current_profile, about=text_data)
        return JsonResponse({"message": "Success done"})


# Delete A Image By User
@login_required(login_url='/loguser')
def Deletepic(request):
    if request.GET.get('value'):
        ownuser = request.user
        value = request.GET.get('value')
        deletephoto = Post.objects.filter(
            Q(id=value) & Q(post_by=ownuser)).first()
        deletephoto.postshow = False
        deletephoto.save()
        return redirect('/')


'''FROM LINE 530 TO 580 IMAGE LIKE AND COMMENT RELATED LOGIC'''


# Like A Image
@login_required(login_url='/loguser')
def like_check(request):
    user = request.user
    like_id = request.GET.get('like_id')
    current_post = Post.objects.filter(id=like_id).first()
    like = Like_post.objects.filter(post_id=like_id, like_user=user).first()
    if like:
        like.delete()
        current_post.no_of_like -= 1
        current_post.save()
    else:
        new_like = Like_post.objects.create(post_id=like_id, like_user=user)
        current_post.no_of_like += 1
        current_post.save()
    data = {
        'likes': current_post.no_of_like
    }
    return JsonResponse(data)

# Go To Comment Page Of A Image
@login_required(login_url='/loguser')
def Showcomment(request, post_id):
    user = request.user
    current_post = Post.objects.filter(id=post_id).first()
    allcomments = Comment.objects.filter(comment_post=current_post)
    recent_user = Profile.objects.filter(user=user).first()
    context = {
        'user': user,
        'allcomments': allcomments,
        'post_id': post_id,
        'recent_user': recent_user
    }
    return render(request, 'comment.html', context)

# Save A New Comment In Database
@login_required(login_url='/loguser')
def Createcomment(request):
    if request.method == "POST":
        comment = request.POST['comment']
        post_id = request.POST['id']
        user = request.user
        user_profile = Profile.objects.filter(user=user).first()
        current_post = Post.objects.filter(id=post_id).first()
        Comment.objects.create(
            text=comment, comment_by=user_profile, comment_post=current_post)
        current_post.no_of_coment += 1
        user_profile.comment_by_user += 1
        current_post.save()
        user_profile.save()
        return JsonResponse({'success': True})

# Custom Error Page
def page_not_found(request, exception):
    return render(request, '404.html')
