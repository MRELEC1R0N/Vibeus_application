from .forms import MessageForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Message

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat')
    return render(request, 'login.html')


def chat_view(request):
    if request.user.is_authenticated:
        users = User.objects.all().exclude(id=request.user.id)  # get all users except the current user
        return render(request, 'chat.html', {'users': users})
    else:
        return redirect('login')




def private_chat_view(request, user_id):
    if request.user.is_authenticated:
        other_user = User.objects.get(id=user_id)
        messages = Message.objects.filter(sender__in=[request.user, other_user], receiver__in=[request.user, other_user])
        room_name = f'{request.user.id}_{other_user.id}'  # Create room name
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.receiver = other_user
                message.save()
                return redirect('private_chat', user_id=user_id)
        else:
            form = MessageForm()
        return render(request, 'private_chat.html', {'messages': messages, 'form': form, 'other_user': other_user, 'room_name': room_name})
    else:
        return redirect('login')



def home(request):
    return render(request, 'home.html')