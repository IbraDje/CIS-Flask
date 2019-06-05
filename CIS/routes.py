from flask import (render_template, flash, url_for,
                   redirect, request, abort, jsonify)
from flask_login import login_user, current_user, logout_user, login_required
from CIS import app, db, bcrypt
from CIS.forms import AlgorithmForm, RegistrationForm, LoginForm
import CIS.utils as utils
from CIS.models import User, Run
import matplotlib.image as mpimg
import arrow
import ast


@app.route("/", methods=['GET', 'POST'])
def home_page():
    return render_template('home.html', title='Home', form=AlgorithmForm(),
                           login=LoginForm())


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    login = LoginForm()
    if login.validate_on_submit():
        user = User.query.filter_by(username=login.username.data).first()
        if user and bcrypt.check_password_hash(
                user.password, login.password.data):
            login_user(user, remember=login.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('home_page'))
        else:
            flash('Login unsuccessful. Please check your email and password',
                  'danger')
            return redirect(url_for('login_page'))
    return render_template('login.html', title='Login', form=login)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, You are now able to log in.',
              'success')
        return redirect(url_for('login_page'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))


@app.route("/account")
@login_required
def account_page():
    runs = Run.query.filter_by(user=current_user).order_by(Run.date_ran.desc())
    return render_template('account.html', title='Account', runs=runs,
                           arrow=arrow, ast=ast)


@app.route("/run/<int:run_id>")
@login_required
def run_page(run_id):
    run = Run.query.get_or_404(run_id)
    return render_template('run.html', title='Run', run=run, ast=ast)


@app.route("/run/<int:run_id>/delete", methods=['POST'])
@login_required
def delete_run(run_id):
    run = Run.query.get_or_404(run_id)
    if run.user != current_user:
        abort(403)
    db.session.delete(run)
    db.session.commit()
    utils.empty_input()
    utils.empty_output()
    flash('The run has been deleted.', 'info')
    return redirect(url_for('account_page'))


@app.route('/process', methods=['POST'])
def process():
    form = AlgorithmForm()
    WSS = BSS = None
    if request.method == 'POST' and form.validate_on_submit():
        image = request.files['image']
        utils.empty_input()
        utils.empty_output()
        input_image_path, input_image_name = utils.save_image(image)
        input_image = mpimg.imread(input_image_path)
        if request.form['algorithm'] != 'VIBGYOR':
            if request.form['algorithm'] == 'K-Means':
                labels, centers = utils.kmeans_images(
                    input_image, int(request.form['clusters']))
            elif request.form['algorithm'] == 'FCM':
                labels, centers = utils.fcm_images(
                    input_image, int(request.form['clusters']))
            elif request.form['algorithm'] == 'PFCM':
                labels, centers = utils.pfcm_images(
                    input_image, int(request.form['clusters']))
            if request.form['choices'] == 'manyImages':
                output_image_name = utils.create_images(labels, centers)
            else:
                output_image_name = utils.create_image(labels, centers)
            WSS = utils.compactness(input_image, labels, centers)
            BSS = utils.separation(labels, centers)
            if current_user.is_authenticated:
                run = Run(algorithm=request.form['algorithm'],
                          clusters=request.form['clusters'], compactness=WSS,
                          separation=BSS, input_image=input_image_name,
                          output_image=str(output_image_name),
                          user_id=current_user.id)
                db.session.add(run)
                db.session.commit()
        else:
            output_image_name = utils.vibgyor(
                input_image, request.form['colors'])
            if current_user.is_authenticated:
                run = Run(algorithm=request.form['algorithm'],
                          color=request.form['colors'],
                          input_image=input_image_name,
                          output_image=output_image_name,
                          user_id=current_user.id)
                db.session.add(run)
                db.session.commit()
        return jsonify(output_image=output_image_name, compactness=WSS,
                       separation=BSS,
                       message=request.form['algorithm']+' ran successfully.')
    return jsonify(image_errors=form.image.errors,
                   clusters_errors=form.clusters.errors,
                   algorithm_errors=form.algorithm.errors,
                   colors_errors=form.colors.errors)
