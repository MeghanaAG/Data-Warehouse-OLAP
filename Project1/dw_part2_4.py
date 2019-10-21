
# coding: utf-8

# In[13]:

import cx_Oracle
from Tkinter import *
import numpy as np
import scipy.stats as st

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
    disease_description.append(row[0])
    
go_id=[]
c.execute('select distinct go_id from gene_go_cluster where go_id not like \'null\' order by go_id') 
for row in c:
    go_id.append(row[0])
    
root = Tk() # creates main window by name root

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.title("Part 2 Problem 4")

#setting the main window size
w = 500
h = 300
x = 50
y = 100

#changing the geometry of root
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

toplabel=Label(root, text = "Select Disease and Go id from the drop downs below ",relief=FLAT)
toplabel.config(width=50,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
toplabel.pack()

#declaring a tkinter variable and assigning it the first element of the list created earlier
variable1 = StringVar(root)
variable1.set(disease_description[1]) # default value to be displayed

#apply function on OptionMenu creates a drop down list with values in the list disease_description
o1 = apply(OptionMenu, (root, variable1) + tuple(disease_description))
o1.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
o1.pack()#.pack() function adds the element to the root window

variable2 = StringVar(root)
variable2.set(go_id[0]) # default value

#apply function on OptionMenu creates a drop down list with values in the list disease_type
o2 = apply(OptionMenu, (root, variable2) + tuple(go_id))
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
    
    #Placing the result frame inside the region of canvas which can be scrolled
    canvas.create_window(0, 0, window=result_frame, anchor='nw')
    query1="""select mf.exp from microarrayfact mf
              where mf.pb_id in (select pb_id from probe pb where uid1 in 
              (select uid1 from gene_go_cluster where go_id =: select2))
              and mf.s_id in(select s_id from patient1 where p_id in 
              (select p_id from diagnosis where ds_id in (select ds_id from disease where name =: select1)))
    """.replace('\n',' ')
    c.execute(query1, select1=selected1,select2=selected2)
    
    list_mf_ALL=[]

    for row in c:
        list_mf_ALL.append(row[0])
    query2="""select mf.exp from microarrayfact mf
              where mf.pb_id in (select pb_id from probe pb where uid1 in 
              (select uid1 from gene_go_cluster where go_id =: select2))
              and mf.s_id in(select s_id from patient1 where p_id in 
              (select p_id from diagnosis where ds_id in (select ds_id from disease where name <>: select1)))
    """.replace('\n',' ')
    c.execute(query2, select1=selected1,select2=selected2)
    
    list_mf_notALL=[]

    for row in c:
        list_mf_notALL.append(row[0])
        
    #perform t-test 
    ttestresult=st.ttest_ind(list_mf_ALL,list_mf_notALL,equal_var=True)
    
    l = Label(result_frame,text="T-statistic value is %f with p-value %f" % (ttestresult[0],ttestresult[1]), relief=FLAT)
    l.config(width=70,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 11))
    l.pack(side=TOP)
        
        
    
    
    
    #Label(result_frame, text="Number of rows returned for this query: %s"%(stringval)).pack()
        
#creates a button with text GO and invokes function Go when the button is clicked     
button = Button(root, text="GO", command=Go)
button.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
button.pack()

#this is like the main function in tkinter which has to be invoked for all the above code to get executed 
mainloop()


# In[ ]:




# In[ ]:



