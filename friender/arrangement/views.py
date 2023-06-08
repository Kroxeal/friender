from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View
from .models import *
from .forms import *
from django.db import transaction
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin




import datetime


# friends = {
#     "Max": [34, "max@mail.ru"],
#     "Grigory": [32, "grigory@mail.ru"],
#     "Anna": [29, "anna@mail.ru"],
#     'Pedro': [21, "pedro@mail.ru"],
#     'Kate': [32, "kate@mail.ru"]
# }
# establishments = ['Butter bro', 'Terra', 'Golden Cafe', 'Pancakes', 'Depo']


# функция представления (вьюшка)
#
@login_required(login_url="/admin/login/")
def main_page(request):
    return render(request, 'main.html')

@permission_required('arrangement.view_users',login_url="/arrangement/main")
def all_friends(request):
    users = Users.objects.all().prefetch_related("hobbies_set", "userrating_set")
    paginator = Paginator(users, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        "friends": users,
        "page_obj": page_obj
        # "friends": Users.objects.filter(age__gte=28).order_by('name')[:100],
        # "friends": Users.objects.filter(name = 'Suzan')[:100],
        # "friends": Users.objects.filter(sex='f').order_by('-age')[:100],
        # "friends": Users.objects.filter(age__gte=28).order_by('-sex')[:100],
    }
    return render(request, "friends.html", context=context)


def static_url(request):
    return render(request, "static_example.html")


def user_rating(request):
    context = {
        "ratings": UserRating.objects.all().select_related('user')
    }
    return render(request, "userrating.html", context=context)


def establishments_rating_form(request, **kwargs):
    establishment_id = int(kwargs['id'])
    print(establishment_id)
    context = {}
    if request.method == 'POST':
        form = EstablishmentsRatingForm(request.POST, request.FILES)
        context['form'] = form
        if form.is_valid():
            EstablishmentsRating.objects.create(
                establishment_id=establishment_id,
                rating=request.POST['rating'],
                description=request.POST['description']
            )
            return redirect('establishments')
    else:
        form = EstablishmentsRatingForm
        context['form'] = form

    return render(request, "establishments_rating_form.html", context=context)


def user_form_rating(request, **kwargs):
    user_id = int(kwargs['id'])
    context = {}
    if request.method == "POST":
        form = RatingUserForm(request.POST, request.FILES)
        context["form"] = form
        if form.is_valid():
            UserRating.objects.create(
                user_id=user_id,
                rating=request.POST['rating'],
                description=request.POST['description'],
                photo=request.FILES["photo"]
            )
            return redirect("friends")
    else:
        form = RatingUserForm()
        context["form"] = form
    # context = {
    #     # "user": Users.objects.get(id=user_id)
    #     "form" : form
    # }
    return render(request, "user_form_rating.html", context=context)


def create_user(request):
    context = {}
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        context["form"] = form
        if form.is_valid():
            form.save()
            return redirect("friends")
    else:
        form = CreateUserForm()
        context["form"] = form
    return render(request, "create_user_form.html", context=context)






@transaction.atomic
def create_arrangement(request):
    context = {}
    if request.method == "POST":
        form = ArrangementForm(request.POST)
        context["form"] = form
        guest = Guest.objects.all().order_by('?')[0]
        if form.is_valid():

            host_id = int(request.POST['host'])
            place_id = int(request.POST['place'])
            print(host_id, place_id)

            host = Host.objects.get(users_ptr_id=host_id)
            establishments = Establishments.objects.get(id=place_id)

            if host.status == 'a':
                host.status = 'b'
                host.save()
                Arrangements.objects.create(
                    host=host,
                    guest=Guest.objects.get(users_ptr_id=guest.id),
                    establishments=establishments
                )
            else:
                return HttpResponse("Пользователь уже занят")

            return redirect("friends")
    else:
        form = ArrangementForm()
        context["form"] = form
    return render(request, "create_arrangement.html", context=context)



class PlaceListView(ListView):
    template_name = 'establishments.html'
    paginate_by = 5
    model = Establishments
    context_object_name = "establishments"
    queryset = Establishments.objects.all()


class EstablishmentsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'createplace.html'
    login_url = "/admin/login/"
    model = Establishments
    fields = ["name", "category", "address", "phone"]
    success_url = reverse_lazy("establishments")
# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context["establishments"] = Establishments.objects.all()
#     return context

# def place_arrangments(request):
#     context = {
#         "establishments": Establishments.objects.all(),
#     }
#     return render(request, 'establishments.html', context=context)