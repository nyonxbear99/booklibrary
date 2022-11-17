from datetime import datetime,timedelta
from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Library.sqlite3"
app.config["SECRET_KEY"] = "Library"
CORS(app)
db = SQLAlchemy(app)

class Members(db.Model):
    member_id = db.Column("memberID", db.Integer, primary_key = True)
    member_name = db.Column("memberName", db.String(20), nullable = False)
    member_age = db.Column("memberAge", db.Integer, nullable = False)
    member_city = db.Column("memberCity", db.String(20), nullable = False)
    loans = db.relationship("Loans", backref = "Members", lazy = True)

    def __init__(self,member_name,member_age,member_city):
        self.member_name = member_name
        self.member_age = member_age
        self.member_city = member_city


class Books(db.Model):
    book_id = db.Column("BookID", db.Integer, primary_key = True)
    book_name = db.Column("BookName", db.String(40),nullable = False)
    book_author = db.Column("BookAuthor", db.String(40), nullable = False)
    publish_date = db.Column("PublishedDate", db.Integer, nullable = False)
    book_type = db.Column("BookType", db.Integer, nullable = False)
    loans = db.relationship("Loans", backref = "Books", lazy = True)
   

    def __init__(self ,book_name,book_author,publish_date,book_type):
        self.book_name = book_name
        self.book_author = book_author
        self.publish_date = publish_date
        self.book_type = book_type
       
class Loans(db.Model):
    loan_id = db.Column("LoanID",db.Integer, primary_key = True)
    book_id = db.Column("BookID", db.Integer, db.ForeignKey("books.BookID") )
    member_id = db.Column("MemberID", db.Integer, db.ForeignKey("members.memberID"))
    loan_date = db.Column("DateOfLoan",db.Date, nullable = True)
    return_date = db.Column("returnDate", db.Date, nullable = True)
    

    def __init__(self,book_id,member_id,loan_date,return_date):
        self.book_id = book_id
        self.member_id = member_id
        self.loan_date = loan_date
        self.return_date = return_date
        
        
# ---------------------------------------------------------------------------------------------
#functions
#main page
@app.route("/")
def main_page():
    return render_template ("index.html")
    
#-----------------------------------------------------------------------------------------------
#Book functions

#Book main page
@app.route("/all_books")
def Book_main_page():
    all_books = Books.query.all()
    return render_template ("Books.html", all_books = all_books)


#ADD book
@app.route("/add_book/", methods=['GET','POST'])
def add_new_book(): 
    if request.method=='POST':
        request_data = request.form
        book_name = request_data["BookName"]
        book_author = request_data["BookAuthor"]
        publish_date = request_data["PublishedDate"]
        book_type = request_data["BookType"]

        newBook= Books(book_name, book_author, publish_date, book_type)
        db.session.add (newBook)
        db.session.commit()
        return redirect('/all_books') 
    return render_template('add_book.html')
    
# search function
@app.route("/search_book/", methods=['POST'])
def search_book():
    name = request.form["book_name"]
    book = Books.query.filter(Books.book_name==name).first()
    if book is None :
        return redirect('/all_books')
    return render_template('search_book.html', book=book)

# delete function
@app.route("/Books/DELETE/<book_id>", methods=['GET'])
def delete_book(book_id):
    all_books = Books.query.get(book_id)
    if all_books:
        db.session.delete(all_books)
        db.session.commit()
        return render_template ("Books.html", all_books = Books.query.all())

#------------------------------------------------------------------------------------
#member functions

#Member main page
@app.route("/all_member/", methods = ['GET'])
@app.route('/all_member/<member_id>')
def Member_main_page(member_id = -1):
    if int(member_id)== -1:
        all_member =Members.query.all()
        return render_template('members.html', all_member=all_member)
    if int(member_id) > -1:
        selected = Members.query.get(int(member_id))
        return render_template('search_member.html', selected = selected)


#add functions
@app.route("/add_member/", methods = ['GET','POST'])
def add_member(): 
    if request.method== 'POST':
        member_name = request.form['memberName']
        member_age = request.form['memberAge']
        member_city = request.form['memberCity']
        newMember= Members(member_name,member_age,member_city)
        db.session.add (newMember)
        db.session.commit()
        return redirect('/all_member/') 
    return render_template('add_member.html')

# search function
@app.route("/search_member/", methods=['POST'])
def search_member():
    name = request.form["member_name"]
    member = Members.query.filter(Members.member_name==name).first()
    if member is None :
        return redirect('/all_member')
    return redirect(f'/all_member/{member.member_id}')

# delete
@app.route("/member/DELETE/<member_id>", methods=['GET'])
def delete_member(member_id):
    member = Members.query.get(member_id)
    if member:
        db.session.delete(member)
        db.session.commit()
        return redirect('/all_member/') 
    return render_template ("members.html",member =Members.query.all())

#----------------------------------------------------------------------------------------------
#Loan functions

# #Loan main page
@app.route("/all_loans")
def Loans_main_page():
    loans = Loans.query.all()
    return render_template ("all_loans.html", loans = Loans.query.all())

# #add loan
@app.route("/add_loan", methods=['POST', 'GET'])
def add_loan():
    date_of_loan = datetime.utcnow().date()
    for member in Members.query.all():
        if request.method== 'POST':
            if member.member_id==int(request.form.get("member_id")):
                for book in Books.query.filter_by(book_name=request.form.get("book_name")):
                    if book.book_type==1:                     
                        return_date=date_of_loan + timedelta(days=10)
                    elif book.book_type==2:                     
                        return_date=date_of_loan + timedelta(days=5)
                    else:                     
                        return_date=date_of_loan + timedelta(days=2)
                newLoan= Loans(member_id=request.form["member_id"],book_id = book.book_id,loan_date=date_of_loan,return_date=return_date)
                db.session.add(newLoan)
                db.session.commit()
                return redirect('/all_loans')
    return render_template('add_loan.html') 
         
@app.route("/loan/DELETE/<ind>", methods=['DELETE', 'GET'])
def return_book(ind=0):
    if int(ind) > 0:
        loan=Loans.query.get(int(ind))
        db.session.delete(loan)
        db.session.commit()
    return redirect("/all_loans")
    

# #late loans
@app.route("/late_Loans", methods=['GET'])
def lateloansdis():
    lateLoan = []
    loans = Loans.query.all()
    for loan in loans:
        if loan.return_date < datetime.utcnow().date():
            lateLoan.append(loan)
    return render_template("late_Loans.html", lateLoan=lateLoan)

#-----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()
    app.run(debug = True)