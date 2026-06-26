from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Producto


class RegistroForm(UserCreationForm):
    username = forms.CharField(
        label='Usuario',
        max_length=30,
        min_length=3,
        strip=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        error_messages={
            'required': 'El nombre de usuario es obligatorio.',
            'min_length': 'El nombre de usuario debe tener al menos 3 caracteres.',
            'max_length': 'El nombre de usuario no puede exceder 30 caracteres.',
        },
    )
    password1 = forms.CharField(
        label='Contraseña',
        min_length=8,
        max_length=128,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        error_messages={
            'required': 'La contraseña es obligatoria.',
            'min_length': 'La contraseña debe tener al menos 8 caracteres.',
        },
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        min_length=8,
        max_length=128,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite la contraseña'}),
        error_messages={
            'required': 'Debes confirmar la contraseña.',
        },
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


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
        fields = ['nombre', 'talla', 'color', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'talla': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del producto', 'rows': 3}),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'talla': 'Talla',
            'color': 'Color',
            'descripcion': 'Descripción',
        }
