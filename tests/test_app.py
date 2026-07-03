import socket

import app as whoami_app


def fake_addrinfo():
    return [
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.2", 0)),
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.3", 0)),
    ]


def test_root_outputs_whoami_text_with_all_request_headers(monkeypatch):
    monkeypatch.setattr(whoami_app.socket, "gethostname", lambda: "test-host")
    monkeypatch.setattr(
        whoami_app.socket,
        "getaddrinfo",
        lambda hostname, port, type: fake_addrinfo(),
    )

    client = whoami_app.app.test_client()
    response = client.get(
        "/?debug=true",
        headers={
            "X-Forwarded-For": "203.0.113.10",
            "X-Request-Id": "abc-123",
            "X-Forwarded-Proto": "https",
        },
    )

    assert response.status_code == 200
    assert response.content_type == "text/plain; charset=utf-8"

    body = response.get_data(as_text=True)
    assert "Hostname: test-host\n" in body
    assert "IP: 10.0.0.2\n" in body
    assert "IP: 10.0.0.3\n" in body
    assert "RemoteAddr: 203.0.113.10\n" in body
    assert "GET /?debug=true HTTP/1.1\n" in body
    assert "Host: localhost\n" in body
    assert "X-Forwarded-For: 203.0.113.10\n" in body
    assert "X-Request-Id: abc-123\n" in body
    assert "X-Forwarded-Proto: https\n" in body


def test_ip_route_outputs_same_header_rich_text(monkeypatch):
    monkeypatch.setattr(whoami_app.socket, "gethostname", lambda: "test-host")
    monkeypatch.setattr(
        whoami_app.socket,
        "getaddrinfo",
        lambda hostname, port, type: fake_addrinfo(),
    )

    client = whoami_app.app.test_client()
    response = client.get("/ip", headers={"X-Custom-Header": "custom value"})

    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "GET /ip HTTP/1.1\n" in body
    assert "X-Custom-Header: custom value\n" in body


def test_json_outputs_headers_structurally(monkeypatch):
    monkeypatch.setattr(whoami_app.socket, "gethostname", lambda: "test-host")
    monkeypatch.setattr(
        whoami_app.socket,
        "getaddrinfo",
        lambda hostname, port, type: fake_addrinfo(),
    )

    client = whoami_app.app.test_client()
    response = client.get("/json", headers={"X-Request-Id": "abc-123"})

    assert response.status_code == 200
    assert response.json["hostname"] == "test-host"
    assert response.json["ips"] == ["10.0.0.2", "10.0.0.3"]
    assert response.json["path"] == "/json"
    assert response.json["headers"]["X-Request-Id"] == "abc-123"
