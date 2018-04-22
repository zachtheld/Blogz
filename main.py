from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:launchcode@localhost:8889/Blogz'
db = SQLAlchemy(app)
app.secret_key = 'supersecretkey'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

    def not_empty(self):
        if self.title and self.body:
            return True
        else:
            return False

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Logged In!')
            return redirect('/newpost')
        else:
            flash('User does not exist or password does not match')
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        # validate username, password and verify
        if len(username) <= 2 or len(password) <= 2:
            flash('Username and Password length must be greater than three characters')
        elif verify != password:
            flash('Verify password must match password')
        elif ' ' in username or ' ' in password:
            flash('Username and Passwords cannot contain spaces')
        elif not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('User already exists')

    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')


@app.route('/blog', methods=['POST', 'GET'])
def blogs():
    entry_id = request.args.get('id')
    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template('single_entry.html', entry=entry)

    blog_entry = Blog.query.all()
    return render_template('blog_entrys.html', entries=blog_entry)

@app.route('/newpost', methods=['POST', 'GET'])
def add_new_entry():
    owner = User.query.filter_by(username=session['username'])

    if request.method == 'POST':
        entry_title = request.form['title']
        entry_content = request.form['content']
        owner = User.query.filter_by(username=session['username']).first()
        new_entry = Blog(entry_title, entry_content, owner)

        if new_entry.not_empty():
            db.session.add(new_entry)
            db.session.commit()
            entry_url = '/blog?id=' + str(new_entry.id)
            return redirect(entry_url)
        else:
            flash('Title and Entry Content are required to make a post')
            return redirect('/newpost')
    
    else:
        return render_template('add_entry.html')







if __name__=='__main__':
    app.run()