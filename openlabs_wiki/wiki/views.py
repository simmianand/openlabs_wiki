# -*- coding: utf-8 -*-
"""
    views

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from wiki.models import *


def create_wiki(request):
    csrf_obj = {}
    csrf_obj.update(csrf(request))
    return render_to_response("create-wiki.html", csrf_obj)

def get_wiki_id():
    lastcount = wiki_count.objects.get(id=1)
    lastcount.lastid=lastcount.lastid+1
    lastcount.save()
    return lastcount.lastid


def show_wiki(request):
    lastcount = wiki_count.objects.get(id=1)
    lastcount.lastid=lastcount.lastid+1
    lastcount.save()
    return HttpResponse(lastcount.lastid)

def update_wiki(request):
    try:
        last_wiki = wiki.objects.raw("SELECT * FROM wiki_wiki WHERE wiki_id = %s ORDER BY pub_date DESC LIMIT 1" % request.GET['wiki_id'])[0]
        values = {
            "wiki_content": last_wiki.content,
            "wiki_title": last_wiki.title,
            "wiki_type": last_wiki.wiki_type,
            "wiki_id": last_wiki.wiki_id,
            }
        values.update(csrf(request))
        return render_to_response('update-wiki.html', values)
    except:
        return HttpResponse("error")
        #return HttpResponseRedirect('create_wiki')

def save_wiki(request):
    if request.method is not 'POST':
        try:
            title = request.POST['title']
            content = request.POST['content']
            comment = request.POST['comment']
            wiki_type = request.POST['visibility']
        except:
            return HttpResponse('{\
                "error": "true",\
                "message": "fill form properly"\
            }')

        if len(title) > 30 or len(title) < 2:
            return HttpResponse('{\
                "error": "true",\
                "message": "title is too long or too short.",\
                "element": "title"\
            }')

        if len(content) < 3:
            return HttpResponse('{\
                "error": "true",\
                "message": "Wiki content too short.",\
                "element": "content"\
            }')

        if len(wiki_type) != 2 or wiki_type != 'PR' and wiki_type != 'PB':
            return HttpResponse('{\
                "error": "true",\
                "message": "set correct visibility",\
                "element": "visibility"\
            }')

        if not request.POST['wiki_id']:
            wiki_id = get_wiki_id()
        else:
            wiki_id=request.POST['wiki_id']


        wiki_obj = wiki(
            wiki_id=wiki_id,
            title=title,
            content=content,
            comment=comment,
            pub_date=datetime.datetime.now(),
            wiki_type=wiki_type,
        )
        wiki_obj.save()
        return HttpResponse('{\
                "error": "false",\
                "message": "Wiki Saved",\
                "element": "none"\
            }')
    else:
        return HttpResponse('Error')
