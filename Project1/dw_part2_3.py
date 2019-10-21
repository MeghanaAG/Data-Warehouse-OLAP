
# coding: utf-8

# In[7]:

import cx_Oracle
from Tkinter import *
import numpy as np
#connecting to oracle
#connection string format 'username/password@server:port/service'
conn_str = 'mgad/GaneshaDM786@aos.acsu.buffalo.edu:1521/aos.buffalo.edu'
#conn_str = 'project1/project1@localhost:1521/xe'
conn = cx_Oracle.connect(conn_str)
c = conn.cursor()

#creating an empty list to hold values that will later be used to populate a drop down list on GUI
disease_description=[]
c.execute('select distinct name from disease') 
for row in c:
    disease_description.append(row[1])
    
cluster_id=[]
c.execute('select distinct cl_id from gene_go_cluster where cl_id not like \'null\' order by cl_id') 
for row in c:
    cluster_id.append(row[0])
    
root = Tk() # creates main window by name root

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.title("Part 2 problem 3")

#setting the main window size
w = 500
h = 300
x = 50
y = 100

#changing the geometry of root
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

toplabel=Label(root, text = "Select disease and cluster_id from the drop downs below ",relief=FLAT)
toplabel.config(width=50,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
toplabel.pack()

#declaring a tkinter variable and assigning it the first element of the list created earlier
variable1 = StringVar(root)
variable1.set(disease_description[0]) # default value to be displayed

#apply function on OptionMenu creates a drop down list with values in the list disease_description
o1 = apply(OptionMenu, (root, variable1) + tuple(disease_description))
o1.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
o1.pack()#.pack() function adds the element to the root window

variable2 = StringVar(root)
variable2.set(cluster_id[0]) # default value

#apply function on OptionMenu creates a drop down list with values in the list disease_type
o2 = apply(OptionMenu, (root, variable2) + tuple(cluster_id))
o2.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
o2.pack()


def Go():
    selected1=variable1.get()
    selected2=variable2.get()
    
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
    toplabel=Label(result_frame, text = "mRNA values are(Results with measurement unit id = 001)",relief=FLAT)
    toplabel.config(width=50,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
    toplabel.pack()
    #Placing the result frame inside the region of canvas which can be scrolled
    canvas.create_window(0, 0, window=result_frame, anchor='nw')
    query="select exp from MICROARRAYFACT where  s_id in (select distinct s_id from clinical_fact where p_id in (select distinct p_id from clinical_fact join disease on  clinical_fact.ds_id like disease.ds_id where disease.name =: sel1)) and pb_id in(select pb_id from probe where UID1 in (select UID1 from genefact where cl_id =: sel2)) and mu_id = 001"
    c.execute(query, sel1=selected1,sel2=selected2)
    for row_number, row in enumerate(c):
        l = Label(result_frame,text='%d.     %d' % (row_number+1, row[0]), relief=FLAT)
        l.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
        l.pack(side=TOP)
    result_frame.update_idletasks()

    canvas.configure(scrollregion=(0, 0, result_frame.winfo_width(), result_frame.winfo_height()))
    #Label(result_frame, text="Number of rows returned for this query: %s"%(stringval)).pack()
        
#creates a button with text GO and invokes function Go when the button is clicked     
button = Button(root, text="GO", command=Go)
button.config(width=10,justify=LEFT,anchor=W,borderwidth=10)
button.pack()

#this is like the main function in tkinter which has to be invoked for all the above code to get executed 
mainloop()


# In[ ]:




# In[ ]:



