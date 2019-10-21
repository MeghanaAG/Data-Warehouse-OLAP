import cx_Oracle
from Tkinter import *
import numpy as np
from collections import defaultdict
import scipy.stats as st
import numpy as np
import tkFont

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
w = 800
h = 300
x = 50
y = 100

#changing the geometry of root
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

root.title("Part 3 Problem 2")

toplabel=Label(root, text = "Select a disease name from the below drop down to classify new patients",relief=FLAT)
toplabel.config(width=70,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
toplabel.pack()

#declaring a tkinter variable and assigning it the first element of the list created earlier
variable1 = StringVar(root)
variable1.set(disease_name[0]) # default value to be displayed

#apply function on OptionMenu creates a drop down list with values in the list disease_description
o1 = apply(OptionMenu, (root, variable1) + tuple(disease_name))
o1.config(width=15,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
o1.pack()#.pack() function adds the element to the root window





def Go():
    selected1=variable1.get()


    result_frame = Toplevel(root)
    result_frame.title("Results")
    result_frame.geometry("%dx%d+%d+%d" % (w, h, x, y))

    #canvas = Canvas(Result_fr)
    #canvas.grid(row=0, column=0, sticky='nswe')

    #scroll = Scrollbar(Result_fr, orient=VERTICAL, command=canvas.yview)
    #scroll.grid(row=0, column=1, sticky='ns')
    #canvas.configure(yscrollcommand=scroll.set)

    #result_frame = Frame(canvas)

    #canvas.create_window(0, 0, window=result_frame, anchor='nw')
    
    
    query2="""select pr."UID1",mf.exp from microarrayfact mf inner join probe pr on mf.pb_id = pr.pb_id inner join Patient1 p on mf.S_ID=p.S_ID
              where p.p_id in(select di.p_id from DIAGNOSIS di, disease ds where   di.DS_ID=ds.DS_ID and ds.NAME =: select1) order by p.p_id, pr."UID1"
     """.replace('\n',' ')


    query3="""select pr."UID1",mf.exp from microarrayfact mf inner join probe pr on mf.pb_id = pr.pb_id inner join Patient1 p on mf.S_ID=p.S_ID
              where p.p_id in(select di.p_id from DIAGNOSIS di, disease ds where   di.DS_ID=ds.DS_ID and ds.NAME <>: select1) order by p.p_id, pr."UID1"
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
    corresponding_mf_A=[]
    corresponding_mf_B=[]
    
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
            corresponding_mf_A.append(mf_values_A)
            corresponding_mf_B.append(mf_values_B)
            
            ttest_pvalues.append(temp_variable_ttest[1])
            count+=1
            
        # forming query to extract new patient data

    query4 = "select * from testsample where u_id in ("

    for i in range(0, len(informative_gene)):

        query4 += str(informative_gene[i])

        if (i != len(informative_gene) - 1):

            query4 += ","

    query4 += ") order by u_id"

    print(query4)

    c.execute(query4) # execute query



    # create an expression list for each new patient

    expList1 = []

    expList2 = []

    expList3 = []

    expList4 = []

    expList5 = []

    # populate expression list with data got from Oracle

    for row in c:

        expList1.append(row[1])

        expList2.append(row[2])

        expList3.append(row[3])

        expList4.append(row[4])

        expList5.append(row[5])
        
    # forming query to extract expression values for patient in group A

    queryA = "select pa.p_id, mf.exp from patient1 pa inner join microarrayfact mf on pa.s_id = mf.s_id inner join probe pb on pb.pb_id = mf.pb_id where pb.uid1 in ("

    for i in range(0, len(informative_gene)):

        queryA += str(informative_gene[i])

        if (i != len(informative_gene) - 1):

            queryA += ","

    queryA += ")"

    queryA += " and pa.p_id in (select distinct diag.p_id as p_id from diagnosis diag inner join disease ds on diag.ds_id = ds.ds_id where ds.name =:select1 "

    queryA += ") order by pa.p_id, pb.uid1"

    c.execute(queryA, select1=selected1) # execute query

    expListA = []

    for row in c:

        expListA.append(row[1])

    

    # compute correlation for new patient with every patient in group A

    corr1A = []

    corr2A = []

    corr3A = []

    corr4A = []

    corr5A = []

    for i in range(0, len(expListA) / len(informative_gene)):

        # get the sublist of expression that correspond to a patient

        expList = expListA[(i * len(informative_gene)):((i+1) * len(informative_gene))]

        # compute correlation between expList1-5 and expList

        corr1A.append(st.pearsonr(expList1,expList)[0])

        corr2A.append(st.pearsonr(expList2,expList)[0])

        corr3A.append(st.pearsonr(expList3,expList)[0])

        corr4A.append(st.pearsonr(expList4,expList)[0])

        corr5A.append(st.pearsonr(expList5,expList)[0])

         

    # forming query to extract expression values for patient in group B

    queryB = "select pa.p_id, mf.exp from patient1 pa inner join microarrayfact mf on pa.s_id = mf.s_id inner join probe pb on pb.pb_id = mf.pb_id where pb.uid1 in ("

    for i in range(0, len(informative_gene)):

        queryB += str(informative_gene[i])

        if (i != len(informative_gene) - 1):

            queryB += ","

    queryB += ")"

    queryB += " and pa.p_id in (select distinct diag.p_id as p_id from diagnosis diag inner join disease ds on diag.ds_id = ds.ds_id where ds.name <> :select1 "

    queryB += ") order by pa.p_id, pb.uid1"

    c.execute(queryB,select1=selected1) # execute query

    expListB = []

    for row in c:

        expListB.append(row[1])

    print "length of expression list B"+np.str(len(expListB))

    # compute correlation for new patient with every patient in group A

    corr1B = []
    corr2B = []
    corr3B = []
    corr4B = []
    corr5B = []

    for i in range(0, len(expListB) / len(informative_gene)):

        # get the sublist of expression that correspond to a patient

        expList = expListB[(i * len(informative_gene)):((i+1) * len(informative_gene))]

        # compute correlation between expList1 and expList

        corr1B.append(st.pearsonr(expList1,expList)[0])

        corr2B.append(st.pearsonr(expList2,expList)[0])

        corr3B.append(st.pearsonr(expList3,expList)[0])

        corr4B.append(st.pearsonr(expList4,expList)[0])

        corr5B.append(st.pearsonr(expList5,expList)[0])



    # do t-test corr1A and corr1B
    res1 = st.ttest_ind(corr1A,corr1B,equal_var=True)

    if (res1[1] < 0.01):
        
        l1 = Label(result_frame,text="Patient 1 is classified as having %s as the p-value returned by T-test is %e" % (selected1, res1[1]), relief=FLAT)
        l1.config(width=100,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
        l1.pack(side=TOP)        
        
        
        print "classify as " + selected1

    else:
        l1 = Label(result_frame,text="Patient 1 is classified as NOT having %s as the p-value returned by T-test is %e" % (selected1, res1[1]), relief=FLAT)
        l1.config(width=100,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
        l1.pack(side=TOP)     

        print "classify as not " + selected1

        

    
    res2=st.ttest_ind(corr2A,corr2B,equal_var=True)

    if (res2[1] < 0.01):
        l2 = Label(result_frame,text="Patient 2 is classified as having %s as the p-value returned by T-test is %e" % (selected1, res2[1]), relief=FLAT)
        l2.config(width=100,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
        l2.pack(side=TOP)         
        
         
        print "classify as " + selected1

    else:
        l2 = Label(result_frame,text="Patient 2 is classified as NOT having %s as the p-value returned by T-test is %e" % (selected1, res2[1]), relief=FLAT)
        l2.config(width=100,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
        l2.pack(side=TOP) 

        print "classify as not " + selected1

    # do t-test corr3A and corr3B
    res3= st.ttest_ind(corr3A,corr3B,equal_var=True)

    if (res3[1] < 0.01): 
               
        l3 = Label(result_frame,text="Patient 3 is classified as having %s as the p-value returned by T-test is %e" % (selected1, res3[1]), relief=FLAT)
        l3.config(width=100,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
        l3.pack(side=TOP)

    else:
        l3 = Label(result_frame,text="Patient 3 is classified as NOT having %s as the p-value returned by T-test is %e" % (selected1, res3[1]), relief=FLAT)
        l3.config(width=100,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
        l3.pack(side=TOP)

        #print "classify as not " + selected1



    # do t-test corr4A and corr4B
    res4=st.ttest_ind(corr4A,corr4B,equal_var=True)
    if (res4[1] < 0.01):
        l4 = Label(result_frame,text="Patient 4 is classified as having %s as the p-value returned by T-test is %e" % (selected1, res4[1]), relief=FLAT)
        l4.config(width=100,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
        l4.pack(side=TOP)         

        print "classify as " + selected1

    else:
        l4 = Label(result_frame,text="Patient 4 is classified as NOT having %s as the p-value returned by T-test is %e" % (selected1, res4[1]), relief=FLAT)
        l4.config(width=100,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
        l4.pack(side=TOP)         

        print "classify as not " + selected1

    # do t-test corr5A and corr5B
    
    res5=st.ttest_ind(corr5A,corr5B,equal_var=True)

    if (res5[1] < 0.01):
        l5 = Label(result_frame,text="Patient 5 is classified as having %s as the p-value returned by T-test is %e" % (selected1, res5[1]), relief=FLAT)
        l5.config(width=100,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
        l5.pack(side=TOP) 
        print "classify as " + selected1

    else:
        l5 = Label(result_frame,text="Patient 5 is classified as NOT having %s as the p-value returned by T-test is %e" % (selected1, res5[1]), relief=FLAT)
        l5.config(width=100,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
        l5.pack(side=TOP) 
        print "classify as not " + selected1
    del dictionary_guid_A,dictionary_guid_B    
            
            
button = Button(root, text="GO", command=Go)
button.config(width=10,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
button.pack()

#this is like the main function in tkinter which has to be invoked for all the above code to get executed 
mainloop()    
    
    
    