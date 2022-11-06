from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.core.exceptions import ValidationError


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=50, label='Почта',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')


class QuantityOfProduct(forms.Form):
    quantity = forms.IntegerField(label='Количество', min_value=1)

    def check_quantity_value(self, fur_on_storage):
        quantity = self.data["quantity"]
        if int(quantity) > fur_on_storage:
            return "None"
        return quantity


class AddressOfOrder(forms.Form):
    address = forms.CharField(label='Адрес доставки')
