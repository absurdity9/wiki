from . import util
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect 
from django.http import HttpResponse
from django.http import Http404
import random

class newArticleform(forms.Form):
   title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'style': 'display:block;margin-bottom:10px;'}))    
   contents = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 5em; display:block;margin-bottom:10px;'}))

class searchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'style': 'display:block;margin-bottom:10px;'}))    

class editArticleform(forms.Form):
   title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'style': 'display:block;margin-bottom:10px;'}))    
   contents = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 5em; display:block;margin-bottom:10px;'}))

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
    return render(request, "encyclopedia/wiki.html", {
        # Get the contents of the entry and put it into article
        "article": util.get_entry(title),
        "title": title
    })
    
def randomentry(request):
    list = util.list_entries()
    articletitle = random.choice(list)
    title = articletitle
    return redirect(reverse("wiki", args=[title]))

def search(request):  
    if request.method == "POST":
        
        # Take in the data the user submitted and save it as newSearch    
        newSearch = searchForm(request.POST)
        
        if newSearch.is_valid():
            
            query = newSearch.cleaned_data['query']
            list = util.list_entries()
            # Use list comprehension to make a new list for entries with substrings containing query
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
    
    # Check if its a post request
    if request.method == "POST":

        # Take in the data the user submitted and save it as newForm    
        newForm = newArticleform(request.POST)

        # Check if form data is valid 
        if newForm.is_valid():

            # Isolate the title and content from the 'cleaned' version of form data
            title = newForm.cleaned_data['title']
            contents = newForm.cleaned_data['contents']

            # Save a the new article 
            article = util.save_entry(title, contents) 
            # Redirect the user to the article with the title 
            return HttpResponseRedirect(reverse("wiki", args=[title]))
        
        else:
            return render(request, "encyclopedia/new.html", {
                "form": newForm 
    })
    # If its not a post request, show the form        
    return render(request, "encyclopedia/new.html", {
        "newForm": newArticleform(),
    })

def editor(request, title):
    
    # Check if its a post request
    if request.method == "POST":

        # Take in the data the user submitted and save it as editForm    
        editForm = editArticleform(request.POST)

        # Check if form data is valid 
        if editForm.is_valid():

            # Isolate the title and content from the 'cleaned' version of form data
            title = editForm.cleaned_data['title']
            contents = editForm.cleaned_data['contents']

            # Save a the new article 
            article = util.save_entry(title, contents) 
            # Redirect the user to the article with the title 
            return HttpResponseRedirect(reverse("wiki", args=[title]))
        
        else:
            return render(request, "encyclopedia/editor.html", {
                "editArticleform": editArticleform()
    })
    # If its not a post request, show the form        
    else:
        contents = util.get_entry(title)
        return render(request, "encyclopedia/editor.html", {
        "editArticleform": editArticleform(initial={
            'title': title,
            'contents': contents,
            })
    })
