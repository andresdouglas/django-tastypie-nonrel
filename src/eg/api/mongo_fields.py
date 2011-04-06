from tastypie import fields
from tastypie.fields import ApiField, ToOneField, ToManyField, ApiFieldError
from tastypie.bundle import Bundle
import pdb



class ListField(ApiField):
    dehydrated_type     =   'list'

    def dehydrate(self, obj):
        # pdb.set_trace()
        return self.convert(super(ListField, self).dehydrate(obj))

    def convert(self, value):
        # pdb.set_trace()
        if value is None:
            return None
        return value 

class EmbeddedListField(ToManyField):
    is_related = False
    is_m2m = False

    def dehydrate(self, bundle):
        if not bundle.obj or not bundle.obj.pk:
            if not self.null:
                raise ApiFieldError("The model '%r' does not have a primary key and can not be d in a ToMany context." % bundle.obj)
            return []
        if not getattr(bundle.obj, self.attribute):
            if not self.null:
                raise ApiFieldError("The model '%r' has an empty attribute '%s' and doesn't all a null value." % (bundle.obj, self.attribute))
            return []
        self.m2m_resources = []
        m2m_dehydrated = []
        # TODO: Also model-specific and leaky. Relies on there being a
        #       ``Manager`` there.
        # NOTE: only had to remove .all()
        for m2m in getattr(bundle.obj, self.attribute):
            m2m_resource = self.get_related_resource(m2m)
            m2m_bundle = Bundle(obj=m2m)
            self.m2m_resources.append(m2m_resource)
            m2m_dehydrated.append(self.dehydrate_related(m2m_bundle, m2m_resource))
        return m2m_dehydrated

    def hydrate(self, bundle):
        return [b.obj for b in self.hydrate_m2m(bundle)]

class DictField(ApiField):
    dehydrated_type     =   'dict'
    
    def dehydrate(self, obj):
        # pdb.set_trace()
        return self.convert(super(DictField, self).dehydrate(obj))

    def convert(self, value):
        if value is None:
            return None

        return value

class EmbeddedModelField(ToOneField):
    dehydrated_type     =   'embedded'

    def __init__(self, embedded, attribute, null=False, help_text=None):
        '''
            The ``embedded`` argument should point to a ``Resource`` class, NOT
            to a ``Model``. Required.
        '''
        super(EmbeddedModelField, self).__init__(
                                                 to=embedded,
                                                 attribute=attribute,
                                                 null=null,
                                                 full=True,
                                                 help_text=help_text,
                                                )
'''
    def dehydrate(self, obj):
        pdb.set_trace()
        return self.convert(super(EmbeddedModelField, self).dehydrate(obj))

    def convert(self, value):
        pdb.set_trace()
        if value is None:
            return None
'''
        
    # Probably have to override
    # def build_related_resource(self):

