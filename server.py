from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)


registrace = []

prihlaseni_uzivatele = {}

@app.route('/')
def index():
    return render_template('index.html', ucastnici=registrace)

@app.route('/registrace', methods=['GET'])
def registrace_stranka():
    return render_template('registrace.html')

@app.route('/api/check-nickname', methods=['GET'])
def check_nickname():
    nick = request.args.get('nick')
    exists = any(reg['nick'] == nick for reg in registrace)
    return jsonify({'exists': exists})

@app.route('/registrace', methods=['POST'])
def zpracuj_registraci():
    nick = request.form['nick']
    je_plavec = bool(int(request.form['je_plavec']))
    kanoe_kamarad = request.form['kanoe_kamarad']

    # Validace na straně serveru
    if not je_plavec:
        return 'Nemůžete se zaregistrovat, pokud neumíte plavat.', 400

    if not (2 <= len(nick) <= 20 and nick.isalnum()):
        return 'Neplatný nick. Povoleny jsou pouze znaky anglické abecedy a číslice (2-20 znaků).', 400

    if kanoe_kamarad and not (2 <= len(kanoe_kamarad) <= 20 and kanoe_kamarad.isalnum()):
        return 'Neplatný kamarád. Povoleny jsou pouze znaky anglické abecedy a číslice (2-20 znaků).', 400

    # Kontrola duplicity nicku
    if any(reg['nick'] == nick for reg in registrace):
        return 'Nick je již obsazen.', 400

    # Uložení registrace
    registrace.append({'nick': nick, 'je_plavec': je_plavec, 'kanoe_kamarad': kanoe_kamarad})
    return 'Registrace úspěšně uložena.', 200

@app.route('/login', methods=['GET'])
def login_stranka():
    return render_template('login.html', current_user=None)

@app.route('/login', methods=['POST'])
def login():
    nick = request.form['nick']

    if any(reg['nick'] == nick for reg in registrace):
        # Přihlášení uživatele
        prihlaseni_uzivatele[nick] = True
        return redirect(url_for('login_stranka', current_user=nick))
    else:
        return 'Uživatel s tímto nickem neexistuje.', 400

@app.route('/logout')
def logout():
    nick = request.args.get('nick')

    if prihlaseni_uzivatele.get(nick):
        # Odhlášení uživatele
        prihlaseni_uzivatele.pop(nick, None)
        return redirect(url_for('login_stranka'))
    else:
        return 'Uživatel není přihlášen.', 400

if __name__ == '__main__':
    app.run(debug=True)

class User(UserMixin):
    def __init__(self, nick):
        self.nick = nick

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET'])
def login_stranka():
    return render_template('login.html', current_user=current_user.nick if current_user.is_authenticated else None)

@app.route('/login', methods=['POST'])
def login():
    nick = request.form['nick']

    if any(reg['nick'] == nick for reg in registrace):
        user = User(nick)
        login_user(user)
        return redirect(url_for('login_stranka'))
    else:
        return 'Uživatel s tímto nickem neexistuje.', 400

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_stranka'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', ucastnici=registrace, current_user=current_user.nick)

@app.route('/registrace', methods=['GET'])
def registrace_stranka():
    return render_template('registrace.html', current_user=current_user.nick)

@app.route('/api/check-nickname', methods=['GET'])
def check_nickname():
    nick = request.args.get('nick')
    exists = any(reg['nick'] == nick for reg in registrace)
    return jsonify({'exists': exists})

@app.route('/registrace', methods=['POST'])
def zpracuj_registraci():


    if __name__ == '__main__':
        app.run(debug=True)
