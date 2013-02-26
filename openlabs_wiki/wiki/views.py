# -*- coding: utf-8 -*-
"""
    views

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime

import markdown
import difflib

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.db import connection, transaction

from wiki.models import *


def error404():
    """ Render 404 Request
    """
    return render_to_response('404.html')


def error403():
    """ Render 403 Request
    """
    return render_to_response('403.html')


def login_check(request):
    """Check if user is logged in or not

    :param request: Fetch SESSION variables
    :return: True if user logged In, False if not.
    """
    request.session['username'] = 'openlabs'
    if 'user' in request.session:
        return True
    else:
        return False


def logout(request):
    try:
        del request.session['username']
        return 1
    except:
        return 0


def fwd_home(request):
    """Forward Url to Home-wiki.

    :param request: No Use.
    :return: Redirecting Url.
    """
    return HttpResponseRedirect('/wiki/home')


def login(request):
    """Forward Url to Home-wiki.

    :param request: No Use.
    :return: Redirecting Url.
    """
    return render_to_response('login.html')


def create_wiki(request):
    """Show create-wiki.html page

    :param request: No Use.
    :return: Render create-wiki.html template
    """
    if not login_check(request):
        return error403()
    csrf_obj = {}
    csrf_obj.update(csrf(request))
    return render_to_response("create-wiki.html", csrf_obj)


def list_wiki(request):
    """List all wiki pages.

    :param request: No Use.
    :return: Rendered html with list of all wiki pages.
    """
    pub_cur = connection.cursor()
    pub_cur.execute("SELECT link, title FROM wiki_wiki, wiki_wikihistory \
        WHERE wiki_wiki.active_wiki = wiki_wikihistory.id AND \
        wiki_wiki.wiki_type = 'PB';")
    pri_cur = connection.cursor()
    pri_cur.execute("SELECT link, title FROM wiki_wiki, wiki_wikihistory \
        WHERE wiki_wiki.active_wiki = wiki_wikihistory.id AND \
        wiki_wiki.user = '"+request.session['username']+"' AND \
        wiki_wiki.wiki_type = 'PR';")
    values = {
        "pub_wiki_list": pub_cur.fetchall(),
        "pri_wiki_list": pri_cur.fetchall(),
    }
    return render_to_response('list-wiki.html', values)


def show_wiki(request, title):
    """Display wiki content as HTML

    :param title: To Map to wiki.
    :return: Render show-wiki.html with wiki content.
    """
    login_check(request)
    if not title:
        title = 'home'

    try:
        user = request.session['username']
    except:
        user = ''

    show_wiki = Wiki.objects.raw("SELECT * FROM wiki_wiki, wiki_wikihistory \
        WHERE wiki_wiki.active_wiki = wiki_wikihistory.id AND \
        LOWER(wiki_wiki.link) = '"+title+"' AND \
            (wiki_wiki.wiki_type = 'PB' OR \
            (wiki_wiki.wiki_type = 'PR' AND \
            wiki_wiki.user = '"+user+"')\
        );")

    try:
        show_wiki = show_wiki[0]
    except:
        return error403()

    content = markdown.markdown(show_wiki.content, safe_mode=True)
    values = {
        "wiki_title": show_wiki.title,
        "wiki_content": content,
        "time": show_wiki.pub_date,
        "user": show_wiki.user,
    }
    return render_to_response('show-wiki.html', values)


def update_wiki(request, title):
    """Insert New Row in table against previous wiki_id

    :param title: To Map to wiki.
    :return: Render update-wiki.html.
    """
    if not login_check(request):
        return error403()
    try:
        user = request.session['username']
    except:
        user = ''

    try:
        last_wiki = Wiki.objects.raw("SELECT * FROM wiki_wiki, \
            wiki_wikihistory \
            WHERE wiki_wiki.active_wiki = wiki_wikihistory.id AND \
            LOWER(wiki_wiki.link) = '"+title+"' AND \
            wiki_wiki.user = '"+user+"'")[0]

        values = {
            "wiki_content": last_wiki.content,
            "wiki_title": last_wiki.title,
            "wiki_type": last_wiki.wiki_type,
            "wiki_id": last_wiki.link,
        }
        values.update(csrf(request))
        return render_to_response('update-wiki.html', values)
    except:
        return error403()


def conv_title(title):
    """ Check if title is unique,
        If yes then convert it to valid string

        :param title: title string to check.
        :return: False or valid title string.
    """
    title = title.lower()
    try:
        last_wiki = Wiki.objects.get(link=title)
        if last_wiki.link:
            return False
    except:
        return title


def update_wiki_check(request):
    """Check if update is allowed or not.

    :return: 1 if allowed allowed.
             2 if No Change.
    """
    try:
        last_wiki = Wiki.objects.raw("SELECT * FROM wiki_wiki WHERE \
            wiki_id = '"+request.POST['wiki_id']+"' ORDER BY pub_date \
            DESC LIMIT 1")[0]
        if (last_wiki.title == request.POST['title'] and
                last_wiki.content == request.POST['content']):
            return 2

        if last_wiki.title == request.POST['title']:
            return 1
    except:
        return 1


def save_wiki(request):
    """Save wiki to database.

    :param request: Read user input from ajax
    :return: json message with error, message [, element] fields.
    """
    if not login_check(request):
        return error403()
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

        link = conv_title(title)
        if link is False:
            return HttpResponse('{\
                "error": "true",\
                "message": "Title is already used.",\
                "element": "title"\
            }')

        wiki_obj = Wiki(
            link=link,
            wiki_type=wiki_type,
            user=request.session['username'],
            active_wiki=0,
        )
        wiki_obj.save()

        wiki_history = WikiHistory(
            link=wiki_obj,
            title=title,
            content=content,
            comment=comment,
            pub_date=datetime.now(),
        )
        wiki_history.save()
        wiki_obj.active_wiki = wiki_history.id
        wiki_obj.save()

        return HttpResponse('{\
                "error": "false",\
                "message": "Wiki Saved",\
                "element": "none"\
            }')
    else:
        return HttpResponse('Error')


def save_update_wiki(request):
    """Update wiki to database.

    :param request: Read user input from ajax
    :return: json message with error, message [, element] fields.
    """
    if not login_check(request):
        return error403()
    if request.method is not 'POST' and 'wiki_id' in request.POST:
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

        else:
            link = request.POST['wiki_id']
#            status = update_wiki_check(request)
#            if status == 2:
#                return HttpResponse('{\
#                    "error": "false",\
#                    "message": "Wiki Saved",\
#                    "element": "none"\
#                }')

        link = conv_title(title)
        if link is False:
            return HttpResponse('{\
                "error": "true",\
                "message": "Title is already used.",\
                "element": "title"\
            }')
        wiki_obj = Wiki.objects.get(
            link=request.POST['wiki_id'],
            user=request.session['username'],
        )
        wiki_obj.wiki_type = wiki_type
        wiki_obj.save()
        wiki_history = WikiHistory(
            link=wiki_obj,
            title=title,
            content=content,
            comment=comment,
            pub_date=datetime.now(),
        )
        wiki_history.save()
        wiki_obj.active_wiki = wiki_history.id
        wiki_obj.save()

        return HttpResponse('{\
                "error": "false",\
                "message": "Wiki Saved",\
                "element": "none"\
            }')
    else:
        return HttpResponse('Error')


def delete_wiki(request, title):
    """Delete wiki page with all previous commits.

    :param request: read wiki_id
    :param title: no use.
    :return: json string with error, message
    """
    if not login_check(request):
        return error403()
    if 'wiki_id' in request.GET and title.lower() != "home":
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM wiki_wiki WHERE \
                wiki_id = "+request.GET['wiki_id'])
            transaction.commit_unless_managed()
            return HttpResponse('{\
                "error": "false",\
                "message": "deleted"\
                }')
        except:
            return HttpResponse('{\
                "error": "true",\
                "message": "Failed"\
                }')
    else:
        return HttpResponse('{\
                "error": "true",\
                "message": "Not Allowed"\
                }')


def history_wiki(request, link):
    """show list history page of wiki

    :param request: no use.
    :return: render history-wiki.html if found wiki, else print error.
    """
    if not login_check(request):
        return error403()
    try:
        wiki_history = Wiki.objects.raw("SELECT wiki_wikihistory.*, \
            wiki_wiki.link FROM wiki_wiki, wiki_wikihistory WHERE link = \
            '"+link+"' AND wiki_wiki.link = wiki_wikihistory.link_id \
            ORDER BY pub_date DESC;")
        values = {
            'wiki_history_list': wiki_history,
            'title': link,
        }
        values.update(csrf(request))
        return render_to_response('history-wiki.html', values)
    except:
        raise
        return HttpResponse('error')


def history_show_wiki(request, title, history_id):
    """Display history for wiki.

    :param title: Title of wiki.
    :param history_id: ID of history.
    :return: Show previous wiki version if wiki exist. Else 'error'
    """
    if not login_check(request):
        return error403()
    try:
        show_wiki = Wiki.objects.raw("SELECT wiki_wikihistory.*, \
            wiki_wiki.user, wiki_wiki.link FROM wiki_wikihistory, \
            wiki_wiki WHERE wiki_wikihistory.link_id = wiki_wiki.link AND \
            wiki_wikihistory.id = "+history_id+";")[0]
        content = markdown.markdown(show_wiki.content, safe_mode=True)
        time = show_wiki.pub_date
        values = {
            "wiki_title": show_wiki.title,
            "wiki_content": content,
            "time": time,
            "user": show_wiki.user,
        }

        return render_to_response('show-history-wiki.html', values)
    except:
        return HttpResponse('error')


def compare_wiki(request, title):
    """compare wikis

    :param request: get wiki_ids from user
    :return: render compare-wiki.html if wiki exist else error.
    """
    if not login_check(request):
        return error403()
    if 'wiki1' in request.POST:
        diff = difflib.Differ()
        wiki1 = WikiHistory.objects.get(id=request.POST['wiki1'])
        wiki2 = WikiHistory.objects.get(id=request.POST['wiki2'])
        values = {
            'content': list(diff.compare(wiki2.content.split('\n'),
            wiki1.content.split('\n'))),
            'title': title,
        }
        return render_to_response('compare-wiki.html', values)
    else:
        return HttpResponse('error')
