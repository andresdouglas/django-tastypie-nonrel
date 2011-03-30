import unittest

from django.test import TestCase
from django.http import HttpRequest

from django.test import TestCase
import settings
import pdb

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
        print_resp(resp)
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized['objects']), 3)

    def test_post(self):
        post_data = '{"list":["1", "2"], "intlist":[1,2]}'
        resp = self.client.post('/api/v1/listfieldtest/',
                                data = post_data,
                                content_type = 'application/json'
                               )

        self.assertEqual(resp.status_code, 201)

        resp = self.client.get('/api/v1/listfieldtest/', 
                               content_type='application/json') 
        print_resp(resp)
        self.assertEqual(resp.status_code, 200)

        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized['objects']), 4)

    def test_put(self):
        resp = self.client.get('/api/v1/listfieldtest/',
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200) 
        
        deserialized = json.loads(resp.content)
        l = deserialized['objects'][0]
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

    def test_delete(self):
        pass

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
        l.list.append(p1)
        l.save()
                                        

    def test_get(self):
        resp = self.client.get('/api/v1/embeddedlistfieldtest/',
                               content_type='application/json') 
        print_resp(resp)
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized['objects']), 1)

    #################### 
    # Big Bag of FAIL
    ####################
    def test_post(self):
        post_data = '{"list":[{"name":"evan"}, {"name":"ethan"}]}'
        resp = self.client.post('/api/v1/embeddedlistfieldtest/',
                                data = post_data,
                                content_type = 'application/json'
                               )

        print_resp(resp)
        self.assertEqual(resp.status_code, 201)
        # pdb.set_trace()

        resp = self.client.get('/api/v1/embeddedlistfieldtest/', 
                               content_type='application/json') 
        print_resp(resp)
        self.assertEqual(resp.status_code, 200)

        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized['objects']), 2)
        
############################################
# DICTS
############################################

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
        print_resp(resp)
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
        print_resp(resp)
        self.assertEqual(resp.status_code, 200)

    def test_put(self):
        resp = self.client.get('/api/v1/dictfieldtest/',
                               content_type='application/json') 
        self.assertEqual(resp.status_code, 200) 
        print_resp(resp) 
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
        print_resp(resp)
        deserialized = json.loads(resp.content)
        # it's last, because when you delete an element in a list it gets pushed
        # to the back
        l = deserialized['objects'][3]
        self.assertEquals(l['dict'], {'1':'one', 'two':2})
 
    def test_delete(self):
        pass

class EmbededModelFieldTest(TestCase):
    def setUp(self):
        from django.conf import settings; settings.DEBUG = True
        from models import PersonTest, EmbeddedModelFieldTest
        m = EmbeddedModelFieldTest.objects.create(
                           customer=PersonTest(name="andres"),
                           customer2=PersonTest(name="douglas"),
                                                 )
        ms = EmbeddedModelFieldTest.objects.all()
        for m in ms:
            print m

    def test_get(self):
        request = HttpRequest()
        resp = self.client.get('/api/v1/embeddedmodelfieldtest/',
                               content_type='application/json',
                               )
        print_resp(resp)
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        request = HttpRequest()
        post_data = '{"customer":{"name":"san"}, "customer2":{"name":"francis"}}'
        resp = self.client.post('/api/v1/embeddedmodelfieldtest/',
                               data=post_data,
                               content_type='application/json',
                               )
        self.assertEqual(resp.status_code, 201)
        # make sure it's there
        resp = self.client.get('/api/v1/embeddedmodelfieldtest/',
                               content_type='application/json',
                               )
        print_resp(resp)
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized['objects']), 2)

    def test_put(self):
        resp = self.client.get('/api/v1/embeddedmodelfieldtest/',
                               content_type='application/json',
                               )

        deserialized = json.loads(resp.content)
        p = deserialized['objects'][0]
        # change it
        p['customer']['name'] = "philip"
        put_data = json.dumps(p)
        put_data = '{"customer":{"name":"philip"}}'
        print "put data ", put_data
        location = p['resource_uri']
        resp = self.client.put(location,
                               data=put_data,
                               content_type='application/json',
                              )
        resp = self.client.get('/api/v1/embeddedmodelfieldtest/',
                               content_type='application/json',
                               )
        deserialized = json.loads(resp.content)
        self.assertEqual(deserialized['objects'][0]['customer']['name'],
                         'philip')

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
