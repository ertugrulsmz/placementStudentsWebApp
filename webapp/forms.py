from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, IntegerField, FloatField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from webapp.db_models import User
from flask_login import current_user
from webapp import bcrypt


class RegistrationForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # db validation for uniqueness in form
    def validate_username(self, username):
        user = User.query.filter_by( username=username.data ).first()
        if user:
            raise ValidationError( 'That username is taken. Please choose a different one.' )

    # db validation for uniqueness in form
    def validate_email(self, email):
        user = User.query.filter_by( email=email.data ).first()
        if user:
            raise ValidationError( 'That email is taken. Please choose a different one.' )


class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CompanyEditForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField( 'Username',
                            validators=[DataRequired(), Length( min=2, max=20 )] )
    email = StringField( 'Email',validators=[DataRequired(), Email()] )
    password = PasswordField( 'Password', validators=[DataRequired()] )
    confirm_password = PasswordField( 'Confirm Password',
                                      validators=[DataRequired(), EqualTo( 'password' )] )
    website = StringField( 'Website' )
    linkedin = StringField( 'Linkedin')
    github = StringField( 'GitHub')
    name = StringField('Name')
    address = StringField('Address')
    image = FileField( 'Image', validators=[FileAllowed( ['jpg', 'png'] )] )
    description = StringField('description',validators=[DataRequired()])
    sector = StringField( 'interests')
    numberofworkers = IntegerField('numberofworkers',validators=[DataRequired()])

    submit = SubmitField( 'Update' )

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by( username=username.data ).first()
            if user:
                raise ValidationError( 'That username is taken. Please choose a different one.' )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by( email=email.data ).first()
            if user:
                raise ValidationError( 'That email is taken. Please choose a different one.' )

    def validate_password(self,password):

        if bcrypt.check_password_hash( current_user.password, password.data ) == False:
            raise ValidationError( 'That password does not belong to this account' )


class StudentEditForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField( 'Username',
                            validators=[DataRequired(), Length( min=2, max=20 )] )
    email = StringField( 'Email',validators=[DataRequired(), Email()] )
    password = PasswordField( 'Password', validators=[DataRequired()] )
    confirm_password = PasswordField( 'Confirm Password',
                                      validators=[DataRequired(), EqualTo( 'password' )] )
    name_surname = StringField( 'NameSurname' )
    university = StringField('university')
    description = StringField('Description')
    class_level = IntegerField('class_level',validators=[DataRequired()])
    gpa = FloatField("GPA")

    keywords = StringField('Keywords (comma separated)')

    github = StringField('GitHub')
    linkedin = StringField( 'Linkedin')
    active = BooleanField("Active Student")
    image = FileField( 'Image', validators=[FileAllowed( ['jpg', 'png'] )] )
    submit = SubmitField( 'Update' )

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by( username=username.data ).first()
            if user:
                raise ValidationError( 'That username is taken. Please choose a different one.' )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by( email=email.data ).first()
            if user:
                raise ValidationError( 'That email is taken. Please choose a different one.' )

    def validate_password(self,password):

        if bcrypt.check_password_hash( current_user.password, password.data ) == False:
            raise ValidationError( 'That password does not belong to this account' )

class CompanyCreateForm(FlaskForm):
    class Meta:
        csrf = False
    website = StringField( 'Website' )
    linkedin = StringField( 'Linkedin')
    github = StringField( 'GitHub')
    name = StringField('Name')
    address = StringField('Address')
    image = FileField( 'Image', validators=[FileAllowed( ['jpg', 'png'] )] )
    description = StringField('Description',validators=[DataRequired()])
    sector = StringField( 'Interest Areas (comma separated)', validators=[DataRequired()] )
    numberofworkers = IntegerField('Number of Workers',validators=[DataRequired()])
    submit = SubmitField( 'Create' )


class StudentCreateForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Name Surname')
    university = StringField('University')
    class_level = IntegerField('Class')
    gpa = FloatField("GPA")
    active = BooleanField("Active Student")
    linkedin = StringField( 'Linkedin')
    github = StringField( 'GitHub')
    image = FileField( 'Image', validators=[FileAllowed( ['jpg', 'png'] )] )
    keywords = StringField('Keywords (comma separated)')
    description = StringField('Description')
    submit = SubmitField( 'Create' )

my_choices = [('1', 'Python'), ('2', 'Deep Learning'), ('3', 'Java')]
class AdvertisementCreateForm(FlaskForm):
    class Meta:
        csrf = False
    title = StringField('Title')
    description = StringField('Description')
    deadline = DateField('Deadline Date', format='%m/%d/%Y')
    submit = SubmitField('Submit')
    keywords = StringField('Keywords (comma separated)')
