from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from webapp import app, db, bcrypt
from webapp.forms import RegistrationForm, LoginForm, CompanyEditForm, CompanyCreateForm, StudentCreateForm, StudentEditForm, AdvertisementCreateForm
from webapp.db_models import User,Companydetail,Advertisement, Studentdetail,Interestarea, Keyword, advertisement_keyword
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
#from webapp.db_models import Img
from base64 import b64encode
from webapp.util import get_interests,get_business_keywords, get_keywords
from webapp.util import is_email
import webapp
from datetime import date
from webapp.match import get_matching
from sqlalchemy import desc



@app.route( "/",methods=['GET', 'POST'] )
@app.route( "/home",methods=['GET', 'POST'] )
def home():
    filtered= ''
    if request.method=='POST':
        search_result =request.form.get("search_area")
        selection = request.form.get("selection")
        selected=[]
        if search_result:
            if selection == "company":
                company=Companydetail.query.filter(Companydetail.name.ilike("%" + search_result + "%")).all()

                print(company)
                if company != []:
                    advertisement = Advertisement.query.filter_by(companydetail_id=company[0].id).all()
                    selected = post_return(advertisement)


            elif selection == "title":
                advertisement = Advertisement.query.filter(Advertisement.title.ilike("%" + search_result + "%")).all()

                if advertisement != []:
                    selected = post_return(advertisement)
            else:
                key=Keyword.query.filter(Keyword.name.ilike("%" + search_result + "%")).first()
                print(key)
                if key is not None:
                    selected ,filtered =filter(key)




        if selected == []:
            flash("No result found for your search...", "danger")
        else:
            return render_template('home.html', posts=selected,filter_keyword=filtered)
    #get method below
    # advertisement = Advertisement.query.all()
    advertisement = Advertisement.query.order_by(Advertisement.date_posted.desc()).all()
    posts= post_return(advertisement)
    return render_template('home.html', posts=posts,filter_keyword=filtered)



def post_return(advertisement):
    posts = []
    for adv in advertisement:
        post = {}
        post['id'] = adv.id
        post['company'] = Companydetail.query.filter_by(id=adv.companydetail_id).first().name
        post['title'] = adv.title
        post['description'] = adv.description
        post['deadline'] = adv.deadline
        post['date_posted'] = adv.date_posted
        user_id = Companydetail.query.filter_by(id=adv.companydetail_id).first().user_id
        user_name = User.query.filter_by(id=user_id).first().username
        post["username"] = user_name
        keys = []
        keyword_adv = db.session.query(advertisement_keyword).filter_by(advertisement_id=adv.id).all()

        for k_id in keyword_adv:
            key = Keyword.query.filter_by(id=k_id[1]).first().name
            keys.append(key)
        post["keywords"] = keys
        posts.append(post)
    return posts
def filter(key):
    if key is not None:
        filtered = key.name
        key_ids = db.session.query(advertisement_keyword).filter_by(keyword_id=key.id).all()
        advertisements = []

        for ids in key_ids:
            advertisement = Advertisement.query.filter_by(id=ids.advertisement_id).first()
            advertisements.append(advertisement)

        selected =post_return(advertisements)
        return selected,filtered
    else:
        return [],''

@app.route( "/<keyword>",methods=['GET','POST'] )
def keywords(keyword):
    if request.method == 'GET':
        key = Keyword.query.filter(Keyword.name.ilike("%" + keyword + "%")).first()
        selected, filtered = filter(key)
        return render_template('home.html', posts=selected, filter_keyword=filtered)
    else:
        flash(f"No search method allowed for /{keyword} page...", "danger")
        return redirect(url_for("home"))



@app.route( "/<id>/detail",methods=['GET'] )
def ad_detail(id):
    adv = Advertisement.query.filter_by(id=id).first()
    post = {}
    post['id'] = adv.id
    comp=Companydetail.query.filter_by(id=adv.companydetail_id).first()
    post['company'] = comp.name
    post['title'] = adv.title
    post['description'] = adv.description
    post['deadline'] = adv.deadline
    post['date_posted'] = adv.date_posted
    user_id = Companydetail.query.filter_by(id=adv.companydetail_id).first().user_id
    user_name = User.query.filter_by(id=user_id).first().username
    post["username"] = user_name
    keys = []
    keyword_adv = db.session.query(advertisement_keyword).filter_by(advertisement_id=adv.id).all()
    for k_id in keyword_adv:
        key = Keyword.query.filter_by(id=k_id[1]).first().name
        keys.append(key)
    post["keywords"] = keys

    try:
        interval = int(str(adv.deadline - adv.date_posted).split(" ")[0])
    except:
        interval = 1
    try:
        position = int(str(date.today() - adv.date_posted).split(" ")[0])
    except:
        position = 0
    post["progress"]=int(position/interval*100)
    print(position,interval,post["progress"])

    accepted_students = []

    responses = webapp.db_models.Response.query.filter_by(advertisement_id=id).all()

    for response in responses:
        if response.answer == 1:
            student = User.query.filter_by(id=response.user_id).first()
            accepted_students.append(student)

    post["accepted_students"] = accepted_students

    return render_template("adv_detail.html",post=post, comp=comp)







@app.route( "/about" )
def about():
    return render_template( 'about.html', title='About' )


@app.route( "/create_profile" )
def create_profile():
    editform = CompanyCreateForm()
    editform_student = StudentCreateForm()
    return render_template( 'create_profile.html', title='Create Profile', form=editform, form_student=editform_student)


@app.route( "/create_profile_student", methods=['POST'])
def create_profile_student():
    editform_student = StudentCreateForm()
    if request.method == 'POST':
        if editform_student.validate_on_submit():

            student_detail = Studentdetail()
            student_detail.user_id = current_user.id

            student_detail.name_surname = editform_student.name.data
            student_detail.university = editform_student.university.data
            student_detail.class_level = editform_student.class_level.data
            student_detail.gpa = editform_student.gpa.data
            student_detail.active = editform_student.active.data
            student_detail.github = editform_student.github.data
            student_detail.linkedin = editform_student.linkedin.data
            student_detail.description = editform_student.description.data

            keywords = get_keywords(editform_student.keywords.data, -1)

            student_detail.keywords = keywords

            # get image
            image = editform_student.image.data
            if image:
                filename = secure_filename(image.filename)
                mimetype = image.mimetype

                student_detail.img = b64encode(image.read()).decode("utf-8")
                student_detail.imgname = filename
                student_detail.mimetype = mimetype

            try:
                db.session.add(student_detail)
                current_user.complete = True
                current_user.type = True
                db.session.add(current_user)
                db.session.commit()


                print("success")
            except AssertionError as err:
                db.session.rollback()
                print("rollback")

            return redirect(url_for('account', username=current_user.username))
        else:
            return redirect(url_for('account', username=current_user.username))

    return render_template( 'create_profile.html', title='Create Profile', form=editform_student)


@app.route( "/create_profile_company", methods=['POST'])
def create_profile_company():
    editform = CompanyCreateForm()
    if request.method == 'POST':
        if editform.validate_on_submit():

            company_details = Companydetail()
            company_details.user_id = current_user.id

            company_details.name = editform.name.data
            company_details.description = editform.description.data
            company_details.address = editform.address.data
            company_details.linkedin = editform.linkedin.data
            company_details.github = editform.github.data
            company_details.website = editform.website.data
            company_details.numberofworkers = editform.numberofworkers.data
            # company_details.sector = editform.sector.data

            # all the interest should be added for the company beacuse it is newly created
            interests = get_interests(editform.sector.data, -1)

            company_details.interests = interests

            print(company_details)

            # get image
            image = editform.image.data
            if image:
                filename = secure_filename(image.filename)
                mimetype = image.mimetype

                company_details.img = b64encode(image.read()).decode("utf-8")
                company_details.imgname = filename
                company_details.mimetype = mimetype

            try:
                db.session.add(company_details)
                current_user.complete = True
                current_user.type = False
                db.session.add(current_user)
                db.session.commit()


                print("success")
            except AssertionError as err:
                db.session.rollback()
                print("rollback")

            return redirect( url_for( 'account2', username=current_user.username ) )
        else:
            return redirect(url_for('account', username=current_user.username))

    return render_template( 'create_profile.html', title='Create Profile', form=editform)

@app.route( "/account/" )
@login_required  # from flask_login package
def account():

    if current_user.complete == False:
        return redirect(url_for('create_profile'))

    if current_user.type == False:  # if it is company
        return redirect( url_for( 'account2', username=current_user.username ) )
    # if it is user --> userprofile redirect
    else:
        return redirect(url_for('account1', username=current_user.username))

    #TODO: Add if statement admin and student page

@app.errorhandler( 401 )
def page_not_found(e):
    # note that we set the 401 status explicitly
    return render_template( '401.html' ), 401

@app.errorhandler( 404 )
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template( '404.html' ), 404

@app.route( "/response/<ad_id>",methods=['POST'])
def response(ad_id):

    response = request.form['res']
    if response == 'Accept':
        my_response = webapp.db_models.Response()
        my_response.user_id = current_user.id
        my_response.advertisement_id = int(ad_id)
        my_response.answer = 1
        try:
            db.session.add(my_response)
            db.session.commit()
        except AssertionError as err:
            db.session.rollback()

    elif response == 'Reject':
        my_response = webapp.db_models.Response()
        my_response.user_id = current_user.id
        my_response.advertisement_id = int(ad_id)
        my_response.answer = 0
        try:
            db.session.add(my_response)
            db.session.commit()
        except AssertionError as err:
            db.session.rollback()
    else:
        return render_template('404.html'), 404

    if current_user.type == False:  # if it is company
        return redirect( url_for( 'account2', username=current_user.username ) )
    else:
        return redirect(url_for('account1', username=current_user.username))

#student account page
@app.route( "/student/<username>",methods=['GET', 'POST'])
def account1(username):
    user = User.query.filter_by(username=username).first()
    try:
        for responsed in user.responses:
            user.advertisements.remove(responsed.advertisement)
    except:
        pass

    if user is not None :
        if user.complete == False :
            abort(404, description="Resource not found")
            return render_template('404.html')
        else:
            business_keywords = []
            for i in user.student_details.keywords:
                business_keywords.append(i.name)
            img_data = user.student_details.img
            editform = StudentEditForm()
            if request.method == 'POST':
                if editform.validate_on_submit():
                    # Only current user can do editing, so I am changing currentuser.

                    hashed_password = bcrypt.generate_password_hash(editform.password.data).decode('utf-8')
                    current_user.email = editform.email.data

                    current_user.student_details.name_surname = editform.name_surname.data
                    current_user.student_details.university = editform.university.data
                    current_user.student_details.description = editform.description.data
                    current_user.student_details.class_level = editform.class_level.data
                    current_user.student_details.gpa = editform.gpa.data

                    current_user.student_details.linkedin = editform.linkedin.data
                    current_user.student_details.github = editform.github.data
                    current_user.student_details.active = editform.active.data

                    keywords = get_keywords(editform.keywords.data, current_user.student_details.id)

                    if keywords and len(keywords) > 0:
                        if len(current_user.student_details.keywords) > 0:
                            current_user.student_details.keywords.extend(keywords)
                        else:
                            current_user.student_details.keywords = keywords



                    image = editform.image.data
                    if image:
                        filename = secure_filename(image.filename)
                        mimetype = image.mimetype

                        current_user.student_details.img = b64encode(image.read()).decode("utf-8")
                        current_user.student_details.imgname = filename
                        current_user.student_details.mimetype = mimetype

                    try:
                        db.session.add(current_user)
                        db.session.commit()
                    except AssertionError as err:
                        db.session.rollback()
                        print("rollback")

                    img_data = current_user.student_details.img
                    return render_template('account_student.html', user=current_user, form=editform,
                                           formerror=False, img_data=img_data, business_keywords = business_keywords)


            return render_template('account_student.html', user=user, form=editform, formerror=False, img_data = img_data, business_keywords = business_keywords)
    else:
        abort(404, description="Resource not found")
        return render_template('404.html')
    return render_template( 'layout.html')

@app.route( "/company/<username>",methods=['GET', 'POST'])
def account2(username):
    user = User.query.filter_by( username=username ).first()
    if user is not None and user.type == False:  # if it is company #check if details is completed
        ads = user.company_details.advertisements
        ads_sorted  = sorted(ads, key=lambda x: x.date_posted, reverse=True)
        img_data = user.company_details.img
        business_keywords = get_business_keywords(user)

        editform = CompanyEditForm()


        if request.method == 'POST':
            if editform.validate_on_submit():
                # Only current user can do editing, so I am changing currentuser.
                hashed_password = bcrypt.generate_password_hash( editform.password.data ).decode( 'utf-8' )
                current_user.username = editform.username.data
                current_user.email = editform.email.data
                current_user.company_details.name = editform.name.data
                current_user.company_details.description = editform.description.data
                current_user.company_details.address = editform.address.data
                current_user.company_details.linkedin = editform.linkedin.data
                current_user.company_details.github = editform.github.data
                current_user.company_details.website = editform.website.data
                current_user.company_details.numberofworkers = editform.numberofworkers.data
                interests = get_interests(editform.sector.data,current_user.company_details.id)

                if interests and len(interests)>0:
                    if len(current_user.company_details.interests)>0:current_user.company_details.interests.extend(interests)
                    else:current_user.company_details.interests = interests


                #get image
                image = editform.image.data
                if image:
                    filename = secure_filename(image.filename )
                    mimetype = image.mimetype

                    current_user.company_details.img = b64encode(image.read()).decode("utf-8")
                    current_user.company_details.imgname = filename
                    current_user.company_details.mimetype = mimetype





                try:
                    db.session.add(current_user)
                    db.session.commit()
                except AssertionError as err:
                    db.session.rollback()
                    print("rollback")

                ads = current_user.company_details.advertisements
                ads_sorted = sorted( ads, key=lambda x: x.date_posted, reverse=True )
                img_data = current_user.company_details.img
                return render_template( 'account_company.html', user=current_user, ads = ads_sorted, form = editform, formerror = False, img_data = img_data, business_keywords = business_keywords)
            else:

                return render_template( 'account_company.html', user=user, ads=ads_sorted, form=editform, formerror = True, img_data = img_data, business_keywords = business_keywords)


        return render_template( 'account_company.html', user=user, ads = ads_sorted, form = editform, formerror = False, img_data = img_data, business_keywords = business_keywords)
    else:
        abort( 404, description="Resource not found" )
        return render_template( '404.html' )


@app.route( "/register", methods=['GET', 'POST'] )
def register():
    if current_user.is_authenticated:
        return redirect( url_for( 'home' ) )

    form = RegistrationForm()

    # came from posted form, if validated
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash( form.password.data ).decode( 'utf-8' )
        user = User( username=form.username.data, email=form.email.data, password=hashed_password )
        db.session.add( user )
        db.session.commit()
        flash( f'Account created for {form.username.data}!', 'success' )
        return redirect( url_for( 'login' ) )

    return render_template( 'register.html', title='Register', form=form )


@app.route( "/login", methods=['GET', 'POST'] )
def login():
    if current_user.is_authenticated:
        return redirect( url_for( 'home' ) )

    form = LoginForm()

    # came from posted form, if validated including database.
    if form.validate_on_submit():

        input = form.email.data
        if is_email(input):
            user = User.query.filter_by( email = input ).first()
        else:
            user = User.query.filter_by(username = input ).first()




        if user and bcrypt.check_password_hash( user.password, form.password.data ):

            login_user( user, remember=form.remember.data )

            # from where login page is reached
            next_page = request.args.get( 'next' )
            if next_page:
                return redirect( next_page )  # url_for or pure string?
            else:
                return redirect( url_for( 'home' ) )
        else:
            flash( 'Login Unsuccessful. Please check username and password', 'danger' )
    return render_template( 'login.html', title='Login', form=form )


@app.route( "/logout" )
def logout():
    logout_user()  # from flask_login package
    return redirect( url_for( 'home' ) )


@app.route("/search")
def search():
    username = request.args.get( 'name' )
    users = User.query.filter(User.username.ilike(username+"%")).all()

    companies = []
    students = []
    for u in users:
        if u.type:
            students.append(u)
        else:
            companies.append(u)

    return render_template('searchresults.html',students = students,companies = companies)


@app.route("/deleteinterest")
def delete_interest():
    company_detail_id = int(request.args.get('company_detail_id'))
    interest_id = int(request.args.get('interest_id'))


    company_detail_entity = Companydetail.query.filter_by(id = company_detail_id).first()
    if company_detail_entity:
        new_interests = []
        for i in company_detail_entity.interests:
            if i.id == interest_id:
                continue
            new_interests.append(i)
        company_detail_entity.interests = new_interests

    try:
        db.session.add(company_detail_entity)
        db.session.commit()
    except AssertionError as err:
        db.session.rollback()



    return redirect(url_for('account2',username = company_detail_entity.user.username))


@app.route("/create_advertisement", methods=['GET', 'POST'])
def create_advertisement():
    form = AdvertisementCreateForm()
    if request.method == 'POST':

        advertisement_details = Advertisement()
        advertisement_details.companydetail_id = current_user.company_details.id
        advertisement_details.title = form.title.data
        advertisement_details.description = form.description.data
        advertisement_details.date_posted = date.today()
        advertisement_details.deadline = form.deadline.data

        keywords = get_keywords(form.keywords.data, -1)

        advertisement_details.keywords = keywords

        try:

            #matching algorithm
            get_matching(advertisement_details)

            db.session.add( advertisement_details )
            db.session.commit()
            print("success")




            return redirect(url_for('account2', username=current_user.username))
        except AssertionError as err:
            db.session.rollback()
            print("rollback")

        # print(advertisement_details)

    return render_template('advertisement.html', form=form)


@app.route("/admin_panel")
def admin_panel():
    if not current_user.is_authenticated:
        abort(404, description="Resource not found")
        return render_template('404.html')
    if not current_user.username == "admin":
        abort(404, description="Resource not found")
        return render_template('404.html')

    advertisement = Advertisement.query.all()
    posts = post_return(advertisement)
    users = User.query.all()

    for user in users:
        if user.username == "admin":
            users.remove(user)
            break

    return render_template('admin_panel_page.html', posts=posts, users=users)

@app.route( "/delete_job_adv/<id>")
def delete_job_adv(id):

    if not current_user.is_authenticated:
        abort(404, description="Resource not found")
        return render_template('404.html')
    if not current_user.username == "admin":
        abort(404, description="Resource not found")
        return render_template('404.html')

    advertisement = Advertisement.query.filter_by(id=id).first()
    responses = webapp.db_models.Response.query.filter_by(advertisement_id=advertisement.id).all()
    print(advertisement)
    try:
        for resp in responses:
            db.session.delete(resp)
        db.session.delete(advertisement)
        db.session.commit()

        print("success")
    except AssertionError as err:
        db.session.rollback()
        print("rollback")
        abort(404, description="Resource not found")
        return render_template('404.html')

    return redirect(url_for("admin_panel"))


@app.route( "/delete_user/<id>")
def delete_user(id):

    if not current_user.is_authenticated:
        abort(404, description="Resource not found")
        return render_template('404.html')
    if not current_user.username == "admin":
        abort(404, description="Resource not found")
        return render_template('404.html')

    user = User.query.filter_by(id=id).first()
    if user.type:
        student_detatil = Studentdetail.query.filter_by(user_id=id).first()
        responses = webapp.db_models.Response.query.filter_by(user_id=user.id).all()

        try:
            for resp in responses:
                db.session.delete(resp)
            db.session.delete(student_detatil)
            db.session.delete(user)
            db.session.commit()

            print("success")
        except AssertionError as err:
            db.session.rollback()
            print("rollback")
            abort(404, description="Resource not found")
            return render_template('404.html')
    else:
        company_detail = Companydetail.query.filter_by(user_id=id).first()
        adverts = Advertisement.query.filter_by(companydetail_id=company_detail.id).all()
        print(user)
        try:
            for adv in adverts:
                db.session.delete(adv)
            db.session.delete(company_detail)
            db.session.delete(user)
            db.session.commit()

            print("success")
        except AssertionError as err:
            db.session.rollback()
            print("rollback")
            abort(404, description="Resource not found")
            return render_template('404.html')

    return redirect(url_for("admin_panel"))
