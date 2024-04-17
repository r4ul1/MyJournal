from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///diary.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Note {self.id}: {self.title}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        
        new_note = Note(title=new_title, content=new_content)
        
        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your note'
    else:
        notes = Note.query.order_by(Note.date_created.desc()).all()
        return render_template('index.html', notes=notes)

@app.route('/view/<int:id>')
def view(id):
    note = Note.query.get_or_404(id)
    return render_template('view.html', note=note)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    note = Note.query.get_or_404(id)
    
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the note'
    else:
        return render_template('update.html', note=note)

@app.route('/delete/<int:id>')
def delete(id):
    note_to_delete = Note.query.get_or_404(id)
    
    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the note'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
    