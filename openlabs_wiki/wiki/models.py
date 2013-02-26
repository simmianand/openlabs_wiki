# -*- coding: utf-8 -*-
"""
    models

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from django.db import models


class Wiki(models.Model):
    """Map wikis to Wiki_History
    """
    link = models.CharField(max_length=50, primary_key=True)
    user = models.CharField(max_length=30)
    wiki_type = models.CharField(max_length=2)
    active_wiki = models.IntegerField()


class WikiHistory(models.Model):
    """Store wiki content
    """
    link = models.ForeignKey(Wiki)
    title = models.CharField(max_length=50)
    content = models.TextField()
    comment = models.TextField()
    pub_date = models.DateTimeField('date published')


class Media(models.Model):
    """Store Images for wiki
    """
    path = models.CharField(max_length=50)
