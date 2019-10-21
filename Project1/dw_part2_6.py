
# coding: utf-8

# In[3]:

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

go_id=[]
c.execute('select distinct go_id from gene_go_cluster where cl_id not like \'null\' order by go_id') 
for row in c:
    go_id.append(row[0])

root = Tk() # creates main window by name root

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.title("Part 2 Problem 6")

#setting the main window size
w = 800
h = 300
x = 50
y = 100

#changing the geometry of root
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

toplabel=Label(root, text = "Select two disease names and go_id from the drop downs below ",relief=FLAT)
toplabel.config(width=50,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
toplabel.pack()

#declaring a tkinter variable and assigning it the first element of the list created earlier
variable1 = StringVar(root)
variable1.set(disease_name[1]) # default value to be displayed

#apply function on OptionMenu creates a drop down list with values in the list disease_description
o1 = apply(OptionMenu, (root, variable1) + tuple(disease_name))
o1.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
o1.pack()#.pack() function adds the element to the root window

variable2 = StringVar(root)
variable2.set(disease_name[1]) # default value

#apply function on OptionMenu creates a drop down list with values in the list disease_type
o2 = apply(OptionMenu, (root, variable2) + tuple(disease_name))
o2.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
o2.pack()

variable3 = StringVar(root)
variable3.set(go_id[0]) # default value

#apply function on OptionMenu creates a drop down list with values in the list disease_type
o3 = apply(OptionMenu, (root, variable3) + tuple(go_id))
o3.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 10))
o3.pack()

def Go():
    selected1=variable1.get()
    selected2=variable2.get()
    selected3=variable3.get()

    Result_fr = Toplevel(root)
    Result_fr.title("Results")


    canvas = Canvas(Result_fr)
    canvas.grid(row=0, column=0, sticky='nswe')

    scroll = Scrollbar(Result_fr, orient=VERTICAL, command=canvas.yview)
    scroll.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=scroll.set)

    result_frame = Frame(canvas)

    canvas.create_window(0, 0, window=result_frame, anchor='nw')

    # computing correlation for patients with the same disease
    if(selected1 == selected2 ):
        query="""select distinct p_id from(select p.p_id, ma.exp from MICROARRAYFACT ma, PATIENT1 p where p.S_ID = ma.S_ID
                 and ma.PB_ID in (select pb_id from Probe pr, GENE_GO_CLUSTER gcc
                 where pr.UID1 = gcc.UID1 and gcc.GO_ID =: select3)
                 and p.P_ID in (select p_id from DIAGNOSIS di, DISEASE ds where di.DS_ID = ds.DS_ID and ds.NAME =: select1)
                 order by p.p_id, ma.PB_ID)
                 """.replace('\n',' ')
        c.execute(query,select3=selected3,select1=selected1)

        list_of_pid=[]

        for row in c:
            list_of_pid.append(row[0])


        dictionary_pid_exp={}



        query1="""select p.p_id, ma.exp from MICROARRAYFACT ma, PATIENT1 p where p.S_ID = ma.S_ID
                  and ma.PB_ID in (select pb_id from Probe pr, GENE_GO_CLUSTER gcc
                  where pr.UID1 = gcc.UID1 and gcc.GO_ID =: select3)
                  and p.P_ID in (select p_id from DIAGNOSIS di, DISEASE ds where di.DS_ID = ds.DS_ID and ds.NAME =: select1)
                  order by p.p_id, ma.PB_ID
                 """.replace('\n',' ')
        c.execute(query1,select3=selected3,select1=selected1)

        for row in c:
            key=row[0]
            value=row[1]

            try:
                dictionary_pid_exp[key].append(value)
            except KeyError:
                dictionary_pid_exp[key] = [value]

        #for keys,values in dictionary_pid_exp.items():
          #  print keys,values

        correlations=[]

        print "break"

        for i in range(0,len(list_of_pid)):
            #print i
            key1=list_of_pid[i]
            values=dictionary_pid_exp[key1]
            for j in range(i+1,len(list_of_pid)):
                key2=list_of_pid[j]
                values2=dictionary_pid_exp[key2]
                #print key1,key2
                #print values
                #print values2
                #cr=st.pearsonr(values,values2)
                cr=st.pearsonr(values,values2)
                #print cr[0],cr[1]
                correlations.append(cr[0])

        #print correlations        
        average_correlation= np.mean(correlations)

        l = Label(result_frame,text="the average correlation is %f" % (average_correlation), relief=FLAT)
        l.config(width=40,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 11))
        l.pack(side=TOP)

        #deleting the dictionary so that a new dictionary will be created when a new query is run
        del dictionary_pid_exp

    else:
        #creating two list of p_id, first list contains p_id of patients with disease nd the second one contains the p_id of patients with disease 2
        query="""select distinct p_id from(select p.p_id, ma.exp from MICROARRAYFACT ma, PATIENT1 p where p.S_ID = ma.S_ID
                 and ma.PB_ID in (select pb_id from Probe pr, GENE_GO_CLUSTER gcc
                 where pr.UID1 = gcc.UID1 and gcc.GO_ID =: select3)
                 and p.P_ID in (select p_id from DIAGNOSIS di, DISEASE ds where di.DS_ID = ds.DS_ID and ds.NAME =: select1)
                 order by p.p_id, ma.PB_ID)
                 """.replace('\n',' ')
        c.execute(query,select3=selected3,select1=selected1)

        list_of_pid_with_1=[]

        for row in c:
            list_of_pid_with_1.append(row[0])

        query="""select distinct p_id from(select p.p_id, ma.exp from MICROARRAYFACT ma, PATIENT1 p where p.S_ID = ma.S_ID
                 and ma.PB_ID in (select pb_id from Probe pr, GENE_GO_CLUSTER gcc
                 where pr.UID1 = gcc.UID1 and gcc.GO_ID =: select3)
                 and p.P_ID in (select p_id from DIAGNOSIS di, DISEASE ds where di.DS_ID = ds.DS_ID and ds.NAME =: select1)
                 order by p.p_id, ma.PB_ID)
                 """.replace('\n',' ')
        c.execute(query,select3=selected3,select1=selected2)

        list_of_pid_with_2=[]

        for row in c:
            list_of_pid_with_2.append(row[0])


        #creating dictionary for group1 
        dictionary_pid_exp_1={}



        query1="""select p.p_id, ma.exp from MICROARRAYFACT ma, PATIENT1 p where p.S_ID = ma.S_ID
                  and ma.PB_ID in (select pb_id from Probe pr, GENE_GO_CLUSTER gcc
                  where pr.UID1 = gcc.UID1 and gcc.GO_ID =: select3)
                  and p.P_ID in (select p_id from DIAGNOSIS di, DISEASE ds where di.DS_ID = ds.DS_ID and ds.NAME =: select1)
                  order by p.p_id, ma.PB_ID
                 """.replace('\n',' ')
        c.execute(query1,select3=selected3,select1=selected1)

        for row in c:
            key=row[0]
            value=row[1]

            try:
                dictionary_pid_exp_1[key].append(value)
            except KeyError:
                dictionary_pid_exp_1[key] = [value]


        #creating dictionary for group2 
        dictionary_pid_exp_2={}



        query1="""select p.p_id, ma.exp from MICROARRAYFACT ma, PATIENT1 p where p.S_ID = ma.S_ID
                  and ma.PB_ID in (select pb_id from Probe pr, GENE_GO_CLUSTER gcc
                  where pr.UID1 = gcc.UID1 and gcc.GO_ID =: select3)
                  and p.P_ID in (select p_id from DIAGNOSIS di, DISEASE ds where di.DS_ID = ds.DS_ID and ds.NAME =: select1)
                  order by p.p_id, ma.PB_ID
                 """.replace('\n',' ')
        c.execute(query1,select3=selected3,select1=selected2)

        for row in c:
            key=row[0]
            value=row[1]

            try:
                dictionary_pid_exp_2[key].append(value)
            except KeyError:
                dictionary_pid_exp_2[key] = [value]

        #for keys,values in dictionary_pid_exp_2.items():
           # print keys,values

        correlations_1_2=[]
        ncorrelations_1_2=[]

        print "break"

        for i in range(0,len(list_of_pid_with_1)):
            #print i
            key1=list_of_pid_with_1[i]
            values=dictionary_pid_exp_1[key1]
            for j in range(0,len(list_of_pid_with_2)):
                key2=list_of_pid_with_2[j]
                values2=dictionary_pid_exp_2[key2]
                #print key1,key2
                #print values
                #print values2
                npcr=np.corrcoef(values,values2)
                cr=st.pearsonr(values,values2)
                #print npcr
                correlations_1_2.append(cr[0])
                ncorrelations_1_2.append(npcr[0,1])

        #print correlations_1_2        
        average_correlation= np.mean(correlations_1_2)
        naverage_correlation= np.mean(ncorrelations_1_2)

        print average_correlation
        print naverage_correlation

        l = Label(result_frame,text="the average correlation is %f" % (average_correlation), relief=FLAT)
        l.config(width=70,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 11))
        l.pack(side=TOP)

        del dictionary_pid_exp_1,dictionary_pid_exp_2






#creates a button with text GO and invokes function Go when the button is clicked     
button = Button(root, text="GO", command=Go)
button.config(width=10,justify=LEFT,anchor=W,borderwidth=10)
button.pack()

#this is like the main function in tkinter which has to be invoked for all the above code to get executed 
root.mainloop()



   
    




# In[ ]:




# In[ ]:



