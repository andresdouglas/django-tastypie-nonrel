from django.db import models

# Create your models here.

from djangotoolbox.fields import ListField, DictField, EmbeddedModelField

class ListFieldTest(models.Model):
    list            =   ListField(models.CharField())
    intlist         =   ListField(models.IntegerField())

class EmbeddedListFieldTest(models.Model):
    list            =   ListField(EmbeddedModelField('PersonTest'))

class DictFieldTest(models.Model):
    dict            =   DictField()

class PersonTest(models.Model):
    name            =   models.CharField(max_length=50)

class EmbeddedModelFieldTest(models.Model):
    customer        =   EmbeddedModelField('PersonTest')
    customer2       =   EmbeddedModelField('PersonTest')
