from flask_sqlalchemy import SQLAlchemy
from flask import *
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
#from flask.ext.session import Session
#from app import app
app = Flask(__name__)
app.secret_key = "manoj"
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root@localhost/book'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


class Book_list(db.Model):
    __tablename__ = "book_list"
    book_num = db.Column(db.Integer , primary_key = True , nullable=False)
    isbn = db.Column(db.Integer)
    title = db.Column(db.String)
    author = db.Column(db.String)
    year = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True , nullable=False)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    
class Book_review(db.Model):
    __tablename__ = "book_review"
    rev_id = db.Column(db.Integer, primary_key=True, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey(
        "book_list.book_num"), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    review = db.Column(db.Text)


@app.route('/')
def index():
    session.pop('email', None)
    return render_template("books_signin.html")


@app.route('/signup_page')
def signup_page():
    return render_template("books_signup.html")


@app.route('/signup' , methods = ['POST'])
def signup():
    session.pop('email' , None)
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('pass')
    print(name , email , password)
    em = User.query.filter_by(email=email).all()
    print(em)
    if em != []:
        return render_template("books_signin.html" , message = "Account already exists. Please sign in")
    else:
        insert = User(name = name , email = email , password = password)
        db.session.add(insert)
        db.session.commit()
        return render_template("books_signin.html" , message = "Account created please sign in ")
    



@app.route('/signin' , methods = ['POST'])
def signin():
    getemail = request.form.get('email')
    password = request.form.get('pass')
    res = User.query.filter(User.email == getemail).filter(User.password == password).all()
    if not res:
        return render_template("books_signin.html" , message = "Wrong Email-ID or Password")
    else:
        session['email'] = getemail
        nm = User.query.filter(User.email == getemail).first()
        print(nm)
        text = " "
        return redirect(url_for('booksearch' , comment = text)) 

@app.route('/booksearch/<string:comment>')
def booksearch(comment):
    n1 = User.query.filter(User.email == session['email']).first()
    return render_template("book_home.html" , username = n1 , message = comment )

@app.route('/search' , methods = ['POST'])
def search():
    if request.method == 'POST':
        name = request.form.get('res')
        nm = User.query.filter(User.email == session['email']).first()
        #print(name)
        result = Book_list.query.filter(db.or_(Book_list.author==name , Book_list.isbn==name , Book_list.title==name)).all()
        if result == []:
            return render_template("book_home.html" , username = nm , message = " No such book found")
        else:
            num = []
            bookrev = []
            for r in result:
                n = str(r)
                x = int(n[n.find(" "):len(n)-1])
                num.append(x)
            for n in num:
                com = Book_review.query.filter(Book_review.book_id == n).all()
                if com != []:
                    bookrev.append(com)
                
            print(bookrev)
            return render_template("books_details.html" , username = nm , data = result , comments = bookrev)

@app.route('/review/<int:booknum>/<int:userid>' , methods = ['POST'])
def review(booknum ,userid):
    print(booknum)
    print(userid)
    id = "comment"+str(booknum)
    com = request.form.get(id)
    print(com)
    getid = Book_review.query.filter(Book_review.userid == userid).filter(Book_review.book_id == booknum).all()
    if getid == []:
        addComment = Book_review(book_id = booknum , userid = userid , review = com)
        db.session.add(addComment)
        db.session.commit()
        text = "Comment Added! Thank You "
        return redirect(url_for('booksearch' , comment = text ))
    else:
        text = "You have already commented on this book"
        return redirect(url_for('booksearch', comment =text))
   
    

@app.route('/logout')
def logout():
    session.pop('email' , None)
    print("Logged out  ")
    return render_template("books_signin.html")

if __name__ == "__main__":
    app.run(debug=True)
