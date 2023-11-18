from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required #only for functions, not classess!


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome, {username}, to the blog!!! You are now able to log in)')
            return redirect('login')
    else:
        form = UserRegisterForm()
    # else:
    #     form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
#flash messages, e.g. appear only 1 time


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            name = u_form.cleaned_data.get('username')
            mail = u_form.cleaned_data.get('email')
            messages.success(request, f'{name}, Your account with {mail} have been updated !')
            return redirect('profil')
            # redirect command causes the browser send a get request
            #because of POST.get.redirect  pattern: otherwise: 
            #Страница, которую вы ищете, использовала введенную информацию. 
            #Возврат на эту страницу может привести к повторению любого из действий, которые вы предприняли.
            #Продолжить?
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form 
        }
    return render(request, 'users/profile.html', context)


# messages.success
# messages.warning
# messages.error
# messages.debug