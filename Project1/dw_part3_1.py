
# coding: utf-8

# In[32]:

import cx_Oracle
from Tkinter import *
import numpy as np
from collections import defaultdict
import scipy.stats as st
import numpy as np

#connecting to oracle
#connection string format 'username/password@server:port/service'
conn_str = 'mgad/GaneshaDM786@aos.acsu.buffalo.edu:1521/aos.buffalo.edu'
#conn_str = 'project1/project1@localhost:1521/xe'
conn = cx_Oracle.connect(conn_str)
c = conn.cursor()

#creating an empty list to hold values that will later be used to populate a drop down list on GUI
disease_name=[]
c.execute('select distinct name from disease') 
for row in c:
    disease_name.append(row[0])



root = Tk() # creates main window by name root

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.title("Part 3 Problem 1")

#setting the main window size
w = 500
h = 300
x = 50
y = 100

#changing the geometry of root
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

toplabel=Label(root, text = "Select the disease name to get the informative genes related to it ",relief=FLAT)
toplabel.config(width=50,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
toplabel.pack()

#declaring a tkinter variable and assigning it the first element of the list created earlier
variable1 = StringVar(root)
variable1.set(disease_name[1]) # default value to be displayed

#apply function on OptionMenu creates a drop down list with values in the list disease_description
o1 = apply(OptionMenu, (root, variable1) + tuple(disease_name))
o1.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
o1.pack()#.pack() function adds the element to the root window



def Go():
    selected1=variable1.get()


    Result_fr = Toplevel(root)
    Result_fr.title("Results")
    #Result_fr.geometry("%dx%d+%d+%d" % (w, h, x, y))

    canvas = Canvas(Result_fr)
    canvas.grid(row=0, column=0, sticky='nswe')

    scroll = Scrollbar(Result_fr, orient=VERTICAL, command=canvas.yview)
    scroll.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=scroll.set)

    result_frame = Frame(canvas)
    #result_frame.geometry("%dx%d+%d+%d" % (w, h, x, y))
    
    
    

    canvas.create_window(0, 0, window=result_frame, anchor='nw')

    # computing correlation for patients with the same disease

    



    query2="""select p.uid1,mf.exp from microarrayfact mf inner join probe p on mf.pb_id = p.pb_id
              where mf.s_id in
              (select p.s_id from PATIENT1 p, DIAGNOSIS di, disease ds
              where p.P_ID=di.P_ID and di.DS_ID=ds.DS_ID
              and ds.NAME =: select1)order by p.uid1
     """.replace('\n',' ')


    query3="""select p.uid1,mf.exp from microarrayfact mf inner join probe p on mf.pb_id = p.pb_id
               where mf.s_id in
              (select p.s_id from PATIENT1 p, DIAGNOSIS di, disease ds
              where p.P_ID=di.P_ID and di.DS_ID=ds.DS_ID
              and ds.NAME <>: select1)order by p.uid1
     """.replace('\n',' ')

    c.execute(query2,select1=selected1)

    dictionary_guid_A={}

    for row in c:
        key=row[0]
        value=row[1]

        try:
            dictionary_guid_A[key].append(value)
        except KeyError:
            dictionary_guid_A[key] = [value]

    c.execute(query3,select1=selected1)

    dictionary_guid_B={}

    for row in c:
        key=row[0]
        value=row[1]

        try:
            dictionary_guid_B[key].append(value)
        except KeyError:
            dictionary_guid_B[key] = [value]



    ttest_pvalues=[]
    informative_gene=[]
    count=0

    

    for key,value in dictionary_guid_A.iteritems():
        #print key
        key1=key
        #key2=list_of_guid_without_ALL[i]
        
            
        #getting microarray expression values for both ALL and not ALL w.r.t to same gene
        mf_values_A=dictionary_guid_A[key1]
        mf_values_B=dictionary_guid_B[key1]
        temp_variable_ttest=st.ttest_ind(mf_values_A, mf_values_B, equal_var = True)
        if(temp_variable_ttest[1] <= 0.01):
            informative_gene.append(key1)
            ttest_pvalues.append(temp_variable_ttest[1])
            count+=1
            
    l1 = Label(result_frame,text="The informative genes are (count = %d)" % (count), relief=FLAT)
    l1.config(width=50,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
    l1.pack(side=TOP)
    
            
    for row in range(0, len(informative_gene)):
        l = Label(result_frame,text='%d' % (informative_gene[row]), relief=FLAT)
        l.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
        l.pack(side=TOP)
        
    del dictionary_guid_A,dictionary_guid_B
    
    result_frame.update_idletasks()

    canvas.configure(scrollregion=(0, 0, result_frame.winfo_width(), result_frame.winfo_height()))
                
    



    #print(informative_gene)









#creates a button with text GO and invokes function Go when the button is clicked     
button = Button(root, text="GO", command=Go)
button.config(width=10,justify=LEFT,anchor=W,borderwidth=10)
button.pack()

#this is like the main function in tkinter which has to be invoked for all the above code to get executed 
root.mainloop()



   
    




# In[ ]:




# In[ ]:



