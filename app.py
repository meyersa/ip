from flask import Flask, request, jsonify, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Apply ProxyFix to handle the X-Forwarded-For header
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

@app.get("/ip")
def get_ip():
    print(f'Returned IP {request.remote_addr}')
    
    return request.remote_addr

@app.get("/json")
def get_json(): 
    print(f'Returned IP {request.remote_addr}')
    return jsonify({"ip": request.remote_addr})

@app.get("/")
def get_home(): 
    print(f'Returned IP page for {request.remote_addr}')
    return render_template("index.html", ip=request.remote_addr)

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000)
