from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/users/login/")
def index(request):
    # Get the logged-in user
    user = request.user

    # Filter goods by the logged-in user that are not in any collection
    stationery_item_queryset = Stationery_item.objects.filter(user=user)

    stationery_item_count = Stationery_item.objects.filter(user=user).count()
    column_stationery_items = stationery_item_count/2

    # Search functionality for goods
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        stationery_item_queryset = stationery_item_queryset.filter(name__icontains=search_query)

    # Paginate goods
    paginator = Paginator(stationery_item_queryset, 25)  # Show 25 goods per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'stationery_items': page_obj,
        'stationery_item_count': stationery_item_count,
        'column_stationery_items': column_stationery_items
    }
    return render(request, 'stationery_items/index.html', context)

@login_required(login_url='/users/login/')
def add_item(request):

    if request.method == "POST":
        data = request.POST
        stationery_item_name = data.get('stationery_item_name')
        stationery_item_description = data.get('stationery_item_description')
        stationery_item_image = request.FILES.get('stationery_item_image')
        stationery_item_quantity = data.get('stationery_item_quantity')
        creator = request.user
        

        Stationery_item.objects.create(user = creator, name = stationery_item_name, description = stationery_item_description, quantity = stationery_item_quantity, image = stationery_item_image)

        messages.info(request, "Stationery Item added successfully")
        return redirect('/stationery_items/')
    
    return render(request, 'stationery_items/add_stationery_item.html')

@login_required(login_url='/users/login/')
def update_item(request ,id):
    queryset = Stationery_item.objects.get(id = id)
    old_queryset = Stationery_item.objects.get(id = id)

    if queryset.user == request.user:
        stationery_item_original_name = queryset.name
        context = {'stationery_item' : queryset}

        if request.method == "POST":
            data = request.POST
            name = data.get('stationery_item_name')
            description = data.get('stationery_item_description')
            image = request.FILES.get('stationery_item_image')
            quantity = data.get('stationery_item_quantity')
            creator = request.user


            queryset.name = name
            queryset.description = description
            queryset.quantity = quantity

            if image:
                queryset.image = image
                old_queryset.delete()
            queryset.save()

            messages.info(request, f"{stationery_item_original_name} has been updated successfully")
            return redirect('/stationery_items/')
    else:
        messages.info(request, f"This stationery item was created by {queryset.user}. So, you can't update this stationery item because you are not the creator of this stationery item.")
        
        return redirect('/stationery_items/')

    return render(request, 'stationery_items/update_stationery_item.html', context)

@login_required(login_url='/users/login/')
def delete_item(request, id):
        queryset = Stationery_item.objects.get(id=id)
        
        if queryset.user == request.user:
            deleted_stationery_item_name = queryset.name
            queryset.delete()
            messages.info(request, f"{deleted_stationery_item_name} deleted successfully")
        else:
            messages.info(request, f"This stationery item was created by {queryset.user}. So, you can't update this stationery item because you are not the creator of this stationery item.")
        return redirect('/stationery_items/')