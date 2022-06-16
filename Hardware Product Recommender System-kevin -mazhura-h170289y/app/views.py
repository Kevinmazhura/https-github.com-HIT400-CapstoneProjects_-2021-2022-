"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings
from . models import *
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    online_stores = OnlineStore.objects.all()
    products = Product.objects.all()
    return render(
        request,
        'app/index.html',
        {
            'products':products,
            'online_stores': online_stores,
            'MEDIA_URL':settings.MEDIA_URL,
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    if request.POST:
        store = request.POST.get('store')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
