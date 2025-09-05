from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

oauth.register(
    name='suap',
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    api_base_url='https://suap.ifrn.edu.br/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://suap.ifrn.edu.br/o/token/',
    authorize_url='https://suap.ifrn.edu.br/o/authorize/',
    fetch_token=lambda: session.get('suap_token')
)


@app.route('/')
def index():
    return render_template('login.html')

# Login com SUAP
@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.suap.authorize_redirect(redirect_uri)

# Callback do SUAP
@app.route('/auth')
def auth():
    token = oauth.suap.authorize_access_token()
    session['suap_token'] = token

    # Buscar dados do usuário
    meus_dados = oauth.suap.get('v2/minhas-informacoes/meus-dados').json()
    session['user'] = meus_dados

    return redirect(url_for('user'))

# Página do usuário
@app.route('/user')
def user():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('user.html', user=session['user'])

# Página do boletim
@app.route('/boletim')
def boletim():
    if 'suap_token' not in session:
        return redirect(url_for('index'))

    ano = request.args.get("ano", "2024")  # ano padrão
    boletim_data = oauth.suap.get(f'v2/minhas-informacoes/boletins/{ano}').json()
    return render_template('boletim.html', boletim=boletim_data, ano=ano)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))