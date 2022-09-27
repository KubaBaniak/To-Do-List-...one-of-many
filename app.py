from flask import Flask, render_template, request, url_for, redirect
from wtforms import Form, StringField
from wtforms.validators import DataRequired
import itertools
from datetime import datetime


app = Flask(__name__)
app.secret_key = '3331df6bcb0872a25088de46'
activities_dict = {}


class Activity:

    newid = itertools.count()

    def __init__(self, name):
        self.name = name
        self.status = False
        self.id = next(Activity.newid)
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def change_status(self):
        self.status = not self.status
        return self.status

class AddActivity(Form):
    activity_name = StringField('Type your activity', [DataRequired()])


@app.route('/', methods=["GET", "POST"])
def landing_page():
    form = AddActivity(request.form)

    if request.method == "POST" and form.validate():
        activity_from_form = Activity(form.activity_name.data)
        activities_dict[activity_from_form.id] = activity_from_form
        return redirect(url_for('landing_page'))

    return render_template("index.html", form=form, l=activities_dict.items())

@app.route('/delete_activity/<int:id>')
def delete_activity(id):
    del activities_dict[id]
    return redirect(url_for('landing_page'))
