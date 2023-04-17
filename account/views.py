from django.shortcuts import render,redirect
from django.views import View
from .forms import *
import utilis
from .models import *
from django.contrib import messages
from django.contrib.auth import login,authenticate, logout


# --------------------------------------------------------------------------------------------------------------------------------------
class RegisterUser(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
             return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    # --------------------------------------------------------------
    template_name='account/RegisterUser.html'
    def get(self,request,*args,**kwargs):
        form=UserRegisterForm()
        return render(request,self.template_name,{'form':form})
    
    # --------------------------------------------------------------   
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
             return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    # --------------------------------------------------------------    
    def post(self,request,*args,**kwargs):
        form=UserRegisterForm(request.POST)
        if form. is_valid():
            data=form.cleaned_data
            active_code=utilis.create_random_code(5)
            CustomerUser.objects.create_user(
                mobile_number=data['mobile_number'],
                active_code=active_code,
                password=data['password1']
                
            )
            request.session['user_session']={
                'active_code':str(active_code),
                'mobile_number':data['mobile_number'],
                'remember_change':False

            }       
            messages.success(request,' اطلاعات شما ثبت شد.کد فعال سازی را وارد کنید','success')
            return redirect('account:verify')
        messages.error(request,'اطلاعات وارد شده معتبر نمیباشد','danger')
        return redirect('account:register')

# --------------------------------------------------------------------------------------------------------------------------------------
class verifyUser(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
             return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    # --------------------------------------------------------------    
    template_name='account/verifyuser.html'
    def get(self,request,*args,**kwargs):
        form=verifyUserForm()
        return render(request,self.template_name,{'form':form})
    
    # --------------------------------------------------------------   
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
             return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    # --------------------------------------------------------------    
    def post(self,request,*args,**kwargs):
        form=verifyUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session= request.session['user_session']
            if data['active_code']==user_session['active_code']:
                user=CustomerUser.objects.get(mobile_number=user_session['mobile_number'])
                if user_session['remember_change'] ==False:
                    user.is_active=True
                    user.active_code=utilis.create_random_code(5)
                    user.save()
                    messages.success(request,'ثبت نام با موفقیت انجام شد','success')
                    return redirect('main:index')
                else:
                    return redirect('account:changepass')

            messages.error(request,'کد وارد شده معتبر نمیباشد','danger')
            return redirect('account:verify')
        messages.error(request,'اطلاعات وارد شده معتبر نمیباشد','danger')
        return redirect('account:verify')

# --------------------------------------------------------------------------------------------------------------------------------------
class LoginUser(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
             return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    # --------------------------------------------------------------    
    template_name='account/loginuser.html'
    def get(self,request,*args,**kwargs):
        form=LoginUserForm()
        return render(request,self.template_name,{'form':form})
    
    # --------------------------------------------------------------    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
             return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    # --------------------------------------------------------------      
    def post(self,request,*args,**kwargs):
        form=LoginUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(username=data['mobile_number'],password=data['password'])
            if user is not None:
                db_user=CustomerUser.objects.get(mobile_number=data['mobile_number'])
                if db_user.is_admin==False:
                        messages.success(request,' ورود با موفقیت انجام شد','success')
                        login(request,user)
                        next_url=request.GET.get('next')
                        if next_url is not None:
                            return redirect(next_url)
                        else:
                            return redirect('main:index')
                else:
                        messages.warning(request,' ادمین نمیتواند از اینجا وارد شود','warning')
                        return render(request,self.template_name,{'form':form})              
            else:
                messages.error(request,'اطلاعات وارد شده کسشر است','danger')
                return render(request,self.template_name,{'form':form})
        messages.error(request,'اطلاعات وارد شده معتبر نمیباشد','danger')
        return render(request,self.template_name,{'form':form})

              
 # --------------------------------------------------------------------------------------------------------------------------------------
class LogoutUser(View):
    
    def dispatch(self, request, *args, **kwargs): 
        if not request.user.is_authenticated:
             return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    # --------------------------------------------------------------    
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('main:index')

            
 # --------------------------------------------------------------------------------------------------------------------------------------
class UserpanelView(View):
     template_name='account/userpanel.html'
     def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    
 # --------------------------------------------------------------------------------------------------------------------------------------
class changepasswordview(View):
    template_name='account/changepassword.html'
    def get(self,request,*args,**kwargs):
        form=changeUserForm()
        return render(request,self.template_name,{'form':form})
    
    # --------------------------------------------------------------
    def post(self,request,*args,**kwargs):
        form=changeUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session= request.session['user_session']
            user=CustomerUser.objects.get(mobile_number=user_session['mobile_number'])
            user.set_password(data['password1'])
            user.active_code=utilis.create_random_code(5)
            user.save()
            messages.success(request,'تغییر رمز شما با موفقیت انجام شد','success')
            return redirect('account:login')
        
        messages.error(request,'اطلاعات وارد شده معتبر نمیباشد','danger')
        return render(request,self.template_name,{'form':form})

 # --------------------------------------------------------------------------------------------------------------------------------------
class RememberchangeUser(View):
    template_name='account/Rememberchange.html'
    def get(self,request,*args,**kwargs):
        form=RememberchangeForm()
        return render(request,self.template_name,{'form':form})
    
    # --------------------------------------------------------------    
    def post(self,request,*args,**kwargs):
        form=RememberchangeForm(request.POST)
        if form.is_valid():
            try:
                data=form.cleaned_data
                user=CustomerUser.objects.get(mobile_number=data['mobile_number'])
                active_code=utilis.create_random_code(5)
                user.active_code=active_code
                user.save()
                request.session['user_session']={
                    'active_code':str(active_code),
                    'mobile_number':data['mobile_number'],
                    'remember_change':True
                }       
                messages.success(request,'    .کد دریافتی را ارسال  کنید','success')
                return redirect('account:verify')
            except:
                    messages.error(request,'شماره موبایل وارد شده معتبر نمیباشد','danger')
                    return render(request,self.template_name,{'form':form})


                
            