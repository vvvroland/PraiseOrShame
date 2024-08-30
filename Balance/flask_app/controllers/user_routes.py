from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.models.user_extractions import Users
from flask_app.models.window_extractions import Praise, Shame
from flask_bcrypt import Bcrypt    

bcrypt = Bcrypt(app) 

#Method for viewing gatekeeper
@app.route('/gatekeeper')
def gatekeeper():
    return render_template('gatekeeper.html')                     #maybe we check the session here as well?


@app.route('/register', methods=['POST'])                                     #post method to register a person and bring them to their profile
def register_user():
    if not Users.valid_register(request.form):
        return redirect('/gatekeeper')
    hashed_pass=bcrypt.generate_password_hash(request.form['password'])
    data={
        **request.form,
        'password': hashed_pass,
        'confirm': hashed_pass
    }
    user_id=Users.create(data)
    session['user_id'] =user_id  ##means user is loged in
    return redirect ('/profile/mine')

@app.route('/login', methods=['Post'])                                      #post method to log in a person and bring them to their profile
def login_user():
    potential_user = Users.get_by_email(request.form)
    if not potential_user:
        flash('Invalid credentials(email)','login')
        return redirect('/gatekeeper')

    if not bcrypt.check_password_hash(potential_user.password,request.form['password']):
        flash('Invalid credentials password', 'login')
        return redirect('/gatekeeper')
    session['user_id'] =potential_user.id
    return redirect('/profile/mine')

# @app.route('/users/recipes')
# def dash():
#     if 'user_id' not in session:
#         return redirect('/')
#     logged_user = Users.get_by_id({'id':session['user_id']})
#     return render_template ('recipes.html', one_user=logged_user)

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/')