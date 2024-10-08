from django.contrib.auth import forms

from django.contrib import admin

from accounts.models import CustomUser


admin.site.register(CustomUser)



from django.contrib.auth import forms

# Register your models here.
class CustomUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = CustomUser
        fields = forms.UserCreationForm.Meta.fields + ('email','first_name','last_name','cpf',)
        
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
            field.widget.attrs['class'] = 'form-control'