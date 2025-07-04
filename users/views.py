from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    ''' sai da pagina'''
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    ''' cria novo usuario'''
    if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        
    # verifica metodo
    if request.method != 'POST':
        #se nao for POST exibe form em branco
        form =  UserCreationForm()
        
    #processa form preenchido
    else:
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            new_user = form.save()
            # faz login
            authenticated_user = authenticate(username = new_user.username, password = request.POST['password1'] )
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))
    
    context = {'form': form}
    return render(request,'users/register.html',context)
            
    