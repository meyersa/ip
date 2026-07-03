import socket

from flask import Flask, Response, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Apply ProxyFix to handle the X-Forwarded-For header
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)


def get_local_ips():
    hostname = socket.gethostname()
    try:
        addresses = socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
    except socket.gaierror:
        return ["127.0.0.1"]

    ips = sorted({address[4][0] for address in addresses})
    return ips or ["127.0.0.1"]


def get_whoami():
    return {
        "hostname": socket.gethostname(),
        "ips": get_local_ips(),
        "remote_addr": request.remote_addr,
        "method": request.method,
        "path": request.full_path.rstrip("?"),
        "http_version": request.environ.get("SERVER_PROTOCOL", "HTTP/1.1"),
        "headers": dict(request.headers.items()),
    }


def render_whoami(whoami):
    lines = [f"Hostname: {whoami['hostname']}"]
    lines.extend(f"IP: {ip}" for ip in whoami["ips"])
    lines.append(f"RemoteAddr: {whoami['remote_addr']}")
    lines.append(
        f"{whoami['method']} {whoami['path']} {whoami['http_version']}"
    )
    lines.extend(f"{name}: {value}" for name, value in whoami["headers"].items())
    return "\n".join(lines) + "\n"


@app.get("/")
def get_home():
    whoami = get_whoami()
    print(f"Returned whoami response for {whoami['remote_addr']}")
    return Response(render_whoami(whoami), mimetype="text/plain")


@app.get("/ip")
def get_ip():
    whoami = get_whoami()
    print(f"Returned whoami response for {whoami['remote_addr']}")
    return Response(render_whoami(whoami), mimetype="text/plain")


@app.get("/json")
def get_json():
    whoami = get_whoami()
    print(f"Returned whoami JSON for {whoami['remote_addr']}")
    return jsonify(whoami)


if __name__ == "__main__":
    app.run("0.0.0.0", port=8000)
