from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, Searchform
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Listing
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
        if current_user.is_authenticated:
            return redirect(url_for('admin'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid Username or Password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
        logout_user()
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(type=form.type.data, username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        return render_template('signup.html', title='Register', form=form)


@app.route('/foo')
@login_required
def foo():
        return "bar"

@app.route('/search', methods=['GET', 'POST'])
def search():
        form = Searchform()
        listing = [
            {'title': "Lorem Ipsum from Acme, Inc", 'desc': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi sodales facilisis eros sed varius. Etiam vitae justo eu leo fermentum pharetra.", 'body':"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi sodales facilisis eros sed varius. Etiam vitae justo eu leo fermentum pharetra. Maecenas venenatis lorem neque, eget pharetra purus tempus quis. Quisque odio dolor, imperdiet at urna quis, dignissim viverra urna. Nunc non lectus venenatis, malesuada massa vitae, dignissim elit. Pellentesque luctus rutrum diam a ullamcorper. Maecenas ornare lobortis orci non gravida. Etiam eu congue velit, sit amet dapibus neque. Mauris eu auctor mi. Vestibulum sit amet sem non justo laoreet iaculis et ac odio. Nam non diam ac libero rhoncus feugiat.", 'location':"Maryland", 'type':"pentest"},
            ]
        if form.validate_on_submit():
            return redirect(url_for('fsearch'))

        return  render_template('search.html', form=form, listing1=listing)

@app.route('/fsearch')
def fsearch():
        form = Searchform()
        return render_template('fsearch.html', form=form)
