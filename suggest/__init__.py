# encoding: utf-8
from flask import Flask, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Email, DataRequired


app = Flask("suggest")
app.config.from_pyfile("settings.py")


db = SQLAlchemy(app)

Bootstrap(app)


class SuggestModel(db.Model):
	__tablename__ = "suggestions"
	suggest_id = db.Column(db.Integer(), primary_key=True)
	name_user = db.Column(db.String(50))
	email_user = db.Column(db.String(50))
	suggest = db.Column(db.String(70))
	description = db.Column(db.Text())

db.create_all()
db.session.commit()


class SuggestForm(Form):
	name = StringField("Nome", validators=[DataRequired()])
	email = StringField("Email", validators=[Email()]) 
	sugestion = StringField("Sugestao", validators=[DataRequired()])
	description = TextAreaField("Descricao")
	submit = SubmitField("Enviar")


@app.route("/", methods=['GET', 'POST'])
def home():
	form = SuggestForm()
	if form.validate_on_submit():
		suggest = SuggestModel()
		suggest.name_user = form.name.data
		suggest.email_user = form.email.data
		suggest.suggest = form.sugestion.data
		suggest.description = form.description.data

		db.session.add(suggest)
		db.session.commit()

		return redirect(url_for("thanks"))	
	return render_template("index.html", form_sugestion=form)


@app.route('/thanks')
def thanks():
	return render_template("thanks.html")
