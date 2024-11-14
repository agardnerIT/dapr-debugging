# dapr-debugging

```
dapr init

# Start consul to work around mDNS issue
docker run -d -p 8500:8500 -p 8600:8600/udp --name dtc-consul consul:1.15 agent -dev -client '0.0.0.0'

# Start the server
dapr run --app-id api --app-port 9000 --dapr-http-port 3500 --log-level debug -- fastapi run server.py --port 9000

# Start a second proxy + the client
# According to Mauricio, DAPR works on proxy <> proxy so let's try that
# client.py issues a GET request to localhost:3501
dapr run --app-id client --dapr-http-port 3501 --log-level debug -- python3 client.py
```

## Expected Flow + Result

1. client.py calls it's own local proxy on 3501
2. client proxy finds `api` and the `foo` endpoint and forwards the request
3. server proxy receives request and forwards to server.py
4. transaction makes it's way back, in reverse, through both proxies
5. We see a nice `200 OK`

## Actual Result

First, server indicates that it isn't using consul:
```
Initialized name resolution to mdns
```

Then client cannot find `app`:

```
DEBU[0001] no mDNS address found in cache, browsing network for app id api  app_id=client component="nr (mdns/v1)" instance=Adams-MacBook-Air.local scope=dapr.contrib type=log ver=1.14.4
DEBU[0001] Browsing for first mDNS address for app id api  app_id=client component="nr (mdns/v1)" instance=Adams-MacBook-Air.local scope=dapr.contrib type=log ver=1.14.4
DEBU[0002] mDNS browse for app id api timed out.         app_id=client component="nr (mdns/v1)" instance=Adams-MacBook-Air.local scope=dapr.contrib type=log ver=1.14.4
DEBU[0002] Browsing for first mDNS address for app id api timed out.  app_id=client component="nr (mdns/v1)" instance=Adams-MacBook-Air.local scope=dapr.contrib type=log ver=1.14.4
DEBU[0002] HTTP service invocation failed to complete with error: invokeError (statusCode='500') msg='{"errorCode":"ERR_DIRECT_INVOKE","message":"failed to invoke, id: api, err: couldn't find service: api"}'  app_id=client instance=Adams-MacBook-Air.local scope=dapr.runtime.http type=log ver=1.14.4
== APP == 500
== APP == {"errorCode":"ERR_DIRECT_INVOKE","message":"failed to invoke, id: api, err: couldn't find service: api"}
✅  Exited App successfully
ℹ️  
terminated signal received: shutting down
✅  Exited Dapr successfully
```

### dapr invoke attempt

Just in case it's something in my code, let's try `dapr invoke`:

```
% dapr invoke --app-id api --method foo --verb GET       
❌  error invoking app api: 500 Internal Server Error
```
