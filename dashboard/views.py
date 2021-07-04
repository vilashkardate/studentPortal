from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.views.generic.detail import DetailView
from youtubesearchpython import VideosSearch
import requests
from django.contrib.auth.decorators import login_required
import wikipedia
# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')

@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm (request.POST)
        if form.is_valid():
            notes = Notes(user = request.user , title = request.POST['title'],description=request.POST['description'])
            notes.save()

        messages.success(request,f'Notes Added from {request.user.username} Succesfully')
    else:
        form  = NotesForm()
    notes = Notes.objects.filter(user = request.user)
    context = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id = pk).delete()
    return redirect ("notes")

class NoteDetailView(DetailView):
    model = Notes

@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request,f'Homework added from {request.user.username} !!')
    else:
            form = HomeworkForm()
    homeworks = Homework.objects.filter(user = request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'homeworks':homeworks,'homework_dont':homework_done,'form':form}
    return render(request,'dashboard/homework.html',context )

    
@login_required
def update_homework(request,pk = None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list =[] 
        for i in video.result()['result']:
            result_dict={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'publish':i['publishedTime'],
                
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return  render(request,'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    context={'form':form}
    return render(request,'dashboard/youtube.html',context)


@login_required
def todo(request):
    if request.method == 'POST':
        form  = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished=='on':
                    finished = True
                else:
                    finished = False
            except :
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f'Todo Added from {request.user.username} !!')
    else:    
        form = TodoForm
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done =True
    else:
        todos_done = False

    context = {
        'todos':todo,
        'form':form,
        'todos_done':todos_done
    }
    return render(request,'dashboard/todo.html',context)

@login_required
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True

    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request,pk = None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')



def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer  = r.json()
        result_list =[] 
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),   
                
            }
            
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return  render(request,'dashboard/books.html',context)
    else:
        form = DashboardForm()
    context={'form':form}
    return render(request,'dashboard/books.html',context)

def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer  = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            defination = answer[0]['meanings'][0]['definations'][0]['defination']
            example = answer[0]['meanings'][0]['definations'][0]['example']
            synonyms = answer[0]['meanings'][0]['definations'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics' : phonetics,
                'audio':audio,
                'defination':defination,
                'example':example,
                'synonyms':synonyms
            }
        except  :
            context = {
                'form':form,
                'input':''
            }
        return render(request,'dashboard/dictionary.html',context)
    else:
        form = DashboardForm()
        context = {'form':form}
    return render(request,'dashboard/dictionary.html',context)


def wiki(request):
    if request.method == 'POST':
        text =   request.POST.get('text')
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        # print(search.title,search.url)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'dashboard/wiki.html',context)
    else:
        form = DashboardForm()
        context = {
            'form':form
        }
    return render(request,'dashboard/wiki.html',context)



def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form =ConversionLengthForm()
            context={
                'form' : form,
                'm_form' : measurement_form,
                'input' :True 
            }
            if 'input' in  request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                inputt = request.POST['input']
                answer = ''
                if inputt and int(inputt) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{inputt} yard = {int(inputt)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{inputt} foot = {int(inputt)/3} yard'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input' : True,
                    'answer':answer
                }
            return render(request,'dashboard/conversion.html',context)

        if request.POST['measurement'] == 'mass':
            measurement_form =ConversionMassForm()
            context={
                'form' : form,
                'm_form' : measurement_form,
                'input' :True 
            }
            if 'input' in  request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                inputt = request.POST['input']
                answer = ''
                if inputt and int(inputt) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{inputt} pound = {int(inputt)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{inputt} kilogram = {int(inputt)*2.20462} pound'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input' : True,
                    'answer':answer
                }
            return render(request,'dashboard/conversion.html',context)
    else:
        form = ConversionForm()
        context ={
            'form':form,
            'input':False
            }
    return render(request,'dashboard/conversion.html',context)



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request,f'Account created for {username} !!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request,'dashboard/register.html',context)


@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user = request.user)
    todo = Todo.objects.filter(is_finished=False,user = request.user)
    if len(homeworks) ==0:
        homework_done = True
    else:
        homework_done = False
    if len(todo) ==0:
        todos_done = True
    else:
        todos_done = False
        
    context={
        'homeworks' : homeworks,
        'todos' : todo,
        'homework_done':homework_done,
        'todos_done':todos_done,
    }
    return render(request,'dashboard/profile.html',context)