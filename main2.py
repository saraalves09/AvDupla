from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    texto = 'OUTRA - BONITO'
    return render_template('home_old.html', pernalonga=texto)


@app.route('/profile/<user>')
def profile(user):
    # texto = 'JOSÉ'
    return render_template('profile_old.html', patolino=user)


if __name__ == '__main__':
    app.run(debug=True)
