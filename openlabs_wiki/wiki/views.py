# -*- coding: utf-8 -*-
"""
    views

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from wiki.models import wiki

NOW = datetime.datetime.now()


def home(request):
    csrf_obj = {}
    csrf_obj.update(csrf(request))
    return render_to_response("create-wiki.html", csrf_obj)


def save_wiki(request):
    if request.method is not 'POST':
        wiki_id = 1  # temp id
        title = request.POST['title']
        content = request.POST['content']
        comment = request.POST['comment']
        pub_date = NOW
        wiki_type = request.POST['visibility']

        wiki_obj = wiki(
            wiki_id=wiki_id,
            title=title,
            content=content,
            comment=comment,
            pub_date=pub_date,
            wiki_type=wiki_type
        )
        wiki_obj.save()
        return HttpResponse('Saved!')
    else:
        return HttpResponse('Error')
