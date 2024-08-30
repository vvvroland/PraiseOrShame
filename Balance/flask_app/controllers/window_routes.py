from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.models.user_extractions import Users
from flask_app.models.window_extractions import Praise, Shame
from flask_bcrypt import Bcrypt   
import random


#### A small, not well focused change lead to broken routes
#### I changed the routing to the community page so the things function
#### Pretty sure the routing f-strings need the id defined as the user ID more clearly


@app.route('/')
def looking_in():
    return render_template('landing.html')   #Just to view the landing page



@app.route('/profile/mine')
def mine():
    if 'user_id' not in session:
        return render_template('gatekeeper.html')
    view_user = Users.get_by_id({'id':id})
    logged_user = Users.get_by_id({'id':session['user_id']})
    your_public_praise=Praise.get_all_praise_public_by_id({'id':session['user_id']})
    your_private_praise=Praise.get_all_praise_private_by_id({'id':session['user_id']})
    your_public_shame=Shame.get_all_shame_public_by_id({'id':session['user_id']})
    your_private_shame=Shame.get_all_shame_private_by_id({'id':session['user_id']})
    return render_template('profile.html', one_user=logged_user, public_praise=your_public_praise, private_praise=your_private_praise, public_shame=your_public_shame, private_shame=your_private_shame, view_user=view_user)


@app.route('/profile/<int:id>/view')
def view(id):
    if 'user_id' not in session:
        return render_template('gatekeeper.html')
    context ={
    'one_user' : Users.get_by_id({'id':session['user_id']}),
    'view_user' : Users.get_by_id({'id':id}),
    'public_praise' : Praise.get_all_praise_public_by_id({'id':id}),
    'private_praise' : Praise.get_all_praise_private_by_id({'id':id}),
    'public_shame' : Shame.get_all_shame_public_by_id({'id':id}),
    'private_shame' : Shame.get_all_shame_private_by_id({'id':id})
    }
        
    return render_template('profile.html',**context)




@app.route('/community')
def dashboard():
    if 'user_id' not in session:
        return render_template('gatekeeper.html')
    logged_user = Users.get_by_id({'id':session['user_id']})
    all_praise=Praise.get_all_praise_public()
    all_shame=Shame.get_all_shame_public()
    return render_template('community.html', one_user=logged_user, all_praise=all_praise, all_shame=all_shame )


#Picking landing page randoms
@app.route('/api/random_praise')
def random_praise():
    praises=Praise.get_all_praise_public_api()
    select_praise=random.choice(praises)
    return select_praise

@app.route('/api/random_shame')
def random_shame():
    shames=Shame.get_all_shame_public_api()
    print(shames)
    select_shame=random.choice(shames)
    return select_shame


#Adding likes to the landing page randoms,
@app.route('/api/like/<int:id>/praise')
def like_praise_api(id):
    data = {
        'id':id
    }
    newlike=Praise.add_like_praise_api(data)
    return redirect('/community')

@app.route('/api/like/<int:id>/shame')
def like_shame_api(id):
    data = {
        'id':id
    }
    newlike=Shame.add_like_shame_api(data)
    return redirect('/community')

#Adding likes to community pages, 
@app.route('/like/<int:id>/praise')
def like_praise(id):
    data = {
        'id':id
    }
    newlike=Praise.add_like_praise(data)
    return redirect('/community')

@app.route('/like/<int:id>/shame')
def like_shame(id):
    data = {
        'id':id
    }
    newlike=Shame.add_like_shame(data)
    return redirect('/community')

#editing praises and shames, pulling up the edit pages
@app.route('/edit/<int:id>/praise')
def show_edit_praise(id):
    if "user_id" not in session:
        return redirect ('/')
    one_praise=Praise.get_by_id_praise({'id':id})
    return render_template('edit_praise.html', one_praise=one_praise)

@app.route('/edit/<int:id>/shame')
def show_edit_shame(id):
    if "user_id" not in session:
        return redirect ('/')
    one_shame=Shame.get_by_id_shame({'id':id})
    return render_template('edit_shame.html', one_shame=one_shame)

#editing praises and shames, actual sending the query.
@app.route('/update/<int:id>/praise', methods=['POST'])
def post_edit_praise(id):
    if "user_id" not in session:
        return redirect ('/')
    data = {
        **request.form,
        'id':id                                                       #taking the info from the request form and the recipe id passed in as the data
    }
    if not Praise.valid_praise(request.form):                        #are we filled out, reason we're passing just the form, not the data, which includes the id we already kno
        return redirect(f'/edit/{id}/praise')                  #go back to the edit form with it filled out per the values in the html
    print('fun******************************************************')   #check to see if the validator is the thing holding things back
    check = Praise.update_praise(data)   
    print(check)                                             #passing the form+id into the update method (from extractions) and applying the class to the data
    return redirect ('/community')

@app.route('/update/<int:id>/shame', methods=['POST'])
def post_edit_shame(id):
    if "user_id" not in session:
        return redirect ('/')
    data = {
        **request.form,
        'id':id                                                       #taking the info from the request form and the recipe id passed in as the data
    }
    if not Shame.valid_shame(request.form):                        #are we filled out, reason we're passing just the form, not the data, which includes the id we already kno
        return redirect(f'/edit/{id}/shame')                  #go back to the edit form with it filled out per the values in the html
    print('fun******************************************************')   #check to see if the validator is the thing holding things back
    Shame.update_shame(data)                                                #passing the form+id into the update method (from extractions) and applying the class to the data
    return redirect ('/community')

#Pulling up the add pages
@app.route('/show_add/praise')
def show_add_praise():
    if "user_id" not in session:
        return redirect ('/')
    return render_template('add_praise.html')

@app.route('/show_add/shame')
def show_add_shame():
    if "user_id" not in session:
        return redirect ('/')
    return render_template('add_shame.html')

#Posting the add from the add pages
@app.route('/praise/add', methods=['POST'])                                   #the action of adding the recipe, posting it
def post_add_praise():
    if "user_id" not in session:
        return redirect ('/')
    if not Praise.valid_praise(request.form):
        return redirect('/show_add/praise')                   #if form not complete per validator, bring back to the page
    praise_data={
        **request.form,
        'userpr_id':session['user_id']                       #This is telling the query to use the logged in person's ID as the id part of the query...
    }
    # user_id=Users.create(recipe_data)
    Praise.add_praise(praise_data)                          #Creating the actual new recipe, passing in the request forn and logged in user ID
    return redirect ('/community')  

@app.route('/shame/add', methods=['POST'])                                   #the action of adding the recipe, posting it
def post_add_shame():
    if "user_id" not in session:
        return redirect ('/')
    if not Shame.valid_shame(request.form):
        return redirect('/show_add/shame')                   #if form not complete per validator, bring back to the page
    shame_data={
        **request.form,
        'usersh_id':session['user_id']                       #This is telling the query to use the logged in person's ID as the id part of the query...
    }
    # user_id=Users.create(recipe_data)
    Shame.add_shame(shame_data)                          #Creating the actual new recipe, passing in the request forn and logged in user ID
    return redirect ('/community')  

#Pulling up the delete decision page
@app.route('/delete_confirm/<int:id>/praise')
def show_delete_praise(id):
    if "user_id" not in session:
        return redirect ('/')
    one_praise=Praise.get_by_id_praise({'id':id})
    return render_template('delete_praise.html', one_praise=one_praise)

@app.route('/delete_confirm/<int:id>/shame')
def show_delete_shame(id):
    if "user_id" not in session:
        return redirect ('/')
    one_shame=Shame.get_by_id_shame({'id':id})
    return render_template('delete_shame.html', one_shame=one_shame)

#Confirming the delete
@app.route('/delete/<int:id>/praise', methods=['POST'])
def post_delete_praise(id):
    if "user_id" not in session:
        return redirect ('/')
    praise_data={
        **request.form,
        'userpr_id':session['user_id'],                       #This is telling the query to use the logged in person's ID as the id part of the query...
        'id':id
    }
    check = Praise.delete_praise(praise_data)   
    print(check)                                             #passing the form+id into the update method (from extractions) and applying the class to the data
    return redirect ('/community')

@app.route('/delete/<int:id>/shame', methods=['POST'])
def post_delete_shame(id):
    if "user_id" not in session:
        return redirect ('/')
    shame_data={
        **request.form,
        'usersh_id':session['user_id'],                       #This is telling the query to use the logged in person's ID as the id part of the query...
        'id':id
    }
    check = Shame.delete_shame(shame_data) 
    print(check)                                               #passing the form+id into the update method (from extractions) and applying the class to the data
    return redirect ('/community')