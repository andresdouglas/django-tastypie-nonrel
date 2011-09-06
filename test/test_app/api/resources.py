from tastypie_nonrel.resources import MongoResource, MongoListResource
from django.conf.urls.defaults import url
from tastypie.utils import trailing_slash


from tastypie.fields import (CharField, 
                             ForeignKey,
                            )
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.bundle import Bundle
from tastypie.exceptions import BadRequest

# Testing
from ..models import (ListFieldTest, 
                      DictFieldTest, 
                      EmbeddedModelFieldTest, 
                      PersonTest,
                      EmbeddedListFieldTest,
                      EmbeddedCollectionFieldTest,
                      CustomerTest,
                    )
from tastypie_nonrel.fields import (ListField, 
                                    DictField, 
                                    EmbeddedModelField, 
                                    EmbeddedListField,
                                    EmbeddedCollection,
                                    )

class EmbeddedModelFieldTestResource(MongoResource):
    customer        =   EmbeddedModelField(embedded='test_app.api.resources.PersonTestResource',
                                           attribute='customer')

    class Meta:
        object_class        =   EmbeddedModelFieldTest
        queryset            =   EmbeddedModelFieldTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

class ListFieldTestResource(MongoResource):
    list            =   ListField(attribute='list')
    intlist         =   ListField(attribute='intlist')

    class Meta:
        object_class        =   ListFieldTest
        queryset            =   ListFieldTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

class DictFieldTestResource(MongoResource):
    dict            =   DictField(attribute='dict')

    class Meta:
        object_class        =   DictFieldTest
        queryset            =   DictFieldTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

class EmbeddedListFieldTestResource(MongoResource):
    list            =   EmbeddedListField(of='test_app.api.resources.PersonTestResource',
                                    attribute='list',
                                    full=True)

    class Meta:
        object_class        =   EmbeddedListFieldTest
        queryset            =   EmbeddedListFieldTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

class EmbeddedCollectionFieldTestResource(MongoResource):
    list            =   EmbeddedCollection(of='test_app.api.resources.PersonTestCollectionResource',
                                           attribute='list',
                                           full=True,
                                           )

    class Meta:
        object_class        =   EmbeddedCollectionFieldTest
        queryset            =   EmbeddedCollectionFieldTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

###################
# Helper Resources
###################

class PersonTestCollectionResource(MongoListResource):
    name            =    CharField(attribute='name')

    class Meta:
        object_class        =   PersonTest
        queryset            =   PersonTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

class PersonTestResource(MongoResource):
    name            =    CharField(attribute='name')

    class Meta:
        object_class        =   PersonTest
        queryset            =   PersonTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

class CustomerTestResource(MongoResource):
    """
        Used to test FK
    """
    person          =   ForeignKey(to='test_app.api.resources.PersonTestResource',
                                   attribute='person',
                                  )
    class Meta:
        object_class        =   CustomerTest
        queryset            =   CustomerTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

