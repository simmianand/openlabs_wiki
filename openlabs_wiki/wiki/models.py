# -*- coding: utf-8 -*-
"""
    models

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from django.db import models

# Create your models here.

TYPE_CHOICES = (
    ('PR','Private'),
    ('PB','Public')
)

class wiki_count(models.Model):
    lastid = models.IntegerField()


class wiki(models.Model):
    wiki_id = models.IntegerField()
    title = models.CharField(max_length=30)
    content = models.TextField()
    comment = models.TextField()
    pub_date = models.DateTimeField('date published')
    wiki_type = models.CharField(max_length=2, choices=TYPE_CHOICES)


class media(models.Model):
    path = models.CharField(max_length=50)
