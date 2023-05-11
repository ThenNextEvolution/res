from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db =SQLAlchemy(app)


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



        

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    data_created = db.Column(db.DateTime, default = datetime.utcnow())
    store_img = db.Column(db.Text, nullable =False, default=r"C:\\Users\\eyita\\flask\\static\\imgs\\test.jpg")
    straddy = db.Column(db.Text)
    # img =db.Column(db.Hyperlink, default =Image.open(r"C:\\Users\\eyita\\flask\\static\\imgs\\test.jpg"))
    
    def __repr__(self):
        return "Task %r>" % self.id

@app.route('/',methods =["POST","GET"])
def index():
    if request.method== "POST":
       Task_content = request.form['content']
       add = request.form["addy"]
       new_Task = Todo(content=Task_content,straddy=add)
       
       try:
           db.session.add(new_Task)
           db.session.commit()
           return redirect('/')
       except:
           return "There was an issue"
    else:
        tasks = Todo.query.order_by(Todo.data_created).all()
        return render_template("index.html",tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task2d =Todo.query.get_or_404(id)
    try:
        db.session.delete(task2d)
        db.session.commit()
        return redirect("/")
    except:
        return "didnt work"

@app.route("/update/<int:id>", methods =['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        print(task.content)
        print(request.form["content"])
        task.content = request.form["content"]
        print(task.content)
        try:
            
            db.session.commit()
            return redirect("/")
        except:
            return "didnt work"
        
    else:
        return render_template("update.html",task=task)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/")
def upload():
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            task.store_img =url_for('download_file', name=filename)
            # return redirect(url_for('download_file', name=filename))
    return render_template("update.html")

@app.route("/static\imgs\<filename>")
def picc():
    return render_template("index.html")

@app.route("/display", methods =['GET','POST'])
def show():
    if request.method=="GET":
        tasks = Todo.query.order_by(Todo.data_created).all()
        return render_template("display.html",tasks=tasks)


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)