from django.db import models

# Create your models here.

from djangotoolbox.fields import ListField, DictField, EmbeddedModelField

class EmbeddedModelFieldTest(models.Model):
    """
        A model with embedded models
    """
    customer        =   EmbeddedModelField('PersonTest')

class DictFieldTest(models.Model):
    dict            =   DictField()

class ListFieldTest(models.Model):
    """
        A model with basic lists
    """
    list            =   ListField(models.CharField())
    intlist         =   ListField(models.IntegerField())

class EmbeddedListFieldTest(models.Model):
    """
        A model with lists of embedded objects
    """
    list            =   ListField(EmbeddedModelField('PersonTest'))

class EmbeddedCollectionFieldTest(models.Model):
    """
        A model with an embedded collection (i.e. elements in the collection can
        be reordered, etc)
    """
    list            =   ListField(EmbeddedModelField('PersonTest'))


################
# Helper Models
################

class PersonTest(models.Model):
    """
        A simple model
    """
    name            =   models.CharField(max_length=50)

class CustomerTest(models.Model):
    """
        A model with a FK to another model
    """
    person          =   models.ForeignKey('PersonTest')

