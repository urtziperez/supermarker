from django.shortcuts import render
# Create your views here.
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from couchdb import Server
from models import User
from django.template.response import SimpleTemplateResponse
from django.template.context import *
from django.core.exceptions import ValidationError
from couchdb import ResourceNotFound
from django.utils.datastructures import MultiValueDictKeyError
#from couchdb.client import ResourceNotFound



SERVER = Server('https://urtzi:urtziperez1992@urtzi.cloudant.com/')

if (len(SERVER) == 0):
    SERVER.create('supermarker')
	
	

def index(request):
    db = SERVER['supermarker']
    return render_to_response('index.html',{'rows':db})



def login(request):
	

	if request.method == 'POST':
		
		
		 db = SERVER['supermarker']
		 name = request.POST['name']
		 password = request.POST['password']
		 for docid in db:
			if db[docid]['name'] == name:
				if db[docid]['password'] == password:
					 return HttpResponseRedirect(u"/session/%s/" % name)
		 return SimpleTemplateResponse(
							template = 'nosession.html',
							content_type = "text/html"
							#context=RequestContext(request))
						)	
					
	else:
	
		return SimpleTemplateResponse(
            template = 'login.html',
            content_type = "text/html"
			)
			
def register(request):

	if request.method == 'POST':
		db=SERVER['supermarker']
		name = request.POST['name']
		password = request.POST['password']
		email = request.POST['email']
		if name or password or email :
			for docid in db:
				if docid == name:
					return SimpleTemplateResponse(
							template = 'nosession.html',
							content_type = "text/html"
							#context=RequestContext(request))
						)
			db[name]= {'name':name,'password':password,'email':email, 'list':name}
			return SimpleTemplateResponse(
				template = 'session.html',
				content_type = "text/html"
				#context=RequestContext(request))
				)
		else:
			return SimpleTemplateResponse(
							template = 'nosession.html',
							content_type = "text/html"
							#context=RequestContext(request))
						)
	elif request.method == 'GET':
		return SimpleTemplateResponse(
							template = 'register.html',
							content_type = "text/html"
							#context=RequestContext(request))
						)

global user_session						

def session(request,id):
	print "Entra a session"
	if request.method == 'POST':
		db=SERVER['products']
		buscar = request.POST['buscar']
		param=[]
		docs=[]
		pos=0
		for docid in db:
			if buscar in docid:
				doc=db[docid]
				doc.update({ u'user' : id })
				docs.append(doc)
				pos=pos+1
		global user_session
		param.append(docs)
		param.append(user_session)
		return render_to_response('session.html',{'param':param})	
	global user_session
	db=SERVER['supermarker']
	param=[]
	print id
	doc = db[id]
	user_session=doc
	param.append(None)
	param.append(user_session)
	return render_to_response('session.html',{'param':param})
'''	
def list(request):
	if request.method == 'GET':
		dblist=SERVER['lists']
		list=dblist[user_session.list]
		return HttpResponseRedirect(u"/session/%s/%s/" % user_session % list.name)
'''

def lista(request,iduser,idlist):
	print "Entra a lista"
	if request.method == 'GET':
		param=[]
		keyprods=[]
		prods=[]
		dbproducts=SERVER['products']
		dblist=SERVER['lists']
		dbuser=SERVER['supermarker']
		list=dblist[idlist]
		user=dbuser[iduser]
		for key in list:
			if key != '_id' and key != '_rev':
				keyprods.append(key)
		for key in keyprods:
			prod=dbproducts[key]
			cantidad=list[key]
			prod.update({ u'cantidad' : cantidad })
			prods.append(prod)
		param.append(prods)
		param.append(user)
		print prods
		return render_to_response('lista.html',{'param':param})
	elif request.method == 'POST':
		param=[]
		dbuser=SERVER['supermarker']
		dblist=SERVER['lists']
		list=dblist[idlist]
		checked = []
		cont=0
		for i in list:
			if i != '_id' and i != '_rev':
				cont=cont+1
		print 'contbefore:'
		print cont
		templist=list
		post = request.POST
		for i in post:
			del templist[i]
		dblist[idlist]=templist
		user=dbuser[iduser]
		param.append(None)
		param.append(user)
		return render_to_response('session.html',{'param':param})
		'''
		print 'Posted:'
		print post
		posted=[]
		for i in post:
			posted.append(i)
		del templist['_id']
		del templist['_rev']
		cont = 0
		removelist=[]
		for i in templist:
			print 'templistvar'
			print i
			print posted[cont]
			print cont+1
			if cont+1 == posted[cont]:
				print 'pasa'
				removelist.append(i)
			cont=cont+1
		newlist=dblist[idlist]
		print 'removelist'
		print removelist
		for i in removelist:
			print 'i'
			print i
			del newlist[i]
		print 'newlist'
		print newlist
		dblist[idlist]=newlist
		user=dbuser[iduser]
		param.append(None)
		param.append(user)
		return render_to_response('session.html',{'param':param})
		'''
		'''
		for i in range(cont):
			try:
				print 'Post:'
				print i+1
				var = request.POST[i+1]
				print 'Posted:'
				print var
				checked.append(var)
			except MultiValueDictKeyError:
				print 'no pasa nada'
				checked.append(0)
		print 'checked:'
		print checked
		cont=1
		print 'list count:'
		print list.items()
		removelist=[]
		for i in list:
			if cont == checked[cont]:
				removelist.append(i)
			cont=cont+1
		for i in removelist:
			del list[i]
			print 'listafinal'
			print list
		dblist[idlist]=list
		user=dbuser[iduser]
		param.append(None)
		param.append(user)
		return render_to_response('session.html',{'param':param})
		'''

def addproduct(request, iduser, idprod):
	dbproducts=SERVER['products']
	dblist=SERVER['lists']
	try:
		list=dblist[iduser]
	except ResourceNotFound:
		dblist[iduser]={ idprod : 1 }
		return HttpResponseRedirect(u"/session/%s/" % iduser)
	product=dbproducts[idprod]
	enc=0
	for key,value in list.items():
		if key == idprod:
			list.update({ idprod : value+1 })
			print 'List:'
			print list
			enc = enc+1
	if enc == 0:
		list.update({ idprod : 1 })
	dblist[iduser]=list
	return HttpResponseRedirect(u"/session/%s/" % iduser)
	
	