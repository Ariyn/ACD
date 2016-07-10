from ACD.Api import api, endPointTo, filtering
import sys, json, mimetypes

class Folders:
	@staticmethod
	@endPointTo("nodes")
	@api
	def query(url, query):
		# print(query)
		return {
			"url":url,
			"query":query
		}

	@staticmethod
	@endPointTo("nodes")
	@filtering(kind = "FOLDER")
	@api
	def list(url, nextToken = None, filters = ""):
		query = {
			"filters":filters
		}

		if nextToken:
			query["startToken"] = nextToken
		# print(query)
		return {
			"url":url,
			"query":query
		}

	@staticmethod
	@endPointTo("nodes")
	@api
	def create(url, name, **kwargs):
		# parent=None, labels=None, properties=None, localID=None
		body = {
			"name":name,
			"kind":"FOLDER"
		}
		body.update(kwargs)
		return {
			"url":url,
			"body":body,
			"method":"POST"
		}

	@staticmethod
	@endPointTo("nodes")
	@api
	def get(url, id):
		url = url + "/"+ id
		return {
			"url":url
		}

	@staticmethod
	@endPointTo("nodes")
	@api
	def patch(url, id):
		url = url + "/"+ id
		return {
			"url":url,
			"method":"PATCH"
		}

class Files:
	@staticmethod
	@endPointTo("nodes","cdproxy")
	@api
	def download(url, id, download=True, **kwargs):
		# read content size from response header
		kwargs["download"] = download
		if "path" in kwargs:
			path = kwargs["path"]
			del(kwargs["path"])

		url = url+ "/%s/content"%id
		print(kwargs, url)
		return {
			"url":url,
			# "query":kwargs,
			"path":path
		}

	@staticmethod
	@endPointTo("nodes")
	@filtering(kind="FILE")
	@api
	def list(url, filters, **kwargs):
		kwargs["filters"] = filters

		return {
			"url":url,
			"query":kwargs
		}

	@staticmethod
	@endPointTo("nodes", "cdproxy")
	@api
	def upload(url, name, file=None, path=None, kind="FILE", **kwargs):
		kwargs["name"], kwargs["kind"] = name, kind
		if "deduplication" in kwargs:
			if kwargs["deduplication"]:
				url = url+"?suppress=deduplication"

			del(kwargs["deduplication"])
			# print(url)

		boundary = "----BOUNDARY_WORD_jeR45rtF5U3ZX9j"
		if file:
			fileName, fileData = name, file
		elif path:
			fileName, fileData = path.split("/")[-1], open(path,"rb").read()
		# print(len(fileData), json.dumps(kwargs))

		mime = mimetypes.guess_type(fileName)[0] or "application/octet-stream"
		print(mime)

		body = []
		body.append("--"+boundary)
		body.append('Content-Disposition: form-data; name="metadata"')
		body.append("")
		body.append(json.dumps(kwargs))
		body.append("--"+boundary)
		body.append('Content-Disposition: form-data; name="content"; filename="%s"'%fileName)
		body.append('Content-Type: %s'%mime)
		body.append("")
		body.append(fileData)
		body.append("--"+boundary)
		# body.append("")

		for i, v in enumerate(body):
			if type(v) == str:
				body[i] = v.encode("utf-8")
		body = b"\r\n".join(body)
		# print(body)

		header = {
			"Content-Type":"multipart/form-data; boundary=%s" % boundary,
		}
		return {
			"url":url,
			"header":header,
			"body":body,
			"method":"POST"
		}

	@staticmethod
	@endPointTo("nodes")
	@api
	def get(url, id, **kwargs):
		query = ("?"+urlencode(kwargs)) if kwargs else ""
		url = url+"/%s%s"%(id, query)

		return {
			"url":url
		}
	@staticmethod
	def tempLink():
		pass

	@staticmethod
	def overwrite():
		pass

	@staticmethod
	def patch():
		pass

class Children:
	@staticmethod
	def add():
		pass
	@staticmethod
	def move():
		pass
	@staticmethod
	def delete():
		pass
	@staticmethod
	def list():
		pass

class Properties:
	@staticmethod
	def add():
		pass
	@staticmethod
	def get():
		pass
	@staticmethod
	def delete():
		pass
	@staticmethod
	def list():
		pass

if __name__ == "__main__":
	# Files.upload(name="gnMCXzP.gif", file="./gnMCXzP.gif", parents=["cj5LbmKOSJiAzMq9NHGwGA"], deduplication=True)
	print(sys.version)
	# d = Files.get(id="p4gDm1-ORbKzJtmPiLppKQ")
	# sys.stdout.buffer.write(str(d).encode("utf-8"))
	# d = Files.download(id="TjBwjcj6QqyrFLtV14d33g", path="./sample.zip")
	# d = Files.list(parents=["cj5LbmKOSJiAzMq9NHGwGA"])
	# d = Folders.query(query = "filters=kind:FOLDER AND parents:1pg2kEOPQMy0s6UfszDARw")
	# d = Folders.list(parents=["sfq5OHXyRz-LEXavuFHClA"])
	# # print(d.keys())
	#
	# print(d["count"], d["nextToken"])
	# for i in d["data"]:
	# 	sys.stdout.buffer.write(str(i).encode("utf-8"))
	# 	print("")

# 이거 결국 space를 %20으로 인코딩 해주니 됨
# https://drive.amazonaws.com/drive/v1/nodes?filters=kind:FOLDER AND parents:1pg2kEOPQMy0s6UfszDARw
# https://drive.amazonaws.com/drive/v1/nodes?filters=parents:1pg2kEOPQMy0s6UfszDARw AND kind:FOLDER
	# print()
	# d = Folders.patch(id="1pg2kEOPQMy0s6UfszDARw")
	# sys.stdout.buffer.write(str(d).encode("utf-8"))
	# print("")
