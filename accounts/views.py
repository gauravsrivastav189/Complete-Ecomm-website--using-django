from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontend:home')

        else:
            form = UserCreationForm()
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm(request.POST)
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        signin_form = AuthenticationForm(data=request.POST)
        if signin_form.is_valid():
            user = signin_form.get_user()
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:

                return redirect('frontend:home')

    else:
        signin_form = AuthenticationForm()
    return render(request, 'login.html', {'signin_form': signin_form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('frontend:home')
    else:
        logout(request)
        return redirect('frontend:home')