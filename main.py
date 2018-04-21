from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:launchcode@localhost:8889/Blogz'
db = SQLAlchemy(app)
app.secret_key = 'supersecretkey'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def not_empty(self):
        if self.title and self.body:
            return True
        else:
            return False

@app.route('/')
def index():
    return redirect('/blog')

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
    if request.method == 'POST':
        entry_title = request.form['title']
        entry_content = request.form['content']
        new_entry = Blog(entry_title, entry_content)

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