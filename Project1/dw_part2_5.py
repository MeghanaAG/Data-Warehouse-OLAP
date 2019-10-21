
# coding: utf-8

# In[28]:

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
c.execute('select distinct name from disease order by name') 
for row in c:
    disease_description.append(row[0])
    
cluster_id=[]
c.execute('select distinct go_id from gene_go_cluster where go_id not like \'null\' order by go_id') 
for row in c:
    cluster_id.append(row[0])
    
root = Tk() # creates main window by name root

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.title("Part 2 Problem 5")

#setting the main window size
w = 500
h = 300
x = 50
y = 100

#changing the geometry of root
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

toplabel=Label(root, text = "Select Disease and Go_id from the drop downs below ",relief=FLAT)
toplabel.config(width=50,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
toplabel.pack()

#declaring a tkinter variable and assigning it the first element of the list created earlier
variable1 = IntVar(root)
#variable1.set(disease_description[0]) # default value to be displayed


variable2 = IntVar(root)
#variable2.set(disease_description[1]) # default value to be displayed


variable3 = IntVar(root)
#variable3.set(disease_description[2]) # default value to be displayed


variable4 = IntVar(root)
#variable4.set(disease_description[3]) # default value to be displayed


variable5 = IntVar(root)
#variable5.set(disease_description[4]) # default value

variable6 = IntVar(root)
#variable6.set(disease_description[5])

c1 = Checkbutton(root, text="ALL", variable=variable1)
c1.config(width=30,justify=LEFT,font=('bold', 10))
c1.pack(side=TOP)


c2 = Checkbutton(root, text="AML", variable=variable2)
c2.config(width=30,justify=LEFT,font=('bold', 10))
c2.pack(side=TOP)

c3 = Checkbutton(root, text="Breast Tumor", variable=variable3)
c3.config(width=30,justify=LEFT,font=('bold', 10))
c3.pack(side=TOP)

c4 = Checkbutton(root, text="Colon Tumor", variable=variable4)
c4.config(width=30,justify=LEFT,font=('bold', 10))
c4.pack(side=TOP)

c5 = Checkbutton(root, text="Flu", variable=variable5)
c5.config(width=30,justify=LEFT,font=('bold', 10))
c5.pack(side=TOP)

c6 = Checkbutton(root, text="Giloblastome", variable=variable6)
c6.config(width=30,justify=LEFT,font=('bold', 10))
c6.pack(side=TOP)

variable7 = StringVar(root)
variable7.set(cluster_id[0])



#apply function on OptionMenu creates a drop down list with values in the list disease_type
o5 = apply(OptionMenu, (root, variable7) + tuple(cluster_id))
o5.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
o5.pack()




def Go():
    
    selected1=variable1.get()
    selected2=variable2.get()
    selected3=variable3.get()
    selected4=variable4.get()
    selected5=variable5.get()
    selected6=variable6.get()
    selected7=variable7.get()
    
    #print selected1,selected2,selected3,selected4,selected5,selected6
    
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
    
    ftestvalue=[]
    
    
    ftest='ftestvalue=st.f_oneway('
    
    
    
    if(selected1==1):
        query1="select mf.exp from microarrayfact mf where mf.pb_id in (select pb_id from probe pb where uid1 in(select uid1 from gene_go_cluster where go_id =:select_goid))and mf.s_id in (select s_id from patient1 where p_id in(select p_id from diagnosis where ds_id in(select ds_id from disease where name like 'ALL')))"
        c.execute(query1,select_goid=selected7)
        
        list_mf_ALL=[]

        for row in c:
            list_mf_ALL.append(row[0])
            
        ftest=ftest+"list_mf_ALL,"
        
        #print ftest
            
    if(selected2==1):
        query1="select mf.exp from microarrayfact mf where mf.pb_id in (select pb_id from probe pb where uid1 in(select uid1 from gene_go_cluster where go_id =:select_goid))and mf.s_id in (select s_id from patient1 where p_id in(select p_id from diagnosis where ds_id in(select ds_id from disease where name like 'AML')))"
        c.execute(query1,select_goid=selected7)
        
        list_mf_AML=[]

        for row in c:
            list_mf_AML.append(row[0])
        ftest=ftest+"list_mf_AML,"
        
        #print ftest
            
            
    if(selected3==1):
        query1="select mf.exp from microarrayfact mf where mf.pb_id in (select pb_id from probe pb where uid1 in(select uid1 from gene_go_cluster where go_id =:select_goid))and mf.s_id in (select s_id from patient1 where p_id in(select p_id from diagnosis where ds_id in(select ds_id from disease where name like 'Breast tumor')))"
        c.execute(query1,select_goid=selected7)
        
        list_mf_BT=[]

        for row in c:
            list_mf_BT.append(row[0])
        ftest=ftest+"list_mf_BT,"
        
        #print ftest
            
    if(selected4==1):
        query1="select mf.exp from microarrayfact mf where mf.pb_id in (select pb_id from probe pb where uid1 in(select uid1 from gene_go_cluster where go_id =:select_goid))and mf.s_id in (select s_id from patient1 where p_id in(select p_id from diagnosis where ds_id in(select ds_id from disease where name like 'Colon tumor')))"
        c.execute(query1,select_goid=selected7)
        
        list_mf_CT=[]

        for row in c:
            list_mf_CT.append(row[0])
            
        ftest=ftest+"list_mf_CT,"
        
        #print ftest
            
    if(selected5==1):
        query1="select mf.exp from microarrayfact mf where mf.pb_id in (select pb_id from probe pb where uid1 in(select uid1 from gene_go_cluster where go_id =:select_goid))and mf.s_id in (select s_id from patient1 where p_id in(select p_id from diagnosis where ds_id in(select ds_id from disease where name like 'Flu')))"
        c.execute(query1,select_goid=selected7)
        
        list_mf_Flu=[]

        for row in c:
            list_mf_Flu.append(row[0])
        ftest=ftest+"list_mf_Flu,"
        
            
    if(selected6==1):
        query1="select mf.exp from microarrayfact mf where mf.pb_id in (select pb_id from probe pb where uid1 in(select uid1 from gene_go_cluster where go_id =:select_goid))and mf.s_id in (select s_id from patient1 where p_id in(select p_id from diagnosis where ds_id in(select ds_id from disease where name like 'Giloblastome')))"
        c.execute(query1,select_goid=selected7)
        
        list_mf_Gb=[]

        for row in c:
            list_mf_Gb.append(row[0])
        ftest=ftest+"list_mf_Gb,"
        
    #print ftest
    ftest=ftest[0:len(ftest)-1]
   
    ftest=ftest+')'

    exec(ftest)
    
    
    
    
            
    l = Label(result_frame,text="F-statistic is %f with p-value %f" % (ftestvalue[0],ftestvalue[1]), relief=FLAT)
    l.config(width=50,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
    l.pack(side=TOP)
            

            
        
    
    
        
#creates a button with text GO and invokes function Go when the button is clicked     
button = Button(root, text="GO", command=Go)
button.config(width=10,justify=LEFT,anchor=W,borderwidth=10)
button.pack()

#this is like the main function in tkinter which has to be invoked for all the above code to get executed 
mainloop()


# In[ ]:




# In[ ]:




# In[ ]:



