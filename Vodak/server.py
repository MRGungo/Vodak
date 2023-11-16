from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


registrace = []

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

    if not je_plavec:
        return 'Nemůžete se zaregistrovat, pokud neumíte plavat.', 400

    if not (2 <= len(nick) <= 20 and nick.isalnum()):
        return 'Neplatný nick. Povoleny jsou pouze znaky anglické abecedy a číslice (2-20 znaků).', 400

    if kanoe_kamarad and not (2 <= len(kanoe_kamarad) <= 20 and kanoe_kamarad.isalnum()):
        return 'Neplatný kamarád. Povoleny jsou pouze znaky anglické abecedy a číslice (2-20 znaků).', 400

    if any(reg['nick'] == nick for reg in registrace):
        return 'Nick je již obsazen.', 400

    registrace.append({'nick': nick, 'je_plavec': je_plavec, 'kanoe_kamarad': kanoe_kamarad})
    return 'Registrace úspěšně uložena.', 200

if __name__ == '__main__':
    app.run(debug=True)
