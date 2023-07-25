from django.shortcuts import render, redirect
from webswap.models import CollectionRanking, UserProfile, WalletsInfo, UserCollectionsList
from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.http import JsonResponse
import time
import calendar


class HomeView(TemplateView):
    template_name = "index.html"

def landing(request):
    return render(request, 'webswap/index.html')

def page_404(request):
    return render(request, 'webswap/404.html')

def about(request):
    return render(request, 'webswap/about.html')

def base(request):
    return render(request, 'webswap/base.html')

def contacts(request):
    return render(request, 'webswap/contacts.html')

def faq(request):
    return render(request, 'webswap/faq.html')

def forgot(request):
    return render(request, 'webswap/forgot.html')

def privacy(request):
    return render(request, 'webswap/privacy.html')

def modal_login(request):
    return render(request, 'modal_login.html')

def ranking (request):
    p = Paginator(CollectionRanking.objects.all(), 20)
    page = request.GET.get('page')
    collect_lists = p.get_page(page)
    return render(request, 'webswap/ranking.html', {"collect": collect_lists})

def swap(request):
    is_authenticated = request.user.is_authenticated
    if not is_authenticated:
        return render(request, 'webswap/swap.html')
    else:
        username = request.user.username
        user_profile= UserProfile.objects.get(wallet_address=username)
        user_collection = UserCollectionsList.objects.filter(token_owner_id=user_profile.id)
        p = Paginator(UserCollectionsList.objects.filter(token_owner_id=user_profile.id), 10)
        page = request.GET.get('page')
        collect_lists = p.get_page(page)
        pages = range(1, (len(user_collection) // 10 + 2))
        collection_num = range(1, len(user_collection))
        user_profile_info = {
            'wallet_balance':user_profile.wallet_balance_eth,
            'token_balance':len(user_collection),
            'token_usd_value':round(float(user_profile.usd_value), 2),
            'wallet_usd_value': (round(float(user_profile.usd_value), 2) + float(user_profile.wallet_balance_eth)),
            'collection_num':collection_num,
        }
        return render(request, 'webswap/swap.html', {"collection":collect_lists, "user_profile_info":user_profile_info, "pages":pages})
        
    

def request_update_collection(request):
    try:
        WalletsInfo.update_collections()
        print('Finished')
    except:
        pass
    finally:
        return redirect(landing)


class AddressVerify(View):
    def user_auth(request):
        if request.method == 'POST':
            now_address = request.POST.get('wallet_address')
            short_address = request.POST.get('public_address')
            current_user_logged = request.POST.get('current_user')
            if len(now_address) == 42:
                user_profile = UserProfile.objects.filter(wallet_address=now_address).exists()
                if user_profile == True:
                    AddressVerify.user_login(request, now_address, short_address, current_user_logged)
                elif user_profile != True:
                    AddressVerify.user_register(request, now_address, short_address)
            else:
                pass
        return HttpResponse(now_address)
    

    def update_user_collections(address):
        try:
            AddressVerify.delete_user_collection_list(address)
        except:
            pass
        WalletsInfo.get_token_list(address)


    def ajax_load_tokens(request):
        if request.method == 'POST':
            address = request.POST.get('address')
            user_profile = UserProfile.objects.get(wallet_address=address)
            now = time.gmtime()
            if user_profile.last_collection_update and \
            (calendar.timegm(now) - user_profile.last_collection_update) < 600:
                return JsonResponse({"message": "Too many requests"})
            else:
                AddressVerify.delete_user_collection_list(address)
                WalletsInfo.get_token_list(address)
                return JsonResponse(({"message": "success"}))

        

    def user_login(request, now_address, short_address, current_user_logged):
        #verify connected wallet and logged in user
        verify_logged_user = AddressVerify.logged_user_address(request, now_address, current_user_logged)
        #if user wallet and 
        if verify_logged_user != 1 :
            user = authenticate(username=now_address, password = short_address)
            if user is not None:
                login(request, user)
                AddressVerify.update_user_collections(address=now_address)
                #user successfully logged in
            else:
                AddressVerify.user_register(request, now_address, short_address)
        else:
            print('User successfully logged in')



    def user_register(request, now_address, short_address):
        #register user_profile:
        try:
            user=UserProfile.objects.create_user(wallet_address=now_address, public_address=short_address)
            user.save()
        except:
            pass
        #register User model
        try:
            new_user = User.objects.create_user(username=now_address, password=short_address)
            new_user.set_password(raw_password=short_address)
            new_user.save()
            AddressVerify.user_login(request, now_address, short_address)
            user = authenticate(username=now_address, password = short_address)
            if user is not None:
                login(request, user)
        except:
            pass
        AddressVerify.update_user_collections(address=now_address)


    def logged_user_address(request, now_address, current_user_logged):
        if now_address == current_user_logged:
            return 1
        elif now_address != current_user_logged:
            logout(request)
            return 0

    def delete_user_collection_list(address):
        user = UserProfile.objects.get(wallet_address=address)
        user_id = user.id
        try:
            UserCollectionsList.objects.filter(token_owner_id=user_id).delete()
        except:
            pass
        return redirect(swap)