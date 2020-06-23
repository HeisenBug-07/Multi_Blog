import os
import secrets
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from myproject.users.form import LoginForm, RegisterForm, UpdateAccount
from myproject.modles import db, User, Post
from flask_login import current_user, login_required, logout_user, login_user
from sqlalchemy import desc

user_blueprint = Blueprint('user', __name__, template_folder='templates/users')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                flash('login successful', 'success')

                next = request.args.get('next')
                if next == None or not next[0] == '/':
                    next = url_for('user.account')

                return redirect(next)

            else:
                flash('login failed, wrong password', 'danger')

        else:
            flash('login failed, email not registered', 'danger')

    return render_template('login.html', form=form)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('registration successful', 'success')
        return redirect(url_for('user.login'))

    return render_template('register.html', form=form)


def add_picture(pic_upload):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    file_name = secrets.token_hex(8)
    store_filename = file_name + '.' + ext_type
    file_path = os.path.join(current_app.root_path, 'static\images', store_filename)
    pic_upload.save(file_path)
    return store_filename


@user_blueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    user = User.query.filter_by(username=current_user.username).first()
    post = Post.query.filter_by(user=user).order_by(desc(Post.date)).all()
    if form.validate_on_submit():
        if form.profile_image.data:
            profile_image = add_picture(form.profile_image.data)
            current_user.profile_image = profile_image

        current_user.email = form.email.data
        db.session.commit()
        flash('account updated', 'success')
        return redirect(url_for('user.account'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.profile_image.data = current_user.profile_image

    return render_template('account.html', form=form, post=post)


@user_blueprint.route('/view_account/<string:sno>')
def view_account(sno):
    user = User.query.filter_by(id=sno).first()
    post = Post.query.filter_by(user_id=sno).order_by(desc(Post.date)).all()
    return render_template('view_account.html', user=user, post=post)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logged outtt !', 'danger')
    return redirect(url_for('user.login'))
