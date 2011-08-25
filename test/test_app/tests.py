import unittest

from django.test import TestCase
from django.http import HttpRequest

from django.test import TestCase
import settings

try:
    import json
except ImportError:
    import simplejson as json

def print_resp(resp):
   if not resp.content:
       return
   try:
       deserialized = json.loads(resp.content)
       if 'error_message' in deserialized.keys():
           print "ERROR: ", deserialized.get('error_message', '')
           print "TRACEBACK: ", deserialized.get('traceback', '')
       print json.dumps(deserialized, indent=4)
   except:
       print "resp is not json: ", resp
############################################
# LISTS
############################################
class ListFieldTest(TestCase):
    # fixtures = ['list_field_test.json', 'dict_field_test.json']

    def setUp(self):
        from django.conf import settings; settings.DEBUG = True
        from models import ListFieldTest, DictFieldTest
        l = ListFieldTest.objects.create(
                                         list=[1,2,3],
                                         intlist=[1,2,3],
                                        )
        l = ListFieldTest.objects.create(
                                         list=[1.0,2.0,3.0],
                                         intlist=[1.0,2.0,3.0],
                                        )
        l = ListFieldTest.objects.create(
                                         list=[1,2,3],
                                         intlist=['1','2','3'],
                                        )

    def test_get(self):
        resp = self.client.get('/api/v1/listfieldtest/',
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)

        os = deserialized['objects']
        self.assertEqual(len(os), 3)
        
        self.assertEqual(os[0]['intlist'], [1,2,3])
        self.assertEqual(os[0]['list'], ['1','2','3'])

        # Objects get transformed to the underlying type of the list
        self.assertEqual(os[1]['intlist'], [1,2,3])
        

    def test_post(self):
        post_data = '{"list":["1", "2"], "intlist":[1,2]}'
        resp = self.client.post('/api/v1/listfieldtest/',
                                data = post_data,
                                content_type = 'application/json'
                               )

        self.assertEqual(resp.status_code, 201)

        resp = self.client.get('/api/v1/listfieldtest/', 
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200)

        deserialized = json.loads(resp.content)
        os = deserialized['objects']
        self.assertEqual(len(os), 4)
        self.assertEqual(os[3]['intlist'], [1,2])
        self.assertEqual(os[3]['list'], ['1','2'])

    def test_put(self):
        resp = self.client.get('/api/v1/listfieldtest/',
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200) 
        
        deserialized = json.loads(resp.content)
        os = deserialized['objects']
        l = os[0]
        l['list'] = [4,5]
        location = l['resource_uri']
        put_data = json.dumps(l)

        resp = self.client.put(location,
                               data=put_data,
                               content_type='application/json')
        self.assertEqual(resp.status_code, 204) 
        
        # make sure the update happened
        resp = self.client.get('/api/v1/listfieldtest/',
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200) 

        deserialized = json.loads(resp.content)
        l = deserialized['objects'][0]
        # the list is of Charfield
        self.assertEquals(l['list'], ['4','5'])
        
        resp = self.client.get(location,
                               content_type='application/json')
         
        deserialized = json.loads(resp.content)
        self.assertEqual(deserialized['list'], ['4', '5'])

    def test_delete(self):
        resp = self.client.get('/api/v1/listfieldtest/',
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200) 
        
        deserialized = json.loads(resp.content)
        os = deserialized['objects']
        old_len = len(os)
        location = os[0]['resource_uri']

        resp = self.client.delete(location,
                                  content_type='application/json')

        self.assertEquals(resp.status_code, 204)

        # make sure it's gone
        resp = self.client.get('/api/v1/listfieldtest/',
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200) 
        deserialized = json.loads(resp.content)
        os = deserialized['objects']  
        self.assertEquals(len(os), old_len - 1)
        
############################################
# EMBEDDED LISTS
############################################
        
class EmbeddedListFieldTest(TestCase):
    # fixtures = ['list_field_test.json', 'dict_field_test.json']

    def setUp(self):
        from django.conf import settings; settings.DEBUG = True
        from models import EmbeddedListFieldTest, PersonTest
        p       = PersonTest(name="andres")
        p1      = PersonTest(name="arman")
        l       = EmbeddedListFieldTest.objects.create()
        l.list.append(p)
        l.save()
        l.list.append(p1)
        l.save()

    def test_get(self):
        resp = self.client.get('/api/v1/embeddedlistfieldtest/',
                               content_type='application/json') 

        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        os = deserialized['objects']
        self.assertEqual(len(os), 1)
        self.assertEqual(os[0]['list'][0]['name'], 'andres') 

    def test_post(self):
        post_data = '{"list":[{"name":"evan"}, {"name":"ethan"}]}'
        resp = self.client.post('/api/v1/embeddedlistfieldtest/',
                                data = post_data,
                                content_type = 'application/json'
                               )
        self.assertEqual(resp.status_code, 201)
        
        location = resp['location']

        resp = self.client.get('/api/v1/embeddedlistfieldtest/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        deserialized = json.loads(resp.content)
        os = deserialized['objects']
        self.assertEqual(len(os), 2)
        self.assertEqual(os[1]['list'][0]['name'], 'evan')

    def test_put(self):
        resp = self.client.get('/api/v1/embeddedlistfieldtest/',
                               content_type='application/json',
                               )

        deserialized = json.loads(resp.content)
        p = deserialized['objects'][0]
        p['list'][0]['name'] = "philip"
        location = p['resource_uri']
        # submit completely new data
        put_data = '{"list":[{"name":"evan"}, {"name":"ethan"}]}'

        resp = self.client.put(location,
                               data=put_data,
                               content_type='application/json',
                              )
        self.assertEquals(resp.status_code, 204)

        resp = self.client.get(location,
                               content_type='application/json',
                               )
        deserialized = json.loads(resp.content)

        self.assertEqual(len(deserialized['list']), 2)
        self.assertEqual(deserialized['list'][0]['name'], 'evan')
        self.assertEqual(deserialized['list'][1]['name'], 'ethan')
        

    def test_delete(self):
        resp = self.client.get('/api/v1/embeddedlistfieldtest/',
                               content_type='application/json',
                               )

        deserialized = json.loads(resp.content)
        location = deserialized['objects'][0]['resource_uri'] 
        resp = self.client.delete(location,
                                  content_type='application/json')
        self.assertEqual(resp.status_code, 204)
        # make sure it's actually gone
        resp = self.client.get('/api/v1/embeddedlistfieldtest/',
                               content_type='application/json',
                               )
        deserialized = json.loads(resp.content)
        # boom
        self.assertEqual(len(deserialized['objects']), 0)
        
        
############################################
# DICTS
############################################
"""
class DictFieldTest(TestCase):

    def setUp(self):
        from django.conf import settings; settings.DEBUG = True
        from models import ListFieldTest, DictFieldTest
        l = DictFieldTest.objects.create(
                                         dict={"1":1, '2':'2',})
        l = DictFieldTest.objects.create(
                                         dict={"1":1, '2':'2', '3':[1,2,3]})
        l = DictFieldTest.objects.create(
                                         dict={"1":1, 
                                               '2':'2', 
                                               'latlon':[1.234, 2.3443],
                                               '3':[1,2,3],
                                               '4':{'1':1},
                                              },
                                        )
        l = DictFieldTest.objects.create(
                                         dict={"1":1,
                                               '2':'2',
                                              })

    def test_get(self):
        resp = self.client.get('/api/v1/dictfieldtest/', 
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        post_data = '{"dict":{"1":1, "2":"2", "3":[1,2,3], "4":{"1":1}}}'
        resp = self.client.post('/api/v1/dictfieldtest/',
                                data = post_data,
                                content_type = 'application/json'
                               )

        self.assertEqual(resp.status_code, 201)

        resp = self.client.get('/api/v1/dictfieldtest/', 
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200)

    def test_put(self):
        resp = self.client.get('/api/v1/dictfieldtest/',
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200) 
        deserialized = json.loads(resp.content)
        l = deserialized['objects'][0]
        l['dict'] = {'1':'one', 'two':2}
        location = l['resource_uri']
        put_data = json.dumps(l)

        resp = self.client.put(location,
                               data=put_data,
                               content_type='application/json')
        self.assertEqual(resp.status_code, 204) 
        
        # make sure the update happened
        resp = self.client.get('/api/v1/dictfieldtest/',
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200) 
        deserialized = json.loads(resp.content)
        # it's last, because when you delete an element in a list it gets pushed
        # to the back
        l = deserialized['objects'][3]
        self.assertEquals(l['dict'], {'1':'one', 'two':2})
 
    def test_delete(self):
        pass

"""

############################################
# EMBEDDED
############################################
class EmbededModelFieldTest(TestCase):
    def setUp(self):
        from django.conf import settings; settings.DEBUG = True
        from models import PersonTest, EmbeddedModelFieldTest
        m = EmbeddedModelFieldTest.objects.create(
                           customer=PersonTest(name="andres"),
                                                 )
        ms = EmbeddedModelFieldTest.objects.all()

    def test_get(self):
        request = HttpRequest()
        resp = self.client.get('/api/v1/embeddedmodelfieldtest/',
                               content_type='application/json',
                               )
        self.assertEqual(resp.status_code, 200)
        rj = json.loads(resp.content)
        self.assertEqual(rj['objects'][0]['customer']['name'], 'andres')

    def test_post(self):
        request = HttpRequest()
        post_data = '{"customer":{"name":"san"}}'
        resp = self.client.post('/api/v1/embeddedmodelfieldtest/',
                               data=post_data,
                               content_type='application/json',
                               )
        self.assertEqual(resp.status_code, 201)
        # make sure it's there
        resp = self.client.get('/api/v1/embeddedmodelfieldtest/',
                               content_type='application/json',
                               )
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized['objects']), 2)
        self.assertEqual(deserialized['objects'][1]['customer']['name'], 'san')

    def test_put(self):
        resp = self.client.get('/api/v1/embeddedmodelfieldtest/',
                               content_type='application/json',
                               )

        deserialized = json.loads(resp.content)
        p = deserialized['objects'][0]
        p['customer']['name'] = "philip"
        put_data = json.dumps(p)

        location = p['resource_uri']
        resp = self.client.put(location,
                               data=put_data,
                               content_type='application/json',
                              )
        self.assertEquals(resp.status_code, 204)

        resp = self.client.get(location,
                               content_type='application/json',
                               )
        deserialized = json.loads(resp.content)

        self.assertEqual(deserialized,
                         p)

        resp = self.client.get('/api/v1/embeddedmodelfieldtest/',
                               content_type='application/json',
                               )

        deserialized = json.loads(resp.content)
        self.assertEquals(len(deserialized['objects']), 1)
        p = deserialized['objects'][0]
        self.assertEquals(p['customer']['name'], "philip")

    def test_delete(self):
        resp = self.client.get('/api/v1/embeddedmodelfieldtest/',
                               content_type='application/json',
                               )

        deserialized = json.loads(resp.content)
        location = deserialized['objects'][0]['resource_uri'] 
        resp = self.client.delete(location,
                                  content_type='application/json')
        self.assertEqual(resp.status_code, 204)
        # make sure it's actually gone
        resp = self.client.get('/api/v1/embeddedmodelfieldtest/',
                               content_type='application/json',
                               )
        deserialized = json.loads(resp.content)
        # boom
        self.assertEqual(len(deserialized['objects']), 0)


############################
# EmbeddedCollections
############################

