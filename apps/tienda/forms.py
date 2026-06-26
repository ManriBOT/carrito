import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Producto


USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_]{3,30}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_REGEX = re.compile(r'^\+?[1-9]\d{1,14}$')
NAME_REGEX = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,50}$')


def validar_username(value):
    if not USERNAME_REGEX.match(value):
        raise ValidationError('El usuario solo puede contener letras, números y guión bajo (3-30 caracteres).')


def validar_password(value):
    if not PASSWORD_REGEX.match(value):
        raise ValidationError('La contraseña debe tener: 8+ caracteres, mayúscula, minúscula, número y símbolo (@$!%*?&).')


def validar_email(value):
    if not EMAIL_REGEX.match(value):
        raise ValidationError('Ingrese un email válido.')


def validar_nombre(value):
    if not NAME_REGEX.match(value):
        raise ValidationError('Solo letras y espacios (2-50 caracteres).')


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        validators=[validar_email],
        error_messages={
            'required': 'El email es obligatorio.',
            'invalid': 'Ingrese un email válido.',
        }
    )
    first_name = forms.CharField(
        label='Nombre',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
        validators=[validar_nombre],
        error_messages={'required': 'El nombre es obligatorio.'}
    )
    last_name = forms.CharField(
        label='Apellidos',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tus apellidos'}),
        validators=[validar_nombre],
        error_messages={'required': 'Los apellidos son obligatorios.'}
    )
    username = forms.CharField(
        label='Usuario',
        max_length=30,
        min_length=3,
        strip=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario123'}),
        validators=[validar_username],
        error_messages={
            'required': 'El nombre de usuario es obligatorio.',
            'min_length': 'Mínimo 3 caracteres.',
            'max_length': 'Máximo 30 caracteres.',
        },
    )
    password1 = forms.CharField(
        label='Contraseña',
        min_length=8,
        max_length=128,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mín. 8 chars, mayús, minús, num, símbolo'}),
        validators=[validar_password],
        error_messages={
            'required': 'La contraseña es obligatoria.',
            'min_length': 'Mínimo 8 caracteres.',
        },
        help_text='Debe contener: mayúscula, minúscula, número y símbolo (@$!%*?&)'
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        min_length=8,
        max_length=128,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite la contraseña'}),
        error_messages={'required': 'Debes confirmar la contraseña.'},
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Este email ya está registrado.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Este nombre de usuario ya existe.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        max_length=30,
        strip=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        error_messages={'required': 'El nombre de usuario es obligatorio.'},
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        error_messages={'required': 'La contraseña es obligatoria.'},
    )


class AgregarCarritoForm(forms.Form):
    producto_id = forms.IntegerField(min_value=1, widget=forms.HiddenInput())
    cantidad = forms.IntegerField(
        min_value=1,
        max_value=99,
        initial=1,
        widget=forms.HiddenInput(),
    )

    def clean_producto_id(self):
        producto_id = self.cleaned_data['producto_id']
        if not Producto.objects.filter(id=producto_id, activo=True).exists():
            raise forms.ValidationError('El producto no existe o no está disponible.')
        return producto_id


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'talla', 'color', 'descripcion', 'precio', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'talla': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del producto', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01', 'min': '0'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'talla': 'Talla',
            'color': 'Color',
            'descripcion': 'Descripción',
            'precio': 'Precio (€)',
            'activo': 'Activo',
        }


class ProductoFormEditar(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'talla', 'color', 'descripcion', 'precio', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'talla': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del producto', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01', 'min': '0'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'talla': 'Talla',
            'color': 'Color',
            'descripcion': 'Descripción',
            'precio': 'Precio (€)',
            'activo': 'Activo',
        }
