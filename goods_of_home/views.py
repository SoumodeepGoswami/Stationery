from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import *
from django.core.paginator import Paginator

# Create your views here.

device = ''

def my_view(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if 'Mobile' in user_agent:
        device = 'mobile'
    else:
        device = 'desktop'

@login_required(login_url='/users/login')
def index(request):
    # Get the logged-in user
    user = request.user

    # Filter goods by the logged-in user that are not in any collection
    goods_queryset = Good.objects.filter(user=user)

    goods_count = Good.objects.filter(user=user).count()
    column_goods = goods_count/2

    # Search functionality for goods
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        goods_queryset = goods_queryset.filter(good_name__icontains=search_query)

    # Paginate goods
    paginator = Paginator(goods_queryset, 25)  # Show 25 goods per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'Goods': page_obj,
        'goods_count': goods_count,
        'column_goods': column_goods
    }

    if device == 'mobile':
        return render(request, 'good_of_home/index_mobile.html', context)
    else:
        return render(request, 'goods_of_home/index.html', context)


def add_good(request):

    if request.method == "POST":
        data = request.POST
        good_name = data.get('good_name')
        good_description = data.get('good_description')
        good_image = request.FILES.get('good_image')
        good_location = data.get('good_location')
        good_collection = data.get('good_collection')
        creator = request.user
        

        Good.objects.create(user = creator, good_name = good_name, good_description = good_description, good_location = good_location, good_image = good_image, good_collection = good_collection)

        messages.info(request, "Good added successfully")
        return redirect('/goods/')
    return render(request, 'goods_of_home/add_good.html')

@login_required(login_url='/users/login')
def update_good(request ,id):
    queryset = Good.objects.get(id = id)
    old_queryset = Good.objects.get(id = id)

    if queryset.user == request.user:
        good_original_name = queryset.good_name
        context = {'good' : queryset}

        if request.method == "POST":
            good_name = request.POST.get('good_name')
            good_description = request.POST.get('good_description')
            good_image = request.FILES.get('good_image')
            good_location = request.POST.get('good_location')
            good_collection = request.POST.get('good_collection')


            queryset.good_name = good_name
            queryset.good_description = good_description
            queryset.good_location = good_location
            queryset.good_collection = good_collection

            if good_image:
                queryset.good_image = good_image
                old_queryset.delete()
            queryset.save()

            messages.info(request, f"{good_original_name} has been updated successfully")
            return redirect('/goods/')
    else:
        messages.info(request, f"This good was created by {queryset.user}. So, you can't update this good because you are not the creator of this good.")
        
        return redirect('/goods/')

    return render(request, 'goods_of_home/update_good.html', context)


@login_required(login_url='/users/login')
def delete_good(request, id):
    queryset = Good.objects.get(id = id)

    if queryset.user == request.user:
        good_name = queryset.good_name
        queryset.delete()
        messages.info(request, f"{good_name} has been deleted successfully")
        return redirect('/goods/')