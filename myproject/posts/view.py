import os
import secrets
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request, abort
from myproject.posts.form import AddPost, UpdatePost
from myproject.modles import db, Post
from flask_login import current_user, login_required

post_blueprint = Blueprint('post', __name__, template_folder='templates/posts')


def add_picture(pic_upload):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]  # contain the extension of file
    file_name = secrets.token_hex(8)  # contain a random generated filename without extension
    store_file = file_name + '.' + ext_type  # contain the new and complete filename
    file_path = os.path.join(current_app.root_path, 'static/images', store_file)
    pic_upload.save(file_path)
    return store_file


@post_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddPost()
    if form.validate_on_submit():
        post_image = add_picture(form.post_image.data)
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id,
                    post_image=post_image)

        db.session.add(post)
        db.session.commit()
        flash('Post Uploaded', 'success')
        return redirect(url_for('user.account'))
    return render_template('add.html', form=form)


@post_blueprint.route('/update/<string:sno>', methods=['GET', 'POST'])
@login_required
def update(sno):
    post = Post.query.filter_by(id=sno).first()
    form = UpdatePost()
    if post.user != current_user:
        abort(403)
    else:

        if form.validate_on_submit():
            if form.post_image.data:
                post_image = add_picture(form.post_image.data)
                post.post_image = post_image

            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()

            flash('post updated', 'success')
            return redirect(url_for('user.account'))

        elif request.method == 'GET':
            form.title.data = post.title
            form.post_image.data = post.post_image
            form.content.data = post.content
    return render_template('update.html', form=form, post=post)


@post_blueprint.route('/delete/<string:sno>')
@login_required
def delete(sno):
    post = Post.query.filter_by(id=sno).first()
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted', 'danger')
    return redirect(url_for('user.account'))


@post_blueprint.route('/read/<string:sno>')
def read(sno):
    post = Post.query.filter_by(id=sno).first()
    return render_template('read.html', post=post)
