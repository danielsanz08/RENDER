from django import forms
from .models import Transaccion, Insumo,CustomUser,Backup
from django.contrib.auth import authenticate
class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['tipo', 'monto', 'descripcion', 'fecha']
        
class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'descripcion', 'cantidad']
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'name', 'email', 'role', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')

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