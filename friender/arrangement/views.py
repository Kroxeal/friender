from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import datetime
from .models import Users
#
# friends = {
#     "Max": [34, "max@mail.ru"],
#     "Grigory": [32, "grigory@mail.ru"],
#     "Anna": [29, "anna@mail.ru"],
#     'Pedro': [21, "pedro@mail.ru"],
#     'Kate': [32, "kate@mail.ru"]
# }
establishments = ['Butter bro', 'Terra', 'Golden Cafe', 'Pancakes', 'Depo']


# функция представления (вьюшка)


def main_page(request):
    return render(request, 'main.html')


def place_arrangments(request):
    context = {
        "establishments": establishments,
    }
    return render(request, 'establishments.html', context=context)


def all_friends(request):
    context = {
        "friends": Users.objects.all(),
    }
    return render(request, "friends.html", context=context)