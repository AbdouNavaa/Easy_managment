from tkinter import *
from tkinter import messagebox, ttk, filedialog
import time
from ttkthemes import ThemedTk
import pymysql
import pandas as pd
# functions
def connect_db():
    try:
        # create a connection object
        global connect 
        global my_cursor
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='sms')
        my_cursor = connect.cursor()
        # messagebox.showinfo('Connection Successful', 'Connected to the database')
        print('Connected to the database')
        show_students()
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
        
    try:
        query = 'create database sms'
        my_cursor.execute(query)
        query = 'use sms'
        my_cursor.execute(query)
        query = 'create table students (Id int primary key auto_increment, name varchar(30), level int not null,'\
        'number varchar(11), email varchar(30), address varchar(100), gender varchar(7), GPA float)'
        my_cursor.execute(query)
        
    except :
        query = 'use sms'
        my_cursor.execute(query)
        

def clock():
    current_date = time.strftime("%d-%m-%Y")
    current_time = time.strftime('%H:%M:%S %p')
    date_label.config(text=f'Date : {current_date}\nTime : {current_time}', )
    # label.config(text=time)
    date_label.after(1000, clock) # pour appler la fonction chaque 1 seconde pour etre fonctionnee 


def add_student():
    def insert_student():
        st_id = id_entry.get()
        name = name_entry.get()
        level = level_entry.get()
        number = number_entry.get()
        email = email_entry.get()
        address = address_entry.get()
        gender = gender_entry.get()
        gpa = gpa_entry.get()
        
        if st_id == '' or name == '' or level == '' or number == '' or email == '' or address == '' or gender == '' or gpa == '':
            messagebox.showerror('Error', 'Please fill all the fields',parent=add_student_windo)
        else:
            try:
                query = 'insert into student values(%s,%s,%s,%s,%s,%s,%s,%s)'
                my_cursor.execute(query,(st_id,name,level,number,email,address,gender,gpa))
                connect.commit()
                result = messagebox.askyesno('Student added successfully', 'do you want to clean the form?' , parent=add_student_windo)
                if result == True:
                    # id_entry.set('')
                    name.delete(0, END) 
                    # level.delete(0, END)
                    # number.delete(0, END)
                    # email.delete(0, END)
                    # address.delete(0, END)
                    # gender.delete(0, END)
                    # gpa.delete(0, END)
                show_students()
            except Exception as e:
                messagebox.showerror('Error', str(e))
    
    add_student_windo = Toplevel()
    add_student_windo.title('Add Student')
    # add_student_windo.geometry('500x600+500+50')
    add_student_windo.grab_set() # pour dire au user qu'il ne permet pas de faire aucun chose(open autre widow ou cliquer sur button ...) sauf 
    # sauf s'il ferme cette windo
    # add_student_windo.configure(bg="#fff")
    
    
        
    # Id
    id_label = Label(add_student_windo,text='Id', font=('Arial', 15,'bold'))
    id_label.grid(row=0,column=0,padx=20,pady=15,sticky=W)
    
    id_entry = Entry(add_student_windo, font=('arial', 15,'bold'), width=20)
    id_entry.grid(row=0,column=1,padx=20,pady=15)
    
    # Name
    name_label = Label(add_student_windo,text='Name', font=('Arial', 15,'bold'))
    name_label.grid(row=1,column=0,padx=20,pady=15,sticky=W)
    
    name_entry = Entry(add_student_windo, font=('arial', 15,'bold'), width=20)
    name_entry.grid(row=1,column=1,padx=20,pady=15)
    
    # Level
    level_label = Label(add_student_windo,text='Level', font=('Arial', 15,'bold'))
    level_label.grid(row=2,column=0,padx=20,pady=15,sticky=W)
    
    level_entry = Entry(add_student_windo, font=('arial', 15,'bold'), width=20)
    level_entry.grid(row=2,column=1,padx=20,pady=15)
    
    # Number
    number_label = Label(add_student_windo,text='Number', font=('Arial', 15,'bold'))
    number_label.grid(row=3,column=0,padx=20,pady=15,sticky=W)
    
    number_entry = Entry(add_student_windo, font=('arial', 15,'bold'), width=20)
    number_entry.grid(row=3,column=1,padx=20,pady=15)
    
    # Email
    email_label = Label(add_student_windo,text='Email', font=('Arial', 15,'bold'))
    email_label.grid(row=4,column=0,padx=20,pady=15,sticky=W)
    
    email_entry = Entry(add_student_windo, font=('arial', 15,'bold'), width=20)
    email_entry.grid(row=4,column=1,padx=20,pady=15)
    
    # Address
    address_label = Label(add_student_windo,text='Address', font=('Arial', 15,'bold'))
    address_label.grid(row=5,column=0,padx=20,pady=15,sticky=W)
    
    address_entry = Entry(add_student_windo, font=('arial', 15,'bold'), width=20)
    address_entry.grid(row=5,column=1,padx=20,pady=15)
    
    # Gender
    gender_label = Label(add_student_windo,text='Gender', font=('Arial', 15,'bold')) 
    gender_label.grid(row=6,column=0,padx=20,pady=15,sticky=W)
    
    gender_entry = Entry(add_student_windo, font=('arial', 15,'bold'), width=20)    
    gender_entry.grid(row=6,column=1,padx=20,pady=15)
    
    # GPA
    gpa_label = Label(add_student_windo,text='GPA', font=('Arial', 15,'bold'))
    gpa_label.grid(row=7,column=0,padx=20,pady=15,sticky=W)
    
    gpa_entry = Entry(add_student_windo, font=('arial', 15,'bold'), width=20)
    gpa_entry.grid(row=7,column=1,padx=20,pady=15)
    
    # buttons
    add_button = ttk.Button(add_student_windo, text='Add' ,style='Custom.TButton', command=insert_student)
    add_button.grid(row=8,column=1, pady=15, ipadx=70, )
    add_student_windo.mainloop()

def search_student():
    def search():
        
        query = 'select * from student where Id=%s or name=%s or level=%s or number=%s or email=%s or address=%s or gender=%s or GPA=%s'
        my_cursor.execute(query,(id_entry.get(),name_entry.get(),level_entry.get(),number_entry.get(),email_entry.get(),address_entry.get(),gender_entry.get(),gpa_entry.get()))
        rows = my_cursor.fetchall()
        student_table.delete(*student_table.get_children())
        for row in rows:
            student_table.insert('',END, values=row)
            
            
    search_student_windo = Toplevel()
    search_student_windo.title('Search Student')
    # search_student_windo.geometry('500x600+500+50')
    search_student_windo.grab_set() # pour dire au user qu'il ne permet pas de faire aucun chose(open autre widow ou cliquer sur button ...) sauf 
    # sauf s'il ferme cette windo
    # search_student_windo.configure(bg="#fff")
    
    
        
    # Id
    id_label = Label(search_student_windo,text='Id', font=('Arial', 15,'bold'))
    id_label.grid(row=0,column=0,padx=20,pady=15,sticky=W)
    
    id_entry = Entry(search_student_windo, font=('arial', 15,'bold'), width=20)
    id_entry.grid(row=0,column=1,padx=20,pady=15)
    
    # Name
    name_label = Label(search_student_windo,text='Name', font=('Arial', 15,'bold'))
    name_label.grid(row=1,column=0,padx=20,pady=15,sticky=W)
    
    name_entry = Entry(search_student_windo, font=('arial', 15,'bold'), width=20)
    name_entry.grid(row=1,column=1,padx=20,pady=15)
    
    # Level
    level_label = Label(search_student_windo,text='Level', font=('Arial', 15,'bold'))
    level_label.grid(row=2,column=0,padx=20,pady=15,sticky=W)
    
    level_entry = Entry(search_student_windo, font=('arial', 15,'bold'), width=20)
    level_entry.grid(row=2,column=1,padx=20,pady=15)
    
    # Number
    number_label = Label(search_student_windo,text='Number', font=('Arial', 15,'bold'))
    number_label.grid(row=3,column=0,padx=20,pady=15,sticky=W)
    
    number_entry = Entry(search_student_windo, font=('arial', 15,'bold'), width=20)
    number_entry.grid(row=3,column=1,padx=20,pady=15)
    
    # Email
    email_label = Label(search_student_windo,text='Email', font=('Arial', 15,'bold'))
    email_label.grid(row=4,column=0,padx=20,pady=15,sticky=W)
    
    email_entry = Entry(search_student_windo, font=('arial', 15,'bold'), width=20)
    email_entry.grid(row=4,column=1,padx=20,pady=15)
    
    # Address
    address_label = Label(search_student_windo,text='Address', font=('Arial', 15,'bold'))
    address_label.grid(row=5,column=0,padx=20,pady=15,sticky=W)
    
    address_entry = Entry(search_student_windo, font=('arial', 15,'bold'), width=20)
    address_entry.grid(row=5,column=1,padx=20,pady=15)
    
    # Gender
    gender_label = Label(search_student_windo,text='Gender', font=('Arial', 15,'bold')) 
    gender_label.grid(row=6,column=0,padx=20,pady=15,sticky=W)
    
    gender_entry = Entry(search_student_windo, font=('arial', 15,'bold'), width=20)    
    gender_entry.grid(row=6,column=1,padx=20,pady=15)
    
    # GPA
    gpa_label = Label(search_student_windo,text='GPA', font=('Arial', 15,'bold'))
    gpa_label.grid(row=7,column=0,padx=20,pady=15,sticky=W)
    
    gpa_entry = Entry(search_student_windo, font=('arial', 15,'bold'), width=20)
    gpa_entry.grid(row=7,column=1,padx=20,pady=15)
    
    # buttons
    search_button = ttk.Button(search_student_windo, text='Search' , command=search)
    search_button.grid(row=8,column=1, pady=15, ipadx=70, )
    search_student_windo.mainloop()



def update_student():
    def update():
        query = "UPDATE student SET id=%s, name=%s, level=%s, number=%s, email=%s, address=%s, gender=%s, gpa=%s WHERE id=%s"
        my_cursor.execute(query, (id_entry.get(),name_entry.get(), level_entry.get(), number_entry.get(), email_entry.get(), address_entry.get(), gender_entry.get(), gpa_entry.get(), row[0]))
        connect.commit()
        messagebox.showinfo("Update Student", "Student Updated Successfully")
        show_students()
        update_student_windo.destroy()
        
        
    update_student_windo = Toplevel()
    update_student_windo.title('Update Student')
    # update_student_windo.geometry('500x600+500+50')
    update_student_windo.grab_set() # pour dire au user qu'il ne permet pas de faire aucun chose(open autre widow ou cliquer sur button ...) sauf 
    # sauf s'il ferme cette windo
    # update_student_windo.configure(bg="#fff")
    
    
        
    # Id
    id_label = Label(update_student_windo,text='Id', font=('Arial', 15,'bold'))
    id_label.grid(row=0,column=0,padx=20,pady=15,sticky=W)
    
    id_entry = Entry(update_student_windo, font=('arial', 15,'bold'), width=20)
    id_entry.grid(row=0,column=1,padx=20,pady=15)
    
    # Name
    name_label = Label(update_student_windo,text='Name', font=('Arial', 15,'bold'))
    name_label.grid(row=1,column=0,padx=20,pady=15,sticky=W)
    
    name_entry = Entry(update_student_windo, font=('arial', 15,'bold'), width=20)
    name_entry.grid(row=1,column=1,padx=20,pady=15)
    
    # Level
    level_label = Label(update_student_windo,text='Level', font=('Arial', 15,'bold'))
    level_label.grid(row=2,column=0,padx=20,pady=15,sticky=W)
    
    level_entry = Entry(update_student_windo, font=('arial', 15,'bold'), width=20)
    level_entry.grid(row=2,column=1,padx=20,pady=15)
    
    # Number
    number_label = Label(update_student_windo,text='Number', font=('Arial', 15,'bold'))
    number_label.grid(row=3,column=0,padx=20,pady=15,sticky=W)
    
    number_entry = Entry(update_student_windo, font=('arial', 15,'bold'), width=20)
    number_entry.grid(row=3,column=1,padx=20,pady=15)
    
    # Email
    email_label = Label(update_student_windo,text='Email', font=('Arial', 15,'bold'))
    email_label.grid(row=4,column=0,padx=20,pady=15,sticky=W)
    
    email_entry = Entry(update_student_windo, font=('arial', 15,'bold'), width=20)
    email_entry.grid(row=4,column=1,padx=20,pady=15)
    
    # Address
    address_label = Label(update_student_windo,text='Address', font=('Arial', 15,'bold'))
    address_label.grid(row=5,column=0,padx=20,pady=15,sticky=W)
    
    address_entry = Entry(update_student_windo, font=('arial', 15,'bold'), width=20)
    address_entry.grid(row=5,column=1,padx=20,pady=15)
    
    # Gender
    gender_label = Label(update_student_windo,text='Gender', font=('Arial', 15,'bold')) 
    gender_label.grid(row=6,column=0,padx=20,pady=15,sticky=W)
    
    gender_entry = Entry(update_student_windo, font=('arial', 15,'bold'), width=20)    
    gender_entry.grid(row=6,column=1,padx=20,pady=15)
    
    # GPA
    gpa_label = Label(update_student_windo,text='GPA', font=('Arial', 15,'bold'))
    gpa_label.grid(row=7,column=0,padx=20,pady=15,sticky=W)
    
    gpa_entry = Entry(update_student_windo, font=('arial', 15,'bold'), width=20)
    gpa_entry.grid(row=7,column=1,padx=20,pady=15)
    
    # buttons
    search_button = ttk.Button(update_student_windo, text='Update' , command=update)
    search_button.grid(row=8,column=1, pady=15, ipadx=70, )

    index = student_table.focus()
    data = student_table.item(index)
    row = data['values']
    
    print(row)
    
    id_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    level_entry.insert(0, row[2])
    number_entry.insert(0, row[3])
    email_entry.insert(0, row[4])
    address_entry.insert(0, row[5])
    gender_entry.insert(0, row[6])
    gpa_entry.insert(0, row[7])

    update_student_windo.mainloop()



def delete_student():   
    index = student_table.focus()
    # print(index)
    data = student_table.item(index)
    id = data['values'][0]
    query = 'delete from student where id=%s'
    my_cursor.execute(query,(id,))
    connect.commit()
    messagebox.showinfo('Success', 'Student deleted successfully')
    show_students()

def show_students():
    
    query = 'select * from student'
    my_cursor.execute(query)
    data = my_cursor.fetchall()
    # print(data)
    student_table.delete(*student_table.get_children())#pour supprimer les donnees exist dans la table avant de les afficher
    for row in data:
        student_table.insert('', 'end', values=row)

def export_student():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexs = student_table.get_children()
    file =[]
    
    for index in indexs:
        content = student_table.item(index)
        file.append(content['values'])
    df = pd.DataFrame(file, columns=['Id', 'Name', 'Level', 'Number', 'Email', 'Address', 'Gender', 'GPA'])
    df.to_csv(url, index=False)# index = Flase pour commencer pr premiere column ou par defaut il commence par le deuxieme et lesse le premiere vide
    messagebox.showinfo('Success', 'Students exported successfully',parent=root)
    
def exit_project():
    result = messagebox.askyesno('Confirm','Are you sure you want to exit?' )
    if result == 'yes':
        root.destroy()
# gui

# create the window
root = ThemedTk()
root.get_themes()

# root.set_theme('equilux') # belles fonts : breeze ou equilux ,arc ou adapta
root.set_theme('arc') # change the theme to vista

root.title('SMS')
root.geometry('1100x630+150+10') #150 pour margin horizontal et 40 pour margin vertical je pense
root.resizable(True, True)
root.configure(bg="#fff")

# create frame for date
date_label = Label(root, font=('Arial', 15,'bold'),bg="#fff")
date_label.place(x=5, y=5)
clock()

# create frame for slider
slider_label = Label(root, text='Student Management System',font=('Arial', 20,'bold'),bg="#fff")
slider_label.place(x=250, y=10)

# left frame

left_frame = Frame(root, bg="#fff")
left_frame.place(x=50, y=80, width=300, height=500)

logo_img = PhotoImage(file='student.png')
logo_img_label = Label(left_frame, image=logo_img, bg='#fff')
logo_img_label.grid(row=0, column=0, columnspan=2, pady=16)

# buttons

add_student_btn = ttk.Button(left_frame , width=27, text='Add student' ,command=add_student)
add_student_btn.grid(row=1,  pady=10)


search_student_btn = ttk.Button(left_frame , width=27, text='Search student' ,command=search_student)
search_student_btn.grid(row=2,  pady=10)

delete_student_btn = ttk.Button(left_frame , width=27, text='Delete student' ,command= delete_student)
delete_student_btn.grid(row=3,  pady=10)

update_student_btn = ttk.Button(left_frame , width=27, text='Update student' ,command=update_student)
update_student_btn.grid(row=4,  pady=10)

show_students_btn = ttk.Button(left_frame , width=27, text='Show student' ,command=show_students)
show_students_btn.grid(row=5,  pady=10)

export_student_btn = ttk.Button(left_frame , width=27, text='Export student' ,command=export_student)
export_student_btn.grid(row=6,  pady=10)

exit_btn = ttk.Button(left_frame , width=27, text='Exit' ,command=exit_project)
exit_btn.grid(row=7,  pady=10)

# create right frame

right_frame = Frame(root)
right_frame.place(x=250, y=70, width=800, height=540,)

scroll_x = Scrollbar(right_frame, orient=HORIZONTAL)
scroll_y = Scrollbar(right_frame, orient=VERTICAL)

student_table = ttk.Treeview(right_frame,columns=('Id','Name','Level','Number','Email','Address','Gender','GPA'),
                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

scroll_x.config(command=student_table.xview)
scroll_y.config(command=student_table.yview)

scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)

student_table.heading('Id', text='Id')
student_table.heading('Name', text='Name')
student_table.heading('Level', text='Level')
student_table.heading('Number', text='Number')
student_table.heading('Email', text='Email')
student_table.heading('Address', text='Address')
student_table.heading('Gender', text='Gender')
student_table.heading('GPA', text='GPA')

student_table.config(show='headings')

student_table.column('Id', width=50,anchor='center')
student_table.column('Name', width=200,)
student_table.column('Level', width=30,anchor='center')
student_table.column('Number', width=50,anchor='center')
student_table.column('Email', width=100)
student_table.column('Address', width=100,)
student_table.column('Gender', width=40,anchor='center')
student_table.column('GPA', width=40,anchor='center')
student_table.pack(fill=BOTH, expand=1,anchor='center')

style = ttk.Style()
style.configure("Treeview", background="white", foreground="black",rowheight=40, font=('Arial', 12,'bold'))
style.configure("Treeview.Heading", background="#fff", foreground="black")



connect_db()
root.mainloop()