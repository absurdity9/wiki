from django import forms 
from django.shortcuts import render, redirect
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect 
from django.http import HttpResponse
from django.http import Http404
import random

def index(request):
    context ={
        "entries": util.list_entries(),
        "searchForm": searchForm()
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

class searchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'style': 'display:block;margin-bottom:10px;'}))    

def search(request):
    
    # Check if its a post request
    if request.method == "POST":
        
        # Take in the data the user submitted and save it as newSearch    
        newSearch = searchForm(request.POST)
        print("Search fx being called")
        
        if newSearch.is_valid():
            
            # Isolate the query title from the 'cleaned' version of form data            
            title = newSearch.cleaned_data['query']
            print(title)
            
            # Get the list of entries
            list = util.list_entries()
            print(list)
            
            if title in list:
                print("True")
                return HttpResponseRedirect(reverse("wiki", args=[title]))
            else:
                print("False")                
                raise Http404("No article was found with this title")
        else:
            raise Http404("Search is not valid")
    else:
        raise Http404("Unknown error")

class newArticleform(forms.Form):
   title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'style': 'display:block;margin-bottom:10px;'}))    
   contents = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 5em; display:block;margin-bottom:10px;'}))

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

def error(request):
     return HttpResponse("Error")