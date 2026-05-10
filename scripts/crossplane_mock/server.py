"""Mock Crossplane API Server.

Simple HTTP server that simulates Crossplane API responses for local development.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class CrossplaneMockHandler(BaseHTTPRequestHandler):
    """HTTP request handler for mock Crossplane API."""

    # Mock data store
    resources = {
        "compute": {},
        "storage": {},
        "network": {},
    }

    def _set_headers(self, status=200):
        """Set response headers."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def _send_json(self, data, status=200):
        """Send JSON response."""
        self._set_headers(status)
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # Health check
        if path == "/health" or path == "/":
            self._send_json({
                "status": "healthy",
                "service": "crossplane-mock",
                "message": "Mock Crossplane API for local development",
            })
            return

        # List resources
        if path.startswith("/apis/"):
            parts = path.split("/")
            if len(parts) >= 4:
                group = parts[2]
                version = parts[3]
                resource_type = parts[4] if len(parts) > 4 else ""

                # Return mock resource list
                self._send_json({
                    "apiVersion": f"{group}/{version}",
                    "kind": f"{resource_type.capitalize()}List",
                    "items": [],
                })
                return

        # Get specific resource
        if path.startswith("/apis/"):
            parts = path.split("/")
            if len(parts) >= 6:
                # /apis/group/version/namespaces/ns/resource/type/name
                resource_name = parts[-1]
                self._send_json({
                    "apiVersion": "v1",
                    "kind": "MockResource",
                    "metadata": {
                        "name": resource_name,
                        "namespace": "default",
                    },
                    "spec": {},
                    "status": {"state": "available"},
                })
                return

        # Default response
        self._send_json({
            "error": "Not found",
            "path": path,
            "message": "Mock Crossplane API - endpoint not implemented",
        }, status=404)

    def do_POST(self):
        """Handle POST requests (create resources)."""
        parsed = urlparse(self.path)
        path = parsed.path

        # Create resource
        if path.startswith("/apis/"):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
                resource_name = data.get("metadata", {}).get("name", "unknown")

                self._send_json({
                    "apiVersion": "v1",
                    "kind": "MockResource",
                    "metadata": {
                        "name": resource_name,
                        "namespace": "default",
                        "uid": f"mock-{resource_name}",
                    },
                    "spec": data.get("spec", {}),
                    "status": {"state": "available"},
                }, status=201)
                return
            except json.JSONDecodeError:
                self._send_json({"error": "Invalid JSON"}, status=400)
                return

        # Default response
        self._send_json({
            "error": "Not found",
            "path": path,
            "message": "Mock Crossplane API - endpoint not implemented",
        }, status=404)

    def do_DELETE(self):
        """Handle DELETE requests (delete resources)."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith("/apis/"):
            parts = path.split("/")
            if len(parts) >= 6:
                resource_name = parts[-1]
                self._send_json({
                    "status": "success",
                    "message": f"Mock resource {resource_name} deleted",
                }, status=200)
                return

        self._send_json({
            "error": "Not found",
            "path": path,
        }, status=404)

    def log_message(self, format, *args):
        """Suppress log messages."""
        pass  # Suppress default logging


def run_server(port=8080):
    """Run the mock Crossplane API server."""
    server_address = ("", port)
    httpd = HTTPServer(server_address, CrossplaneMockHandler)
    print(f"Mock Crossplane API server running on port {port}")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
