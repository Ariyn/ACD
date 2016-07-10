from ACD.Api import api, endPointTo, filtering
import sys, json, mimetypes

@endPointTo("account/info")
@api
def info(url):
	return {
		"url":url
	}

@endPointTo("account/endpoint")
@api
def endpoint(url):
	return {
		"url":url
	}

@endPointTo("account/quota")
@api
def quota(url):
	return {
		"url":url
	}

@endPointTo("account/usage")
@api
def usage(url):
	return {
		"url":url
	}


if __name__ == "__main__":
	d = endpoint()
	print(d)

	d = quota()
	print(d)

	d = usage()
	print(d)
