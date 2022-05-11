from main import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from datetime import datetime
from main.forms import UserRegistration, LoginUser, NewAd, Search
from main.models import User, Ad
from flask_login import login_user, current_user, logout_user, login_required
from flask_paginate import Pagination, get_page_parameter
import secrets
import os
from PIL import Image

year = datetime.now().year


@app.route("/")
@app.route("/home")
def home():
    total = Ad()
    return render_template("home.html", year=year, title='Home', total=total)


@app.route("/about")
def about():
    return render_template("about.html", year=year, title='About Us')


@app.route("/contacts")
def contacts():
    return render_template("contacts.html", year=year, title='Contacts')


@app.context_processor
def layout():
    form = Search()
    return dict(form=form)


@app.route("/search", methods=["POST", "GET"])
def search():
    form = Search()
    if form.validate_on_submit():
        page = request.args.get('page', default=1, type=int)
        ads = Ad.query.filter(Ad.characteristics.like('%' + form.searched.data + '%')).paginate(per_page=3, page=page, error_out=True)
        return render_template("search.html", form=form, searched=form.searched.data, ads=ads)


@app.route("/sign-up", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserRegistration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, phone_number=form.phone_number.data,
                    city=form.city.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Your account has been successfully created! You are now logged in!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", year=year, title='Sign Up', form=form)


@app.route("/sign-in", methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginUser()
    if form.validate_on_submit():
        try:
            user_has_account = User.query.filter_by(email=form.email.data).first()
            passwords_match = bcrypt.check_password_hash(user_has_account.password, form.password.data)
            if passwords_match:
                login_user(user_has_account, remember=form.remember.data)
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check the credentials!', 'danger')
        except AttributeError:
            flash('Account does not exist. Please create an account!', 'danger')
    return render_template("sign-in.html", year=year, title='Sign In', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have logged out from your account!', 'info')
    return redirect(url_for('home'))


@app.route('/account/<username>', methods=["GET", "POST"])
def account(username):
    page = request.args.get('page', default=1, type=int)
    user = User.query.filter_by(username=username).first()
    ads = Ad.query.filter_by(seller=user).paginate(per_page=3, page=page, error_out=True)
    total = Ad.query.filter_by(seller=user).count()
    return render_template("account.html", user=user, year=year, title='Account', ads=ads, total=total)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/ads_images', picture_fn)
    output_size = (175, 175)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/new_ad', methods=["GET", "POST"])
@login_required
def new_ad():
    form = NewAd()
    if form.validate_on_submit():
        ad = Ad()
        if form.image.data:
            picture_file = save_picture(form.image.data)
            ad.image = picture_file
        ad.brand = form.brand.data
        ad.category = form.category.data
        ad.description = form.description.data
        ad.price = form.price.data
        ad.condition = form.condition.data
        ad.characteristics = form.characteristics.data
        ad.seller = current_user

        db.session.add(ad)
        db.session.commit()

        flash('Your advertisement has been successfully published!', 'success')
        return redirect(url_for('home'))

    return render_template("new_ad.html", year=year, title='New Ad', form=form)
# image_file=f'ads_images/{form.image.data}'


@app.route('/cell_phones', methods=["GET", "POST"])
def phones():
    page = request.args.get('page', default=1, type=int)
    ads = Ad.query.filter_by(category="Cell Phones").paginate(per_page=3, page=page, error_out=True)
    total = Ad()
    return render_template("ads.html", ads=ads, title='Cell Phones', url='phones', total=total)


@app.route('/computers', methods=["GET", "POST"])
def computers():
    page = request.args.get('page', default=1, type=int)
    ads = Ad.query.filter_by(category="Computers").paginate(per_page=3, page=page, error_out=True)
    total = Ad()
    return render_template("ads.html", ads=ads, total=total, title='Computers', url='computers')


@app.route('/tablets', methods=["GET", "POST"])
def tablets():
    page = request.args.get('page', default=1, type=int)
    ads = Ad.query.filter_by(category="Tablets").paginate(per_page=3, page=page, error_out=True)
    total = Ad()
    return render_template("ads.html", ads=ads, total=total, title='Tablets', url='tablets')


@app.route('/tv&video', methods=["GET", "POST"])
def tv_video():
    page = request.args.get('page', default=1, type=int)
    ads = Ad.query.filter_by(category="TV&Video").paginate(per_page=3, page=page, error_out=True)
    total = Ad()
    return render_template("ads.html", ads=ads, total=total, title='TV&Video', url='tv_video')


@app.route('/photo_cameras', methods=["GET", "POST"])
def photo_cameras():
    page = request.args.get('page', default=1, type=int)
    ads = Ad.query.filter_by(category="Photo Cameras").paginate(per_page=3, page=page, error_out=True)
    total = Ad()
    return render_template("ads.html", ads=ads, total=total, title='Photo Cameras', url='photo_cameras')


@app.route('/photo_cameras', methods=["GET", "POST"])
def e_books():
    page = request.args.get('page', default=1, type=int)
    ads = Ad.query.filter_by(category="E-Books").paginate(per_page=3, page=page, error_out=True)
    total = Ad()
    return render_template("ads.html", ads=ads, total=total, title='E-Books', url='e_books')


@app.route("/ad/<int:ad_id>/update", methods=['POST'])
@login_required
def delete_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    db.session.delete(ad)
    db.session.commit()
    flash('Your ad has been deleted!', 'success')
    return redirect(url_for('home'))