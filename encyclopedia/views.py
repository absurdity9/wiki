from django import forms 
from django.shortcuts import render, redirect
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import Http404
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

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
   searchTitle = forms.CharField(widget=forms.TextInput(attrs={'style': 'display:block;margin-bottom:10px;'}))    


def searchentry(request, title):
    list = util.list_entries()
    if title in list:
        return redirect(reverse("wiki", args=[title]))
    else:
        return HttpResponseRedirect(reverse("wiki", args=[title]))


class newArticleform(forms.Form):
   title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'style': 'display:block;margin-bottom:10px;'}))    
   contents = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 5em; display:block;margin-bottom:10px;'}))

# Add a new article
def new(request):
    # Check if its a post request
    if request.method == "POST":

        # Take in the data the user submitted and save it as form    
        form = newArticleform(request.POST)

        # Check if form data is valid 
        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data
            title = form.cleaned_data['title']
            contents = form.cleaned_data['contents']

            # Save a the new article 
            article = util.save_entry(title, contents) 
            # Redirect the user to the article with the title 
            return HttpResponseRedirect(reverse("wiki", args=[title]))
        
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form 
    })
    # If its not a post request, show the form        
    return render(request, "encyclopedia/new.html", {
        "form": newArticleform() 
    })
