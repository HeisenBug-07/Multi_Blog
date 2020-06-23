from flask import Blueprint, render_template, redirect, url_for, flash
from myproject.core.form import ContactUs
from myproject.modles import db, Contact


core_blueprint = Blueprint('core', __name__)


@core_blueprint.route('/about', methods=['GET', 'POST'])
def about():
    form = ContactUs()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data, email=form.email.data, feedback=form.feedback.data)
        db.session.add(contact)
        db.session.commit()
        flash('send', 'success')
        return redirect(url_for('core.about'))
    return render_template('about.html', form=form)


