"""
    Log details of HTTP errors for better diagnostics.

    If called, this will print::

        HTTP.CLIENT
        HTTP::GET ERROR: HTTP Error 404: Not Found

        URLLIB
        HTTP::GET ERROR for http://failure.exampe.com/: HTTP Error 404: Not Found
            RESPONSE BODY:
            <h1>404: Not Found</h1>

        REQUESTS
        HTTP::GET ERROR: 404 Client Error: Not Found for url: http://failure.exampe.com/
            RESPONSE BODY:
            <h1>404: Not Found</h1>
"""
import socket
import http.client
import urllib.request, urllib.error
from contextlib import contextmanager

CONN_ERRORS = (
    socket.gaierror,
    socket.herror,
    socket.timeout,
)
HTTP_ERRORS = CONN_ERRORS + (
    http.client.HTTPException,
    urllib.error.URLError,
    urllib.error.HTTPError,
)
MAX_ERROR_LINES = 15

try:
    import requests
    HTTP_ERRORS = HTTP_ERRORS + (requests.RequestException,)
except ImportError:
    requests = None


@contextmanager
def http_diagnostics(handler=print):
    """ Context manager that nicely reports any errors from HTTP calls.

        Args:
            handler: Logging callable that takes a message and returns ``None``,
                or an exception class to raise instead.
    """
    try:
        yield
    except HTTP_ERRORS as cause:
        import pprint

        response = getattr(cause, 'response', getattr(cause, 'file', None))
        request = getattr(response, 'request', getattr(cause, 'request', None))
        if 0:
            context = dict(exc_type=type(cause), exc_args=cause.args, exc_obj=vars(cause),
                messages=[str(x) for x in cause.args])
            if request: context['request'] = vars(request)
            if response: context['response'] = vars(response)
            pprint.pprint(context)

        url = getattr(cause, 'url', getattr(request, 'url', ''))
        method = getattr(request, 'method', getattr(response, '_method', ''))
        message = getattr(cause, 'reason', str(cause))
        try:
            data = pprint.pformat(response.json(), indent=4)
        except (AttributeError, TypeError, ValueError):
            try:
                data = response.content.decode('utf8')
            except (AttributeError, UnicodeDecodeError):
                try:
                    data = response.fp.read().decode('utf8')
                except (AttributeError, UnicodeDecodeError, IOError):
                    data = ''
        if data:
            data = data.splitlines()
            if len(data) > MAX_ERROR_LINES:
                data = data[:MAX_ERROR_LINES] + ['...']
            data = '\n    RESPONSE BODY:\n' + '\n'.join(['    ' + x for x in data])

        exc = handler("HTTP{}{} ERROR{}{}: {}{}".format(
            '::' if method else '', method,
            ' for ' if url else '', url,
            message, data))
        if exc:
            raise exc from cause


if __name__ == '__main__':
    bad_url = 'http://failure.exampe.com/'
    timeout = .05  # try .05

    print('HTTP.CLIENT')
    with http_diagnostics():
        conn = http.client.HTTPConnection(bad_url.split('/')[2], timeout=timeout)
        try:
            conn.request('GET', '/')
            response = conn.getresponse()
            if response.status >= 300:
                exc = http.client.HTTPException("HTTP Error {}: {}".format(response.status, response.reason))
                exc.response = response
                raise exc
        finally:
            conn.close()

    print('\nURLLIB')
    with http_diagnostics():
        urllib.request.urlopen(bad_url, timeout=timeout)

    if requests:
        print('\nREQUESTS')
        with http_diagnostics():
            response = requests.get(bad_url, timeout=timeout)
            response.raise_for_status()


