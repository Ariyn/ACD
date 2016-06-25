from urllib.request import Request, urlopen, HTTPRedirectHandler, build_opener, install_opener
from urllib.parse import urlencode
from urllib.error import URLError
import time, json
import sys

clientID = "amzn1.application-oa2-client.fe15a59719c340268fe49bc23ce17c9d"
clientSecret = "26995c543b5138220c04cc24765d9938ec750e15382dbb943e173d879261adbc"
redirectURL = "http://localhost"

authURL = "https://www.amazon.com/ap/oa"
refreshURL = "https://api.amazon.com/auth/o2/token"
endPoint = "https://drive.amazonaws.com/drive/v1/"
userToken = {"access_token":None, "token_type":None, "expires_in":None, "bear_time":None, "scope":None}

class WrongTokenError(BaseException):
	pass

def auth_codeGrant(scope=None, redirectURL = redirectURL, url = None, refresh=False, fromCT = False):
	data = {
		"client_id":clientID,
		"redirect_uri":redirectURL
	}
	header = {}

	if url or refresh:
		if url:
			urlList = [i.split("=") for i in url.replace(redirectURL+"/?", "").split("&")]
			newDict = {
				"grant_type":"authorization_code",
				"code":urlList[0][1]
			}
		elif refresh:
			print("refreshing")
			if not fromCT:
				checkToken(fromRT = True)
			# print(userToken["refresh_token"])
			newDict = {
				"grant_type":"refresh_token",
				"refresh_token":userToken["refresh_token"],
			}

		data["client_secret"] = clientSecret
		data.update(newDict)
		data=urlencode(data).encode("utf-8")
		newURL = refreshURL

		header = {
			"Content-Type":"application/x-www-form-urlencoded"
		}

		try:
			req = Request(newURL, headers = header, data = data)
			response = urlopen(req)
			jsonStr = response.read().decode("utf-8")

			# print(jsonStr)
			jsonData = json.loads(jsonStr)
			# print(jsonData, type(jsonData))

			makeToken(**jsonData)
			# print(response.info())
			# print(jsonData)
		except URLError as e:
			print(e.errno)
			print(dir(e), e.errno, e)
	else:
		data.update({
			"scope":"%20".join(scope).replace(":", "%3A"),
			"response_type":"code",
		})

		data = "&".join([i+"="+data[i] for i in data])
		newURL, data = authURL+"?"+data, None
		print(newURL)

def makeToken(access_token, token_type, expires_in, scope=None, refresh_token = None, bear_time=None):
	userToken["access_token"] = access_token.replace("%7C", "|")
	userToken["token_type"] = token_type
	userToken["expires_in"] = int(expires_in)
	userToken["scope"] = scope if scope else userToken["scope"]
	userToken["bear_time"] = time.time()
	userToken["refresh_token"] = refresh_token

	string = json.dumps(userToken)
	open("./token","w").write(string)

def checkToken(fromRT = False, recursive = 0):
	try:
		token = json.loads(open("./token","r").read())
		for i in userToken:
			if i not in userToken:
				raise WrongTokenError

		makeToken(**token)
	except:
		print("wrong json file")

	try:
		now = time.time()
		# print("here")
		if token["bear_time"] + int(token["expires_in"]) < now:
			print("Token expired. Need to refresh.")
			# print(token["bear_time"] + token["expires_in"], now)
			raise WrongTokenError
		retVal = True
	except:
		if not fromRT:
			auth_codeGrant(refresh=True, fromCT = True)
		retVal = False

	return retVal

# checkToken()
# auth_codeGrant(refresh=True)
# auth_codeGrant(["clouddrive:write", "clouddrive:read_other"])
# auth_codeGrant(url = "http://localhost/?code=ANAgBVfyRWdYcbqKhNcf&scope=clouddrive%3Awrite+clouddrive%3Aread_other")
