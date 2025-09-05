from flask import Flask

app = Flask(__name__)

# Página inicial simples só pra testar
@app.route('/')
def index():
    return "<h1>Flask rodando! 🚀</h1><p>Edite o app.py para começar seu cliente SUAP.</p>"

if __name__ == "__main__":
    app.run(debug=True)
