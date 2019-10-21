
# coding: utf-8

# In[8]:

from Tkinter import *
def func1():
    import subprocess
    import os
    #import dw_problem1
    #import dw_problem2
    #import dw_problem6

    root = Tk() # creates main window by name root

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.title("Main Window")
    root.configure(background='blue')

    #setting the main window size
    w = 800
    h = 500
    x = 50
    y = 100

    #changing the geometry of root
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))

    canvas = Canvas(root)
    canvas.grid(row=0, column=0, sticky='nswe')

    canvas.configure(background='blue')

    result_frame = Frame(canvas)
    result_frame.configure(background='blue')

    canvas.create_window(0, 0, window=result_frame, anchor='nw')
    def pr1():
        os.system('python dw_part2_1.py')

    def pr2():
        os.system('python dw_part2_2.py')
    def pr3():
        os.system('python dw_part2_3.py')
    def pr4():
        os.system('python dw_part2_4.py')
    def pr5():
        os.system('python dw_part2_5.py')
    def pr6():
        os.system('python dw_part2_6.py')
    def pr7():
        os.system('python dw_part3_1.py')
    def pr8():
        os.system('python dw_part3_2.py')



    b1 = Button(result_frame, text='Part 2 Problem 1', command=pr1)
    b1.config(width=30,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
    b1.pack(side=TOP, padx=4, pady=4)

    b2 = Button(result_frame, text='Part 2 Problem 2', command=pr2)
    b2.config(width=30,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
    b2.pack(side=TOP, padx=4, pady=4)

    b3 = Button(result_frame, text='Part 2 Problem 3',  command=pr3)
    b3.config(width=30,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
    b3.pack(side=TOP, padx=4, pady=4)

    b4 = Button(result_frame, text='Part 2 Problem 4', command=pr4)
    b4.config(width=30,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
    b4.pack(side=TOP, padx=4, pady=4)

    b5 = Button(result_frame, text='Part 2 Problem 5', width=40, command=pr5)
    b5.config(width=30,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
    b5.pack(side=TOP, padx=4, pady=4)

    b6 = Button(result_frame, text='Part 2 Problem 6', width=40, command=pr6)
    b6.config(width=30,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
    b6.pack(side=TOP, padx=4, pady=4)
    
    b7 = Button(result_frame, text='Part 3 Problem 1', width=40, command=pr7)
    b7.config(width=30,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
    b7.pack(side=TOP, padx=4, pady=4)   
    
    b8 = Button(result_frame, text='Part 3 Problem 2', width=40, command=pr8)
    b8.config(width=30,justify=LEFT,anchor=W,borderwidth=10,font=('bold', 12))
    b8.pack(side=TOP, padx=4, pady=4) 

    result_frame.update_idletasks()


    root.mainloop()
    
if __name__ == '__main__':
    func1()



# In[ ]:




# In[ ]:



