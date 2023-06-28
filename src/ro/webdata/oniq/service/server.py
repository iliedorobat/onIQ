import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

from ro.webdata.oniq.service.handlers import entities_handler, matcher_handler, resource_type_handler
from ro.webdata.oniq.service.query_const import PATHS


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()

        output = {}
        parsed = urlparse(self.path)

        if parsed.path == "/" + PATHS.MATCHER:
            # TODO: remove: replaced by SpotlightService
            output = matcher_handler(parsed)

        elif parsed.path == "/" + PATHS.RESOURCE_TYPE:
            output = resource_type_handler(parsed)

        elif parsed.path == "/" + PATHS.ENTITIES:
            output = entities_handler(parsed)

        self.wfile.write(json.dumps(output).encode())


def main():
    PORT = 8200
    server = HTTPServer(("", PORT), Handler)
    print("Server running on port %s" % PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()
