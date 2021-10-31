# functions we need

#adds a warning to student or prof. ( db : students + profs names, warning#)
# +1 warning to warning# under given name
def addWarning(f_name, l_name):

#6 funds
#warn professor if not their students have been given grade after semester.
#pull up class for prof this term, see if any missing grades. (check end of term db)
def warnProfGrades():

#get GPA of whole class for this term
#check GPA >3.5 or GPA <2.5 give warning + 1.
def warnProfGrading():
    addWarning(f_name, l_name)

#check if student has F 2 times in same course then
#check if student has lower than 2.0 GPA. (get all of users grades / amt)
#tour to terminated page or suspension.
def terminateStudent():

#check if student has F 2 times in same course name
#check if student has GPA between 2 & 2.25
#tell student to go meet with registrar on personal homepage
def warnSafeStudent():

#check if student GPA above 3.75 this term
#check if student GPA above 3.5 for all classes
#either true honorRollStudent on personal homepage && -1 warning
def honorRollStudent():


#7
#route student to suspend page if warnings = 3 when user logs in (for pref & students)
def suspensionPage(f_name, l_name):

#if writer = prof /and recipient = student /and registrar = punish then
#give student W or suspension
def deregister(f_name,l_name):

#8
#when the prof presses button run this to get student’s info from db (course / prof / grade )
def getStudentsAcademics(f_name,l_name):

#One time tutorial for new students.(db = tutorial column, 0 = new 1 = done)
#run if tutorial = 0, if tutotial = 1 then dont
def tutorial():

#9
# 1.
#if the semester has started and student drop then W grade.
def withrawal():

#get student’s name and see current classes, if all grades = W (suspend if all classes dropped)
def suspension():

#etc
#set the start and end of the term (insert into db)
def termDuration(start,end):
