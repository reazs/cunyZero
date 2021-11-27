import sqlalchemy

#get the Class and Time given the sudents name 
def getShowInProfile(name):
    db.select([db.columns.Name, db.columns.Class, db.columns.Time]).where(db.columns.Name.in_([name])) 

#get warning amount
def getWarnings(name):
    db.select([db.columns.Name, db.columns.Warnings]).where(db.columns.Name.in_([name])) 

#the students grade page course history
#this will also show up in pop up if teacher looks into student.
def getShowGrades(name):
    db.select([db.columns.Name, db.columns.Class, db.columns.Professor, db.columns.Grade, db.columns.Grade]).where(db.columns.Name.in_([name])) 

#the teacher's class page
def getShowTeacher(prof):
    db.select([db.columns.term, db.columns.Professor, db.columns.Name, db.columns.Term, db.columns.]).where(db.columns.Name.in_([prof]))

#Admin complaint page
def getComplaints():
    db.select([db.columns.Name, db.columns.Complaints, db.columns.Resolved]).where(db.columns.Resolved.in_(['0']))
    
#get the 2* or later reviews for the admin to review
#might need to add resolved columsn to know if review has already been looked into
def getReviews():
    db.select([db.columns.Name, db.columns.Recipient, db.columns.Rating, db.columns.Reviews]).where(db.columns.Rating.in_(['2']))

#check if the student is holding honorolls in the db
def getHonoroll(name):
    db.select([db.columns.Name, db..columns.Honorolls]).where(db.columns.Name.in_([name]))

#register for classes shows this
# this is for classes on the student page
def getClasses(term):
    db.select([db.columns.Term, db.columns.CourseID, db.columns.CourseName, db.columns.Professor]).where(db.columns.Name.in_([term]))


# models we need left
def Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer = db.Column(db.String, nullable=False)
    reviewTo = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)
    
def Warnings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    warnings = db.Column(db.Integer, nullable=False)

def Terms(db.Model):
    term_start = db.Column(db.DateTime, primary_key=True)
    term_end = db.Column(db.DateTime, primary_key=True)

class ReviewForm(FlaskForm):
    ReviewFor = StringField("Review For", validators=[DataRequired()])
    Rating = StringField("Rate 1-10", validators=[DataRequired()])
    review = CKEditorField("Let us know what you think", validators=[DataRequired()])
    submit = SubmitField("Sumbit")
    


#go into review and check average of reviews
#add all of the reviews of the professor if < 2, then give Warnings
def checkReview():
    
    

