from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.db.models import F
from django.utils.safestring import mark_safe
class UserRatingInline(admin.StackedInline):
    model = UserRating
    extra = 2

class UsersInline(admin.TabularInline):
    model = Hobbies.user.through

class HobbiesInline(admin.TabularInline):
    model = Hobbies.user.through
    extra = 0

@admin.action(description="Change city")
def change_city(modeladmin, request, queryset):
    queryset.update(city="Baranovichi")

@admin.action(description="year later")
def year_later(modeladmin, request, queryset):
    queryset.update(age=F("age")+1)

# @admin.display
# def choices_sex(obj):
#     return obj.get_sex_display()
color_code = 'ffd700'
# @admin.display(description="ФИО")
# def upper_case_name(obj):
#     return f"{obj.name} {obj.surname}".upper()


@admin.display(description='is capital')
def check_capital(object):
    return mark_safe(f"<p style='color:#{color_code};'>capital</p>") if object.city in ['Minsk',"Moscow"] else "simple city"


@admin.display(description='change_status')
def change_status(modeladmin, request, queryset):
    queryset.update(status='b')


class HostAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'max_spend_value', 'status', change_status]
    list_editable = ['status']


@admin.register(Hobbies)
class HobbiesAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name', 'category']
    inlines = [
        UsersInline,
    ]


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    @admin.display
    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{} {}</span>',
            color_code,
            self.name,
            self.surname,
        )

    fields = [("name", 'surname'), 'age', 'email', 'sex','city']
    list_display = [colored_name,"surname","name", 'age', 'sex', 'city',check_capital, ]
    list_display_links = [colored_name,'name','surname']
    list_editable = ["age",'city']
    list_filter = (
        ('city'),
        ('sex'),
        ('surname')
    )
    ordering = ['-name','-age']
    search_fields = ['city','age','sex', 'surname']
    list_per_page = 5
    # list_filter = ['age','sex','city']
    save_on_top = True
    inlines = [
        UserRatingInline,
        HobbiesInline,
    ]
    actions = [change_city,year_later]


@admin.display(description='фото')
def get_html_photo(objects):
    if objects.photo:
        return mark_safe(f'<img src={objects.photo.url} width=50>')


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):


    # get_html_photo.short_descriptions = 'фото'

    list_display = ["rating", "user", get_html_photo]
    list_display_links = ['rating', 'user']



# admin.site.register(Users,UsersAdmin)
# admin.site.register(UserRating)
# admin.site.register(Hobbies)
admin.site.register(Establishments)
admin.site.register(EstablishmentsRating)
admin.site.register(Passport)
admin.site.register(Arrangements)
admin.site.register(Host)
admin.site.register(Guest)
# Register your models here.