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

root.title("Part 2 Problem 2")

toplabel=Label(root, text = "Select the disease description from the drop down below ",relief=FLAT)
toplabel.config(width=60,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
toplabel.pack()

#declaring a tkinter variable and assigning it the first element of the list created earlier
variable1 = StringVar(root)
variable1.set(disease_description[0]) # default value to be displayed

#apply function on OptionMenu creates a drop down list with values in the list disease_description
o1 = apply(OptionMenu, (root, variable1) + tuple(disease_description))
o1.config(width=15,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
o1.pack()#.pack() function adds the element to the root window



#function that gets executed when Go button on 
def Go():
    selected1=variable1.get()

    Result_fr = Toplevel(root)
    Result_fr.title("Results")

    canvas = Canvas(Result_fr)
    canvas.grid(row=0, column=0, sticky='nswe')
    #add a scroll bar to the canvas
    scroll = Scrollbar(Result_fr, orient=VERTICAL, command=canvas.yview)
    scroll.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=scroll.set)
    
    #adding result frame to canvas
    result_frame = Frame(canvas)
    canvas.create_window(0, 0, window=result_frame, anchor='nw')
    query="select distinct type from drug where DR_ID in (select distinct dr_id from clinical_fact join disease on  clinical_fact.ds_id like disease.ds_id where disease.DESCRIPTION =:selected)"
    c.execute(query, selected=selected1)
    toplabel1=Label(result_frame, text = "Types of Drugs applied are",relief=FLAT)
    toplabel1.config(width=60,justify=LEFT,anchor=W,borderwidth=10)
    toplabel1.pack()
    for row_number, row in enumerate(c):
        l1=Label(result_frame, text =  str(row[0]))
        l1.config(width=60,justify=LEFT,anchor=W,borderwidth=10)
        l1.pack(side=TOP)
    result_frame.update_idletasks()

    canvas.configure(scrollregion=(0, 0, result_frame.winfo_width(), result_frame.winfo_height()))
    

#creates a button with text GO and invokes function Go when the button is clicked     
button = Button(root, text="GO", command=Go)
#button.config(width=15,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))

button.pack()


#this is like the main function in tkinter which has to be invoked for all the above code to get executed 
mainloop()
