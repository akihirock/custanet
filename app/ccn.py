# coding:UTF-8
from google.appengine.ext import ndb
import logging

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

class CcnUtils(object):
    
    def to_json(self):
        result = super(CcnUtils,self).to_dict()
        result['key'] = self.key.id()
        curl = result["url"].get()
        curlObj = {'id':result["url"].id(),"ttl":curl.ttl}
        result['url'] = curlObj
        
        cusers = []
        """
        for c in result["usr"]:
            cuser = c.get()
            cuserObj = { "id":c.id(),"nam":cuser.nam}
            cusers.append(cuserObj)
        result['usr'] = cusers
        """
        for c in result["usr"]:
            cuser = c.get()
            cusers.append(cuser.nam)
        result['usr'] = cusers        
        
        return result
 
    
    def to_j(self):
        result = super(CcnUtils,self).to_dict()
        for k in result.keys():
            if k=="key":
                result[k] = self.key.id().__str__()
            elif result[k] is None:
                result[k] = ""
            elif k=="dat":
                result[k] = result[k].strftime('%Y/%m/%d %H:%M:%S')
                    
        curl = result["url"].get()
        curlObj = {'id':result["url"].id(),"ttl":curl.ttl}
        result['url'] = curlObj
        
        cusers = []
        for c in result["usr"]:
            cuser = c.get()
            cuserObj = { "id":c.id(),"nam":cuser.nam}
            cusers.append(cuserObj)
        result['usr'] = cusers
        result['key'] = self.key.id()
        
        return result 
 
 
 
class CcaUtils(object):
    
    def to_json(self):
        result = super(CcaUtils,self).to_dict()
        result['key'] = self.key.id()
        curl = result["url"].get()
        curlObj = {'id':result["url"].id(),"ttl":curl.ttl}
        result['url'] = curlObj
        
        cuser = result["usr"].get()
        result['usr'] = cuser.nam      
        
        return result
 
    
 
     

class CuserUtils(object):
    def to_j(self):
        result = super(CuserUtils,self).to_dict()
        result['key'] = self.key.id()
        
        cusers = []
        for c in result["ivt"]:
            cuser = c.get()
            cuserObj = { "id":c.id(),"nam":cuser.nam}
            cusers.append(cuserObj)
        result["ivt"] = cusers 

        del result["ivt"]

        cusers = []
        for c in result["fri"]:
            cuser = c.get()
            cuserObj = { "id":c.id(),"nam":cuser.nam}
            cusers.append(cuserObj)
        result["fri"] = cusers         
        
        return result 
    

class Cuser(CuserUtils,ndb.Model):
    
    nam = ndb.StringProperty()
    mal = ndb.StringProperty(indexed=True)
    fri = ndb.KeyProperty(indexed=True,repeated=True)
    ivt = ndb.KeyProperty(indexed=True,repeated=True)
    css = ndb.JsonProperty(
                           default={
                                    "font-family":"Arial",
                                    "color":"#1100ff",
                                    "font-opacity":"100",
                                    "font-size":"14pt",
                                    "font-style":"normal",
                                    "font-opacity":"100",   
                                    'font-weight': "400",
                                    'text-decoration':"none",
                                    'letter-spacing':"0px",
                                    'word-spacing':'0px',
                                    'line-height':'1em',
                                    'text-align':'left',
                                    'text-shadow-positonx':'1px',
                                    'text-shadow-positony':'2px',
                                    'text-shadow-blur':'3px',
                                    'text-shadow':'#ff00ff',
                                    'xt-shadow-flg':1,
                                    'top':'0',
                                    'left':'0',
                                    'depth':1,
                                    'height':"100px",
                                    "width":"180px",
                                    'background-color':'#bbaacc',
                                    'background-opacity':'50',
                                    'padding':'5px',
                                    'border-radius':'20px',
                                    'box-shadow':'#000000',
                                    'box-shadow-flg':'1',
                                    'box-shadow-positonx':"10px",
                                    'box-shadow-positony':"10px",
                                    'box-shadow-blur':"3px",
                                    'border-style':'solid',
                                    'border-color':'#7e28bd',
                                    'border-opacity':'100',
                                    'border-width':'6px',
                                    'bheight':'0',
                                    'bwidth':'0'
                                    }
                           )


class Curl(ndb.Model):
    ttl = ndb.StringProperty()
    url = ndb.StringProperty()     
        
class Ccn(CcnUtils,ndb.Model):
    url = ndb.KeyProperty(Curl,indexed=True)
    usr = ndb.KeyProperty(Cuser,indexed=True,repeated=True)
    txt = ndb.StringProperty(indexed=True)
    dat = ndb.DateTimeProperty(indexed=True,auto_now_add=True)
    css = ndb.JsonProperty()
    tag = ndb.StringProperty(repeated=True)
    pub = ndb.StringProperty(default="r")
    wrk = ndb.StringProperty()
    
    
class Cca(CcaUtils,ndb.Model):
    url = ndb.KeyProperty(Curl,indexed=True)
    usr = ndb.KeyProperty(Cuser,indexed=True)
    dat = ndb.DateTimeProperty(indexed=True,auto_now_add=True)

       
    
    
