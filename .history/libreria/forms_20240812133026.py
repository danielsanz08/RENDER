from django import forms
from .models import Transaccion

class TramsaccionForm(forms.ModelForm):
    class Meta:
        model: Transaccion
        fields: '__all__'
        


class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'descripcion', 'cantidad']
        
        