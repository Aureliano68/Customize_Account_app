from django import forms
from .models import CustomerUser
from django.core .exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# --------------------------------------------------------------------------------------------------------------------------------------
class UsercreateForm(forms.ModelForm):
    password1=forms.CharField(label='password1',widget=forms.PasswordInput)
    password2=forms.CharField(label='password2',widget=forms.PasswordInput)

    class Meta:
        model=CustomerUser
        fields=['mobile_number','email','name','family','gender']
        
    def clean_password2(self):
        pass1=self.cleaned_data['password1']
        pass2=self.cleaned_data['password2']
        if pass1 and pass2 and pass1!=pass2:
            raise ValidationError('پسورد اول و دوم مطابقت ندارد')
        return pass2
    def save(self,commit=True):
       user= super().save(commit=False)
       user.set_password(self.cleaned_data['password1'])
       if commit:
           user.save_m2m()
       return user
        
# --------------------------------------------------------------------------------------------------------------------------------------       
class UserchangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text="برای تغییر رمز خود روی این  <a href='../password' > لینک</a> کلیک کنید")
    class Meta:
        model=CustomerUser
        fields=['mobile_number','password','email','name','family','gender','is_active','is_admin']
        
# --------------------------------------------------------------------------------------------------------------------------------------       
class UserRegisterForm(forms.ModelForm):
    password1=forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'},))
    password2=forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز عبور را وارد کنید'},))

    class Meta:
        model=CustomerUser
        fields=['mobile_number',]
        widgets={
            'mobile_number':forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل را وارد کنید'},)
        }
        
    def clean_pass2(self):
        pass1=self.cleaned_data['password1']
        pass2=self.cleaned_data['password2']
        if pass1 and pass2 and pass1!=pass2:
            raise ValidationError('رمز و تکرار رمز عبور مغایرت دارند')
        return pass1

# --------------------------------------------------------------------------------------------------------------------------------------       
class verifyUserForm(forms.Form):
    active_code=forms.CharField(label=" کد فعال سازی",error_messages={'required':'این فیلد نمیتواند خالی باشد'},widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد دریافتی را وارد کنید'},))

# --------------------------------------------------------------------------------------------------------------------------------------       
class LoginUserForm(forms.Form):
    mobile_number=forms.CharField(label="شماره موبایل",
                                  error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید'},))
    password=forms.CharField(label="رمز عبور",
                                  error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':' رمز عبور را وارد کنید'},))

# --------------------------------------------------------------------------------------------------------------------------------------       
class changeUserForm(forms.Form):
    password1=forms.CharField(label="رمز عبور",
                                  error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':' رمز عبور را وارد کنید'},))
    password2=forms.CharField(label="رمز عبور",
                                  error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':' تکرار رمز عبور را وارد کنید'},))
    
    def clean_pass2(self):
        pass1=self.cleaned_data['password1']
        pass2=self.cleaned_data['password2']
        if pass1 and pass2 and pass1!=pass2:
            raise ValidationError('رمز و تکرار رمز عبور مغایرت دارند')
        return pass1
    
# --------------------------------------------------------------------------------------------------------------------------------------       
class RememberchangeForm(forms.Form):
   mobile_number=forms.CharField(label="شماره موبایل",
                                  error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید'},))