from tastypie.resources import ModelResource, Resource
from django.conf.urls.defaults import url
from tastypie.utils import trailing_slash


from tastypie import fields
from tastypie.fields import CharField, ToOneField
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.bundle import Bundle
from tastypie.exceptions import BadRequest

# Testing
from ..models import ListFieldTest, DictFieldTest, EmbeddedModelFieldTest, PersonTest, EmbeddedListFieldTest
from mongo_fields import ListField, DictField, EmbeddedModelField, EmbeddedListField


class PersonTestResource(ModelResource):
    name            =    CharField(attribute='name')

    class Meta:
        object_class        =   PersonTest
        queryset            =   PersonTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

class ListFieldTestResource(ModelResource):
    list            =   ListField(attribute='list')
    intlist         =   ListField(attribute='intlist')

    class Meta:
        object_class        =   ListFieldTest
        queryset            =   ListFieldTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

class EmbeddedListFieldTestResource(ModelResource):
    list            =   EmbeddedListField(to=PersonTestResource,
                                    attribute='list',
                                    full=True)

    class Meta:
        object_class        =   EmbeddedListFieldTest
        queryset            =   EmbeddedListFieldTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

    def obj_create(self, bundle, request=None, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """
        bundle.obj = self._meta.object_class()
        
        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)
        
        bundle = self.full_hydrate(bundle)
        
        # Now pick up the M2M bits.
        m2m_bundle = self.hydrate_m2m(bundle)
        self.save_m2m(m2m_bundle)

        bundle.obj.save()
        return bundle

    def hydrate_m2m(self, bundle):
        ret = super(EmbeddedListFieldTestResource, self).hydrate_m2m(bundle)
        return ret

class DictFieldTestResource(ModelResource):
    dict            =   DictField(attribute='dict')

    class Meta:
        object_class        =   DictFieldTest
        queryset            =   DictFieldTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()

class EmbeddedModelFieldTestResource(ModelResource):
    customer        =   EmbeddedModelField(embedded=PersonTestResource,
                                           attribute='customer')
    customer2       =   EmbeddedModelField(embedded=PersonTestResource,
                                           attribute='customer2')

    class Meta:
        object_class        =   EmbeddedModelFieldTest
        queryset            =   EmbeddedModelFieldTest.objects.all()
        allowed_methods     =   ['get', 'post', 'put', 'delete']
        authorization       =   Authorization()
        authentication      =   Authentication()
