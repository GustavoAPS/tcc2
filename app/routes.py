from app import app
from flask import render_template, request, redirect, url_for, flash

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']  

    # Teste de autentificação
    if email == 'test@example.com' and password == 'password':  
        flash('Login bem-sucedido!', 'success')
        print(f"Email: {email}")
        print(f"Senha: {password}")
        return redirect(url_for('index'))
    else:
        flash('Email ou senha inválidos.', 'warning')
        print(f"Email: {email}")
        print(f"Senha: {password}")
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        confirm_email = request.form.get('confirm_email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        anxiety = request.form.get('anxiety')
        competitiveness = request.form.get('competitiveness')

        genres = request.form.getlist('genres')
        activities = request.form.getlist('activities')
        motivations = request.form.getlist('motivations')

        # Validações
        if not (username and email and confirm_email and password and confirm_password):
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('register'))

        if email != confirm_email:
            flash('Os e-mails não coincidem!', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('register'))

        # Teste de depuração
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Anxiety: {anxiety}")
        print(f"Competitiveness: {competitiveness}")
        print(f"Genres: {', '.join(genres)}")
        print(f"Activities: {', '.join(activities)}")
        print(f"Motivations: {', '.join(motivations)}")

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

