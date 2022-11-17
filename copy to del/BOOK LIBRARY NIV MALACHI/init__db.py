from datetime import date
from book_library import *

member1 = Members(member_name = "or", member_age = 22, member_city = "lod")
member2 = Members(member_name = "alon", member_age = 22, member_city = "kadima")
member3 = Members(member_name = "omer", member_age = 22, member_city = "binyamina")
member4 = Members(member_name = "shir", member_age = 22, member_city = "bat yam")

book1= Books(book_name = "Alice's Adventures in Wonderland", book_author ="Lewis Carroll",publish_date = 1865 ,book_type = 1)
book2= Books(book_name = "The Little Prince", book_author ="Antoine de Saint-Exupéry",publish_date = 1943 ,book_type = 2)
book3= Books(book_name = "The Hunger Games", book_author ="Suzanne Collins",publish_date = 2008 ,book_type = 3)
book4= Books(book_name = "The Lion, the Witch and the Wardrobe", book_author ="C.S.Lewis",publish_date = 1865 ,book_type = 2)


loan1 = Loans(book_id = 1, member_id = 1, loan_date = date(2022,10,19), return_date = date(2022,10,29))
loan2 = Loans(book_id = 2, member_id = 2, loan_date = date(2022,10,20), return_date = date(2022,10,25))
loan3 = Loans(book_id = 3, member_id = 3, loan_date = date(2022,10,25), return_date = date(2022,10,27))
loan4 = Loans(book_id = 4, member_id = 1, loan_date = date(2022,10,19), return_date = date(2022,10,24))
loan5 = Loans(book_id = 2, member_id = 2, loan_date = date(2022,10,22), return_date = date(2022,10,27))

with app.app_context():
    db.session.add_all([member1,member2,member3,member4])
    db.session.add_all([book1,book2,book3,book4])
    db.session.add_all([loan1,loan2,loan3,loan4,loan5])
    db.session.commit()
    
