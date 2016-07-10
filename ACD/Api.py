# api decorator test
import json

from urllib.request import Request, urlopen, HTTPRedirectHandler, build_opener, install_opener
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError

from ACD.secret import *
from ACD.Auth import checkToken, userToken

version = "0.0.1"

url = "https://drive.amazonaws.com"
cdProxyUrl = "https://content-na.drive.amazonaws.com"

preHeader = {
	"Accept-Type":"gzip",
	"User-agent":"cdc-"+version+";python3;"
}

def endPointTo(*args, **kwargs):
	def _nodes(func):
		if 1 < len(args):
			proxy = args[1]
			_url = cdProxyUrl
		else:
			proxy = "drive"
			_url = url

		endPoint = "/%s/v1/%s"%(proxy, args[0])
		def __nodes(*args, **kwargs):
			kwargs["url"] = _url+endPoint
			return func(*args, **kwargs)
		return __nodes
	return _nodes

def filtering(**kwargs):
	def _filtering(func):
		filterList = ["isRoot", "name", "kind", "modifiedDate", "createdDate", "labels", "description", "parents", "status", "size", "contentType", "md5", "contentDate", "extension"]
		preFilter = kwargs

		def filteringCall(*args, **kwargs):
			newData = {i:kwargs[i] for i in kwargs if i in filterList}
			newData.update(preFilter)

			for i in newData:
				if i in kwargs:
					del(kwargs[i])

				if i == "parents":
					newData["parents"] = " OR ".join(["parents:"+ e for e in newData["parents"]])
				else:
					if type(newData[i]) == str:
						newData[i] = i+":"+newData[i]
					elif type(newData[i]) == bool:
						newData[i] = i+":"+str(newData[i]).lower()

			# kwargs["filters"] = " AND ".join([newData[i] for i in newData])
			kwargs["filters"] = " AND ".join([newData[i] for i in newData])

			return func(*args, **kwargs)

		return filteringCall
	return _filtering

def api(func):
	def apiCall(*args, **kwargs):
		"""
		api real caller

		"""
		checkToken()

		# print(args, kwargs)
		parms = func(*args, **kwargs)

		url = parms["url"]
		query = parms["query"] if "query" in parms else None
		header = parms["header"] if "header" in parms else None
		body = parms["body"] if "body" in parms else None
		method = parms["method"] if "method" in parms else None

		if not header:
			header = {}
		header.update(preHeader)
		header["Authorization"] = "Bearer "+userToken["access_token"]

		if query:
			if type(query) != str:
				query = "&".join([i+"="+str(query[i]) for i in query])
			url = url+"?"+query.replace(" ","%20")
			# print(url)
			body = None
		elif body:
			if type(body) == dict or type(body) == list:
				body = json.dumps(body)

			if type(body) != bytes:
				body = body.encode("utf-8")
			header["Content-Length"] = len(body)

		if not method:
			method = "GET"
		# 	method = (lambda: method)

		# print(url, header, body)
		try:
			req = Request(url, headers = header, data=body, method=method)
			print(req.method, req.full_url)
			response = urlopen(req)
			# print(response.info())
			if "path" in parms:
				open(parms["path"], "wb").write(response.read())
			else:
				d = json.loads(response.read().decode("utf-8"))
				if "nextToken" not in d:
					d["nextToken"] = None
				return d
		except HTTPError as e:
			print(e, e.read())
	return apiCall
