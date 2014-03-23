import cStringIO
from handlers import unexpected as handle_unexpected
import pycurl
import requests
import urllib

def request(method, url, params, handlers, **kwargs):

	curl    = pycurl.Curl()
	body_io = cStringIO.StringIO()

	if method == 'post':
		curl.setopt(pycurl.POST, 1)
		curl.setopt(pycurl.POSTFIELDS, urllib.urlencode(params)) 
	else:
		url = '{0}?{1}'.format(url, urllib.urlencode(params))

	curl.setopt(pycurl.URL, url)
	curl.setopt(pycurl.WRITEFUNCTION, body_io.write)
	
	curl.perform()

	response = {
		'http_code': curl.getinfo(pycurl.HTTP_CODE),
		'body'     : body_io.getvalue()
	}

	curl.close()

	if response['http_code'] in handlers:
		return handlers[response['http_code']](response, **kwargs)
	else:
		handle_unexpected(response, **kwargs)


def download_file(url, params, handlers, **kwargs):

	curl = pycurl.Curl()
 	url  = '{0}?{1}'.format(url, urllib.urlencode(params))
	file = open(kwargs['file_name'], 'wb')

	curl.setopt(pycurl.URL, url)
	curl.setopt(pycurl.WRITEDATA, file)
	
	curl.perform()

	response = {
		'http_code': curl.getinfo(pycurl.HTTP_CODE)
	}

	curl.close()
	file.close()

	if response['http_code'] in handlers:
		return handlers[response['http_code']](response, **kwargs)
	else:
		handle_unexpected(response, **kwargs)


def upload_file(url, params, handlers, **kwargs):

	curl    = pycurl.Curl()
	body_io = cStringIO.StringIO()
	_params = []
	for key, value in params.iteritems():
		_params.append((key, value))

	curl.setopt(pycurl.POST, 1)
	curl.setopt(pycurl.HTTPPOST, _params)
	curl.setopt(pycurl.URL, url)
	curl.setopt(pycurl.WRITEFUNCTION, body_io.write)
	
	curl.perform()

	response = {
		'http_code': curl.getinfo(pycurl.HTTP_CODE),
		'body'     : body_io.getvalue()
	}

	curl.close()

	if response['http_code'] in handlers:
		return handlers[response['http_code']](response, **kwargs)
	else:
		handle_unexpected(response, **kwargs)