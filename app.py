#! C:\Users\edrixxx\OneDrive - Ericsson\Desktop\Projects\CRUDrestAPI\myvenv\Scripts\python.exe


from flask import Flask, appcontext_popped,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///details.db'
db = SQLAlchemy(app)
app.app_context().push()


class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signum = db.Column(db.String(200),unique = True, nullable = False)
    name = db.Column(db.String(200),nullable = False)
    stren = db.Column(db.String(200))
    date_created =  db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Intern %r>' % self.id




@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        signum = request.form['signum']
        name = request.form['name']
        stren = request.form['stren']
        new_detail = Details(signum=signum, name=name, stren=stren)

        try:
            db.session.add(new_detail)
            db.session.commit()
            return redirect('/')
        except:
            return "There was some issue adding the intern details."
        
    else:
        deets = Details.query.order_by(Details.date_created).all()
        return render_template('index.html', deets=deets)
    

@app.route('/delete/<int:id>')
def delete(id):
    det_to_delete = Details.query.get_or_404(id)

    try:
        db.session.delete(det_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return "There was a problem deleting that intern detail."
    
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):

    deets = Details.query.get_or_404(id)

    if request.method =='POST':
        if request.method == 'POST':
            deets.signum = request.form['signum']
            deets.name = request.form['name']
            deets.stren = request.form['stren']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue upating your task."
    else:
        return render_template('update.html',deets=deets)
    


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)