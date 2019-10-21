import cx_Oracle
from Tkinter import *
#connecting to oracle
#connection string format 'username/password@server:port/service'
conn_str = 'mgad/GaneshaDM786@aos.acsu.buffalo.edu:1521/aos.buffalo.edu'
#conn_str = 'project1/project1@localhost:1521/xe'
conn = cx_Oracle.connect(conn_str)
c = conn.cursor()

#creating an empty list to hold values that will later be used to populate a drop down list on GUI
disease_description=[]
c.execute('select distinct description from disease') 
for row in c:
    disease_description.append(row[0])
    
#disease type drop down list options
disease_type=[]
c.execute('select distinct type from disease') 
for row in c:
    disease_type.append(row[0])

#disease name drop down list options
disease_name=[]
c.execute('select distinct name from disease') 
for row in c:
    disease_name.append(row[0])
    

root = Tk() # creates main window by name root

#setting the main window size
w = 800
h = 300
x = 50
y = 100

#changing the geometry of root
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

root.title("Part 2 Problem 1")

toplabel=Label(root, text = "Select the disease description, type and name from the drop downs below ",relief=FLAT)
toplabel.config(width=60,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
toplabel.pack()

#declaring a tkinter variable and assigning it the first element of the list created earlier
variable1 = StringVar(root)
variable1.set(disease_description[0]) # default value to be displayed

#apply function on OptionMenu creates a drop down list with values in the list disease_description
o1 = apply(OptionMenu, (root, variable1) + tuple(disease_description))
o1.config(width=15,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
o1.pack()#.pack() function adds the element to the root window

variable2 = StringVar(root)
variable2.set(disease_type[0]) # default value

#apply function on OptionMenu creates a drop down list with values in the list disease_type
o2 = apply(OptionMenu, (root, variable2) + tuple(disease_type))
o2.config(width=15,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
o2.pack()

variable3 = StringVar(root)
variable3.set(disease_name[0]) # default value

o3 = apply(OptionMenu, (root, variable3) + tuple(disease_name))
o3.config(width=15,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
o3.pack()

#function that gets executed when Go button on 
def Go():
    selected1=variable1.get()
    selected2=variable2.get()
    selected3=variable3.get()
    print selected1
    result_frame = Toplevel(root)
    result_frame.title("Results")
    result_frame.geometry("%dx%d+%d+%d" % (w, h, x, y))
    query="select count(p_id) from clinical_fact join disease on  clinical_fact.ds_id like disease.ds_id where disease.DESCRIPTION =:selected"
    c.execute(query, selected=selected1)
    for row_number, row in enumerate(c):
        Label(result_frame, text = "Number of patients with %s : "%(selected1) + str(row[0]),font=('bold', 12)).pack()
    query="select count(p_id) from clinical_fact join disease on  clinical_fact.ds_id like disease.ds_id where disease.TYPE =:selected"
    c.execute(query, selected=selected2)
    for row_number, row in enumerate(c):
        Label(result_frame, text = "Number of patients with %s : "%(selected2) + str(row[0]),font=('bold', 12)).pack()
    query="select count(p_id) from clinical_fact join disease on  clinical_fact.ds_id like disease.ds_id where disease.NAME =:selected"
    c.execute(query, selected=selected3)
    for row_number, row in enumerate(c):
        Label(result_frame, text = "Number of patients with %s : "%(selected3) + str(row[0]),font=('bold', 12)).pack()
    

#creates a button with text GO and invokes function Go when the button is clicked     
button = Button(root, text="GO", command=Go)
button.config(width=15,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
button.pack()

#this is like the main function in tkinter which has to be invoked for all the above code to get executed 
mainloop()


