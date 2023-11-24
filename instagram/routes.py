import os

from flask import render_template, redirect, url_for, jsonify, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename

from instagram.models import load_user, User, Posts, Like, Comment
from instagram import app, database
from instagram.forms import FormLogin, FormCreateNewAccount, FormCreateNewPost, CommentForm
from instagram import bcrypt
from instagram import login_manager


@app.route('/', methods=['POST', 'GET'])
def homepage():
    formLogin = FormLogin()

    return render_template("login.html", form=formLogin)

@app.route('/login', methods=['POST'])
def login():
    formLogin = FormLogin()

    if formLogin.validate_on_submit():
        userToLogin = User.query.filter_by(email=formLogin.email.data).first()
        if userToLogin and bcrypt.check_password_hash(userToLogin.password, formLogin.password.data):
            login_user(userToLogin)
            return redirect(url_for('profile', user_id=userToLogin.id))

    return render_template('login.html', form=formLogin, error='Credenciais inválidas.')


@app.route('/profile/<user_id>', methods=['POST', 'GET'])
@login_required
def profile(user_id):
    if int(user_id) == int(current_user.id):
        _formNewPost = FormCreateNewPost()
        _formNewComment = CommentForm()

        if _formNewPost.validate_on_submit():
            _post_text = _formNewPost.text.data

            _post_img = _formNewPost.photo.data
            _img_name = secure_filename(_post_img.filename)
            path = os.path.abspath(os.path.dirname(__file__))
            path2 = app.config['UPLOAD_FOLDER']
            _final_path = f'{path}/{path2}/{_img_name}'

            _post_img.save(_final_path)

            newPost = Posts(post_text=_post_text,
                           post_img=_img_name,
                           user_id=int(current_user.id)
                           )
            database.session.add(newPost)
            database.session.commit()

        posts = Posts.query.all()

        return render_template("profile.html", user=current_user, form=_formNewPost, posts=posts, formComment=_formNewComment)
    else:
        _user = User.query.get(int(user_id))
        return render_template("profile.html", user=_user, form=False)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/new', methods=['POST', 'GET'])
def create_account():
    formCreateAccount = FormCreateNewAccount()

    if formCreateAccount.validate_on_submit():
        password = formCreateAccount.password.data
        password_cr = bcrypt.generate_password_hash(password)
        newUser = User(username=formCreateAccount.username.data,
                       email=formCreateAccount.email.data,
                       password=password_cr)

        database.session.add(newUser)
        database.session.commit()
        login_user(newUser, remember=True)
        return redirect(url_for('profile', user_id=newUser.id))

    return render_template("enroll.html", form=formCreateAccount)

@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like(post_id):
    post = Posts.query.get(post_id)

    if post:
        if current_user.id not in [like.user_id for like in post.likes]:
            like = Like(user_id=current_user.id, post_id=post.id)
            database.session.add(like)
            database.session.commit()

            return jsonify({'success': True, 'likes': len(post.likes)})
        else:
            return jsonify({'success': False, 'error': 'You already liked this'}), 400
    else:
        return jsonify({'success': False, 'error': 'Post not found'}), 404

@app.route('/get_comments/<int:post_id>')
def get_comments(post_id):
    post = Posts.query.get_or_404(post_id)
    comments = post.comments

    return render_template('parcialcmm.html', comments=comments)

@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    post = Posts.query.get_or_404(post_id)
    comment_text = request.form.get('comment_text')
    if comment_text:
        new_comment = Comment(text=comment_text)
        post.comments.append(new_comment)
        database.session.commit()

    comments = post.comments
    return render_template('parcialcmm.html', comments=comments)