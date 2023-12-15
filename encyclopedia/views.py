from . import util
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect 
from django.http import HttpResponse
from django.http import Http404
import random
import markdown2

class newArticleform(forms.Form):
   title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'style': 'display:block;margin-bottom:10px;'}))    
   contents = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 5em; display:block;margin-bottom:10px;'}))

class searchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'style': 'display:block;margin-bottom:10px;width:180px;'}))    

class editArticleform(forms.Form):
   title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'style': 'display:block;margin-bottom:10px;'}))    
   contents = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 5em; display:block;margin-bottom:10px;height:600px;'}))

def index(request):
    context ={
        "entries": util.list_entries(),
        "searchForm": searchForm(),
        "editArticleform": editArticleform(),
    }
    return render(request, "encyclopedia/index.html", context)

def directory(request, title):
    list = util.list_entries()
    if title in list:
        #return HttpResponseRedirect(reverse("entries{title}.md"))
        article = util.get_entry(title)
        return HttpResponseRedirect(reverse("wiki", args=[title]))
    else:
        raise Http404("This article does not exist. Go back to create one.")
         
def wiki(request, title):
    markdown_article = util.get_entry(title)
    html_content = markdown2.markdown(markdown_article)
    return render(request, "encyclopedia/wiki.html", {
        # Get the contents of the entry and put it into article
        'html_content': html_content,
        "title": title,
        "searchForm": searchForm(),
    })
    
def randomentry(request):
    list = util.list_entries()
    articletitle = random.choice(list)
    title = articletitle
    return redirect(reverse("wiki", args=[title]))

def search(request):  
    if request.method == "POST":
        
        newSearch = searchForm(request.POST)
        
        if newSearch.is_valid():
            
            query = newSearch.cleaned_data['query']
            list = util.list_entries()
            matchingEntries = [entry for entry in list if query.lower() in entry.lower()]
            if len(matchingEntries) == 1:
                return HttpResponseRedirect(reverse("wiki", args=[matchingEntries[0]]))
            else:
                print(matchingEntries)
                return render(request, "encyclopedia/searchresults.html", {
                    "matchingEntries": matchingEntries
                })
        else:
            raise Http404("Search is not valid")
    else:
        raise Http404("Unknown error")

def new(request):
    
    if request.method == "POST":
        newForm = newArticleform(request.POST)

        if newForm.is_valid():

            title = newForm.cleaned_data['title']
            contents = newForm.cleaned_data['contents']

            article = util.save_entry(title, contents) 
            return HttpResponseRedirect(reverse("wiki", args=[title]))
        
        else:
            return render(request, "encyclopedia/new.html", {
                "form": newForm,
                "searchForm": searchForm(),
    })
    return render(request, "encyclopedia/new.html", {
        "newForm": newArticleform(),
        "searchForm": searchForm(),
    })

def editor(request, title):
    
    if request.method == "POST":
        editForm = editArticleform(request.POST)

        if editForm.is_valid():

            title = editForm.cleaned_data['title']
            contents = editForm.cleaned_data['contents']

            article = util.save_entry(title, contents) 
            return HttpResponseRedirect(reverse("wiki", args=[title]))
        
        else:
            return render(request, "encyclopedia/editor.html", {
                "editArticleform": editArticleform(),
                "searchForm": searchForm(),
    })
    else:
        contents = util.get_entry(title)
        return render(request, "encyclopedia/editor.html", {
        "editArticleform": editArticleform(initial={
            'title': title,
            'contents': contents,
            "searchForm": searchForm(),
            })
    })
