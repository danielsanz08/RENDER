from django import forms
from .models import Transaccion, Insumo,CustomUser,Backup,
from django.contrib.auth import authenticate
from django.core.mail import BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['tipo', 'monto', 'descripcion', 'fecha']
        
class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'descripcion', 'cantidad']
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'name', 'email', 'role', 'phone']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        name = cleaned_data.get('name')

        # Validate passwords
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Las contraseñas no coinciden.')

        # Check if email, phone, or name already exists
        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', 'Ya existe un usuario con este email.')

        if CustomUser.objects.filter(phone=phone).exists():
            self.add_error('phone', 'Ya existe un usuario con este teléfono.')

        if CustomUser.objects.filter(name=name).exists():
            self.add_error('name', 'Ya existe un usuario con este nombre.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        password = cleaned_data.get("password")

        if not name or not password:
            raise forms.ValidationError("Nombre y contraseña son requeridos.")
        
        return cleaned_data
    
class BackupForm(forms.ModelForm):
    class Meta:
        model = Backup
        fields = ['file_name', 'file_path']
        widgets = {
            'file_name': forms.TextInput(attrs={'placeholder': 'Nombre del archivo'}),
            'file_path': forms.TextInput(attrs={'placeholder': 'Ruta del archivo'}),
        }
        
User = get_user_model()


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Contraseña actual')
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='Nueva contraseña')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar nueva contraseña')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("La contraseña actual es incorrecta.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Las nuevas contraseñas no coinciden.")
        return cleaned_data

    def save(self):
        new_password = self.cleaned_data.get('new_password1')
        if new_password:
            self.user.set_password(new_password)
            self.user.save()

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone', 'profile_picture', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        
class CustomPasswordResetForm(PasswordResetForm):
    identifier = forms.CharField(
        label="Correo Electrónico o Teléfono",
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Introduce tu correo electrónico o número de teléfono'})
    )

    def clean_identifier(self):
        identifier = self.cleaned_data.get('identifier')
        if not identifier:
            raise ValidationError("Por favor, ingresa tu correo electrónico o número de teléfono.")
        
        if '@' in identifier:
            if not User.objects.filter(email=identifier).exists():
                raise ValidationError("No hay ningún usuario con ese correo electrónico.")
        else:
            if not User.objects.filter(phone=identifier).exists():
                raise ValidationError("No hay ningún usuario con ese número de teléfono.")
        
        return identifier

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=None,
             from_email=None, request=None,
             html_email_template_name=None,
             extra_email_context=None):
        try:
            super().save(
                domain_override=domain_override,
                subject_template_name=subject_template_name,
                email_template_name=email_template_name,
                use_https=use_https,
                token_generator=token_generator,
                from_email=from_email,
                request=request,
                html_email_template_name=html_email_template_name,
                extra_email_context=extra_email_context,
            )
        except BadHeaderError:
            raise ValidationError("El encabezado del correo electrónico no es válido.")
        except Exception as e:
            # Aquí puedes registrar el error o manejarlo de acuerdo a tus necesidades
            print(f'Error al enviar el correo: {str(e)}')
            raise ValidationError(f"Hubo un problema al enviar el correo electrónico: {str(e)}")
        
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }