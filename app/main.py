# coding:UTF-8

import os
import urllib
import logging
import json
import string
import random

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.ndb import query
from google.appengine.api import memcache

import jinja2 
import webapp2
from ccn import *
import datetime
from jinja2 import Environment, FileSystemLoader
debugStr = "http://localhost:11080"
debugStr = "http://custanets.appspot.com"


def timeJST (value):
    return (value + datetime.timedelta(hours=9)).strftime('%m/%d %H:%M:%S').decode('utf-8')

def tag2Name (value):
    custanet_genre = { 
        '0010':'PC関連', 
        '0020':'インターネット関連' ,
        '0030':'ホームページ制作' ,
        '0040':'ブログ' ,
        '0050':'素材' ,
        '0060':'懸賞・プレゼント' ,
        '0070':'レストラン・料理' ,
        '0080':'ファッション' ,
        '0090':'健康・ダイエット' ,
        '0100':'文学・芸術' ,
        '0110':'音楽・映画' ,
        '0120':'アイドル・芸能' ,
        '0130':'アニメ・コミック' ,
        '0140':'ゲーム' ,
        '0150':'占い' ,
        '0160':'スポーツ' ,
        '0170':'アウトドア' ,
        '0180':'車・バイク' ,
        '0190':'ペット・動物' ,
        '0200':'旅行' ,
        '0210':'ビジネス・仕事' ,
        '0220':'ショッピング' ,
        '0230':'出会い' ,
        '0240':'チャット・掲示板'
    }
    
    if value and custanet_genre[value]:
        tagName = custanet_genre[value].decode('utf-8')
    else:
        tagName = ""
    return tagName

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
JINJA_ENVIRONMENT.filters['timeJST'] = timeJST
JINJA_ENVIRONMENT.filters['tag2Name'] = tag2Name

def isCuser(user):
    mail = user.user_id()
    cuser = memcache.get(mail)  # @UndefinedVariable
    if cuser is None:
        cuser = Cuser.get_by_id(user.user_id())
        memcache.add(mail,cuser)  # @UndefinedVariable
    return cuser

def isCurl(url,title):
    curl = memcache.get(url)  # @UndefinedVariable
    if curl is None:
        curl = Curl.get_by_id(url)
        if curl is None:
            curl = Curl(id = url,ttl = title)
            curl.put()
        memcache.add(url,curl)  # @UndefinedVariable
    return curl


from webapp2_extras import sessions
class BaseHandler(webapp2.RequestHandler):              # taken from the webapp2 extrta session example
    def dispatch(self):                                 # override dispatch
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)       # dispatch the main handler
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
    
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}        
        
class MainHandler(BaseHandler):
    def get(self):
        self.response.headers.add_header(
                "P3P",
                "CP=CAO PSA OUR"
            )
        
        user = users.get_current_user()
     
        if user:
            cuser = isCuser(user)
            
            template_values = {
                               'debugStr': debugStr,
                               'login' : True,
                               'logouturl' : users.create_logout_url(self.request.uri)
                               }               
            
            if cuser == None:
                template_values['signin'] = False 
            else:
                template_values['signin'] = True
                template_values['name'] = cuser.nam
                
                ivts = []
                for c in cuser.ivt:
                    ivt = c.get()
                    ivtObj = { "id":c.id(),"nam":ivt.nam}
                    ivts.append(ivtObj)
                template_values['ivts'] = ivts

                fris = []
                for c in cuser.fri:
                    fri = c.get()
                    friObj = { "id":c.id(),"nam":fri.nam}
                    fris.append(friObj)
                template_values['fris'] = fris
                
                ccns = Ccn.query(Ccn.usr.IN([cuser.key])).order(-Ccn.dat).fetch()
                
                ccn_dics = []
            
                for ccn in ccns:
                    ccn_dic = ccn.to_json()
                    ccn_dics.append(ccn_dic)
                    
                template_values['ccns'] = ccn_dics
                template_values['cuserKey'] = cuser.key.id()
                

            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))

        else:

            template_values = {
                'loginurl' : users.create_login_url(self.request.uri),
                'login' : False ,
                'signin' : False
            }

            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))

class Signin(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        nickname = self.request.get('nickname')
        
        q = Cuser.query()
        q2 = q.filter( Cuser.nam == nickname)
        cusers = q2.fetch()
        
        if cusers == [] :
            cuser = Cuser(id=user.user_id(),mal=user.email(),nam = nickname)
            cuser.put()
            self.response.write(nickname)
        else:
            self.error(500)

class Request(webapp2.RequestHandler):
    def post(self):

        email = self.request.get('email')

        user = users.get_current_user()
        
        if user is None:
            self.error(500)
            return
        
        cuser = isCuser(user)

        q = Cuser.query()
        q2 = q.filter( Cuser.mal == email)
        friend = q2.fetch(1)[0]
        
        if friend:
            fi = friend.ivt
            fi.append(cuser.key)
            friend.ivt = set(fi)
            friend.put();
            self.response.write("t")
        else:
            self.response.write("f")
 
class Invite(webapp2.RequestHandler):
    def post(self):
        
        fids = self.request.get_all('fid')

        user = users.get_current_user()
        
        if user is None:
            self.error(500)
            return
        
        cuser = isCuser(user)
        cf = cuser.fri
        ci = cuser.ivt
        
        cusers=[]
        for f in fids:
            fuser = Cuser.get_by_id(f)
            if fuser:
                ff = fuser.fri
                ff.append(cuser.key)
                fuser.fri = set(ff)
                cusers.append(fuser)
                ci.remove(fuser.key)
                cf.append(fuser.key)
                cusers.append(fuser)
        
        cuser.fri = set(cf)
        cuser.ivt = set(ci)
        cusers.append(cuser)

        ndb.put_multi(cusers)
        
        ret = []
        for c in set(cf):
            u = c.get()
            ret.append( {"id":c.id(),"nam":u.nam } )
        
        logging.info(ret)
        
        self.response.write(json.dumps(ret))

class Delete(webapp2.RequestHandler):
    def post(self):

        fids = self.request.get_all('fid')

        user = users.get_current_user()
        
        if user is None:
            self.error(500)
            return
    
        cuser = isCuser(user)
        cf = cuser.fri
        
        cusers = []
        for f in fids:
            fkey = ndb.Key("Cuser",f)
            cf.remove(fkey)
            fuser = fkey.get() 
            ff = fuser.fri
            ff.remove(cuser.key)
            fuser.fri = set(ff)
            cusers.append(fuser)
            
        cuser.fri = set(cf)
        cusers.append(cuser)
        
        ndb.put_multi(cusers)
        
        ret = []
        for c in set(cf):
            u = c.get()
            ret.append( {"id":c.id(),"nam":u.nam } )
        
        self.response.write(json.dumps(ret))
        
        
class DeleteCn(webapp2.RequestHandler):
    def post(self):

        cids = self.request.get_all('cid')

        user = users.get_current_user()
        
        if user is None:
            self.error(500)
            return
    
        cuser = isCuser(user)

        ckeys = []
        for c in cids:
            ckey = ndb.Key("Ccn",c)
            ccn = Ccn.get_by_id(int(c))
            ckeys.append(ccn.key);
            
        self.response.write(cids)    
        
        
        
class Login(webapp2.RequestHandler):
    def get(self):

        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        self.response.headers['Content-Type'] = 'application/javascript;charset=UTF-8'   
        self.response.headers.add_header(
                "P3P",
                "CP=CAO PSA OUR"
            )
        
        url = self.request.get('url')
        
        if url == "":
            self.response.write("alert('no url');")
            return

        chars = string.ascii_letters + string.digits + '_'
        pw = "".join([ random.choice(chars) for i in range(16) ])
                  
        ua = self.request.environ["HTTP_USER_AGENT"]
            
        if('MSIE' in ua):
        #if(True):
                str = "if(typeof CUSTANETed =='undefined'){\r\n"
                str += 'var cuser=' + json.dumps(cuser.to_j()) + ';\r\n'
                str += "var l2 = document.createElement('link');\r\n"
                str += "l2.setAttribute('rel', 'stylesheet');l2.setAttribute('type', 'text/css');\r\n"
                str += "l2.setAttribute('href', '" + debugStr +  "/styles/custanet.min.css');\r\n"
                str += "document.getElementsByTagName('head')[0].appendChild(l2);\r\n"
                str += "var element = document.createElement('div');\r\n"
                str += "element.id = 'custanet-result';\r\n"
                str += "var objBody = document.getElementsByTagName('body').item(0);\r\n"
                str += "objBody.appendChild(element);\r\n"
                str += "var pw='" + pw + "';\r\n"
                str += "var view = document.getElementById('custanet-result');\r\n"
                
                f = open('html.min.txt')
                lines2 = f.readlines()
                f.close()
                
                allline = ""
                for line in lines2:
                    allline += line.rstrip()
                str += "var CUSTANETed=1;view.innerHTML ='" + allline + "';\r\n"
                str += 'var ccns="";\r\n'
                str += "$('#custanet_welcome_iframe').attr('src','" + debugStr + "/loginIE.html');\r\n"
                f = open('js.min.txt')
                lines2 = f.readlines()
                f.close()           
                
                allline = ""
                
                for line in lines2:
                    allline += line
                str +=  allline
    
                str += "\r\n};\r\n"
                self.response.write(str)            
                return
      
            
        user = users.get_current_user()
        
        if user is None:
            str = """
var custanetLoading = document.getElementById('custanet-loading');
custanetLoading.innerHTML="";
var custanetA = document.createElement('a');
custanetA.appendChild(document.createTextNode('Please login Custanet.'));
"""
            str += "custanetA.href='" + debugStr + "';custanetA.target = 'blank';custanetLoading.appendChild(custanetA);"
            #self.response.write("alert('no user');var custanetLoading=document.getElementById('custanet-loading');custanetLoading.parentNode.removeChild(custanetLoading);var a = document.createElement('a');a.appendChild(document.createTextNode('Please login Custanet'));a.href = 'http://custanets.appspot.com/';a.target = 'blank';document.getElementById('custanet-loading').appendChild(a);")
            #self.response.write("alert('no user');")
            self.response.write(str)
            return
        
        cuser = isCuser(user)
      
        if cuser == None:
            self.response.write("alert('no cuser');")
        else:
            memcache.add(pw,cuser)  # @UndefinedVariable
            
            curl = memcache.get(url)  # @UndefinedVariable
            
            if curl is None:
                curl = Curl.get_by_id(url)
                if curl is not None:
                    memcache.add(url,curl)  # @UndefinedVariable

            if curl is None:
                ccns=[]
            else:
                ccns = Ccn.query(Ccn.url == curl.key , Ccn.usr.IN([cuser.key]) ).order(-Ccn.dat).fetch()
              
            ccn_dics = []        
            for ccn in ccns:
                ccn_dic = ccn.to_j()
                ccn_dics.append(ccn_dic)
            
            
            #str = "(function(){\r\n"
            str = "if(typeof CUSTANETed =='undefined'){\r\n"
            str += 'var cuser=' + json.dumps(cuser.to_j()) + ';\r\n'
            str += "var l2 = document.createElement('link');\r\n"
            str += "l2.setAttribute('rel', 'stylesheet');l2.setAttribute('type', 'text/css');\r\n"
            str += "l2.setAttribute('href', '" + debugStr +  "/styles/custanet.min.css');\r\n"
            str += "document.getElementsByTagName('head')[0].appendChild(l2);\r\n"
            str += "var element = document.createElement('div');\r\n"
            str += "element.id = 'custanet-result';\r\n"
            str += "var objBody = document.getElementsByTagName('body').item(0);\r\n"
            str += "objBody.appendChild(element);\r\n"
            str += "var pw='" + pw + "';\r\n"
            str += "var view = document.getElementById('custanet-result');\r\n"
            
            f = open('html.min.txt')
            lines2 = f.readlines()
            f.close()
            
            allline = ""
            for line in lines2:
                allline += line.rstrip()
            str += "var CUSTANETed=1;view.innerHTML ='" + allline + "';\r\n"
            str += 'var ccns=' + json.dumps([p.to_j() for p in ccns ] ) + ';\r\n'
            
            f = open('js.txt')
            lines2 = f.readlines()
            f.close()           
            
            allline = ""
            
            for line in lines2:
                allline += line
            str +=  allline

            str += "\r\n};\r\n"
            self.response.write(str)

        
class Set(webapp2.RequestHandler):
    
    def post(self):

        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        self.response.headers['Content-Type'] = 'application/javascript;charset=UTF-8'        
    
        url = self.request.get('url')
        if url == "":
            self.response.write("NoUrl")
            return

        pw = self.request.get('pw')
        cuser = memcache.get(pw)  # @UndefinedVariable
        
        
        if cuser == None:
            self.response.write("NoUser1")
            return
        else:            
            title= self.request.get('title')
            curl = isCurl(url,title)
            cns = self.request.get_all('cns[]')
            
            tag = self.request.get('tag')
            #logging.info(tag)
            #tag = json.loads(tag)
            #logging.info(tag)
            #if len(tag) == 0:
            #    tag=[];
            #logging.info("jooj")
            
            ccns_keys=[]
            ccns = []
            
            for cn in cns:
                c = json.loads(cn)
                pubs = c["auth"]
                usrs = []
                usrs.append(cuser.key)
                for p in pubs:
                    if p != "r" and p !="u" and p !="t":
                        fuser = Cuser.get_by_id(p)
                        usrs.append(fuser.key)
                        pub = "f";
                    else: 
                        pub = p;  
                        
                txt = c["txt"] 
                txt = txt.replace('\r\n','<br>')
                txt = txt.replace('\n','<br>')
                txt = txt.replace('\r','<br>')                
                
                if "tag" in c:
                    tag = c["tag"] 
                    if len(tag) == 0:
                        tag=[];
                else :
                     tag=[];
                                    
                logging.info("jooj")
                logging.info(tag)
                                                             
                if "css" in c :
                    css = c["css"]
                    
                    if (len( str(c["key"]) )==10):
                        ccn = Ccn(url=curl.key,usr=usrs,txt=txt,css=css,pub=pub,tag=tag)
                        ccns.append(ccn)
                        ccns_keys.append(c["key"])      
                    else:
                        ccn = Ccn.get_by_id(int(c["key"])) 
                        if ccn and ccn.usr[0] == cuser.key:
                            logging.info( "jiijij")  
                            ccn.usr = usrs
                            ccn.pub = pub
                            ccn.txt = txt
                            ccn.css = css
                            ccn.tag = tag       
                            ccns.append(ccn)
                            ccns_keys.append(c["key"])
                            
                else:
                    ccn = Ccn(url=curl.key,usr=usrs,txt=txt,pub=pub,tag=tag)
                    ccns.append(ccn)
                    ccns_keys.append(c["key"])                           
                      
                            
            ndb.put_multi(ccns)
     
            reCcns = []
            for i in range(len(ccns)):
                a = ccns[i].to_j()
                a["wrk"] = ccns_keys[i]
                reCcns.append(a)
            
            #self.response.write( self.request.get("callback") + "(" +  json.dumps(reCcns) + ");"  )  
            self.response.write( json.dumps(reCcns)  )  
  
    
class CheckIE(webapp2.RequestHandler):
    def post(self):
        ukey = self.request.get('ukey')
        logging.info("123456789aaa")
        logging.info(ukey)
        
        logging.info(self.request.environ["HTTP_USER_AGENT"])
        
        self.response.write("") 
        
        
class LoginIE(webapp2.RequestHandler):
    def get(self):
        template_values = {}

        template = JINJA_ENVIRONMENT.get_template('loginIE.html')
        self.response.write(template.render(template_values))        
        
        
class Test(webapp2.RequestHandler):
    def get(self):
        self.response.write("aaa")         
                
        
        
        
            
app = webapp2.WSGIApplication([
    ('/', MainHandler),('/signin', Signin),('/login',Login),('/set',Set),('/loginIE.html',LoginIE),('/checkIE',CheckIE),('/request',Request),('/invite',Invite),('/delete',Delete),('/deleteCn',DeleteCn),('/test',Test)
], config=config,debug=True)
