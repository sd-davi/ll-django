from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'paginas/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics' : topics }
    
    return render(request, 'paginas/topics.html',context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    
    # verifica se usuario loagdo é dono do topico
    
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added')
    context =  {'topic' : topic , 'entries' : entries}
    
    return render(request, 'paginas/topic.html/', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit= False)
            new_topic.owner =  request.user
            form.save()
            return HttpResponseRedirect(reverse('topics'))
    context = {'form' : form}
    return render(request, "paginas/new_topic.html", context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    
     # verifica se usuario loagdo é dono do topico
    
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = EntryForm()
    else: 
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            form.save()
            return HttpResponseRedirect(reverse('topic',args=[topic_id]))
    context = {'topic' : topic ,'form' : form}
    return render(request, "paginas/new_entry.html", context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    
     # verifica se usuario loagdo é dono do topico
    
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # traz anotação já existente
        form =  EntryForm(instance=entry)
    else:
        # salva o dado da requisição sobre a anotação
        form =  EntryForm(instance=entry, data= request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    context = {'topic':topic,'entry':entry, 'form':form}
    return render(request,"paginas/edit_entry.html",context)
        