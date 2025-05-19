from peticiones import Endpoint

endpoint = Endpoint()

endpoint.login()

sessionId = endpoint.get_sessionId()

print(sessionId)


