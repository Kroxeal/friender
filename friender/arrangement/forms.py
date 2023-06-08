from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from .models import *


def validate_length_description(value):
    if len(value.split()) < 3:
        raise ValidationError(
            "need more than 2 words"
        )


def validate_max_length_description_establishments(value):
    if len(value) > 100:
        raise ValidationError(
            'input description before 100 symbol',
        )


class RatingUserForm(forms.ModelForm):

    class Meta:
        model = UserRating
        exclude = ("user",)


class EstablishmentsRatingForm(forms.ModelForm):

    description = forms.CharField(validators=[
            validate_max_length_description_establishments,
        ])
    rating = forms.IntegerField(validators=[
        MaxValueValidator(5, message='input rating between 1 and 5'),
        MinValueValidator(1, message='input rating between 1 and 5')
    ])

    class Meta:
        model = EstablishmentsRating
        exclude = ('establishment',)


class EstablishmentCreateForm(forms.ModelForm):
    class Meta:
        model = Establishments
        fields = ("name","category","address","phone")
# class RatingUserForm(forms.Form):
#     rating = forms.IntegerField(validators=[
#         MaxValueValidator(5, message='input rating between 1 and 5'),
#         MinValueValidator(1, message='input rating between 1 and 5')
#     ])
#     description = forms.CharField(
#         validators=[
#             MinLengthValidator(3, message='input more than 3 symbols'),
#             validate_length_description
#         ],
#         widget=forms.Textarea(
#             attrs={
#                 'cols':30,
#                 'rows':3,
#                 'placeholder':'your opinion about arrangement',
#                 "class": "special"
#             }
#         )
#     )


class ArrangementForm(forms.Form):
    host = forms.ChoiceField(choices=Host.objects.values_list('id','name'))
    place = forms.ChoiceField(choices=Establishments.objects.values_list('id','name'))


class CreateUserForm(forms.ModelForm):
    age = forms.IntegerField(validators=[
        MaxValueValidator(90, message='input age between 18 and 90'),
        MinValueValidator(18, message='input age between 18 and 90')
    ])

    class Meta:
        model = Users
        exclude = ('email',)
        # fields = "__all__"
