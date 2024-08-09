from app import app
from flask import render_template, request, redirect, url_for, flash

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    # Lógica de autenticação
    if email == 'test@example.com' and senha == 'password':  # Exemplo de condição
        flash('Login bem-sucedido!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Email ou senha inválidos.', 'danger')
        return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    # Lógica de registro
    flash('Cadastro bem-sucedido!', 'success')
    return redirect(url_for('index'))