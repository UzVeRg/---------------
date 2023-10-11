# импорты
import tkinter as tk
from tkinter import ttk
import sqlite3 as sq

# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # инициализация виджетов главного окна
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)



        # кнопка добавления
        self.img_add = tk.PhotoImage(file='./img/add_user.png')
        btn_add = tk.Button(toolbar, text='Добавить', bg='#d7d7d7',
                            bd=0, image=self.img_add,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)


        # кнопка изменения
        self.img_upd = tk.PhotoImage(file='./img/update.png')
        btn_upd = tk.Button(toolbar, text='Изменить', bg='#d7d7d7',
                            bd=0, image=self.img_upd,
                            command=self.open_update_child)
        btn_upd.pack(side=tk.LEFT)



        # кнопка удаления
        self.img_del = tk.PhotoImage(file='./img/del_user.png')
        btn_del = tk.Button(toolbar, text='Удалить', bg='#d7d7d7',
                            bd=0, image=self.img_del,
                            command=self.delete_records)
        btn_del.pack(side=tk.LEFT)



        # кнопка поиска
        self.img_search = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, text='Найти', bg='#d7d7d7',
                            bd=0, image=self.img_search,
                            command=self.open_search)
        btn_search.pack(side=tk.LEFT)



        # кнопка обновления
        self.img_ref = tk.PhotoImage(file='./img/refresh.png')
        btn_ref = tk.Button(toolbar, text='Обновить', bg='#d7d7d7',
                            bd=0, image=self.img_ref,
                            command=self.view_records)
        btn_ref.pack(side=tk.LEFT)






        # ячейки

        self.tree = ttk.Treeview(self, 
                                 columns=('id', 'name', 'phone', 'email', 'salary'),
                                 height=17,
                                 show='headings')
        self.tree.column('id', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=170, anchor=tk.CENTER)
        self.tree.column('salary', width=120, anchor=tk.CENTER)


        self.tree.heading('id', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack(side=tk.LEFT)




        # скроллбар

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    



    # записи

    def records(self,name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # отображение данных

    def view_records(self):
        self.db.cur.execute('SELECT * FROM staff')
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i in self.db.cur.fetchall():
            self.tree.insert('', 'end', values=i)



    # метод изменения данных

    def update_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE staff
            SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
                            
        ''',(name, phone, email, salary, id))
        self.db.conn.commit()
        self.view_records()



    # удаление записей

    def delete_records(self):
        for row_id in self.tree.selection():
            item_id = self.tree.item(row_id)['values'][0]
            if item_id:
                self.db.cur.execute('DELETE FROM staff WHERE id = ?', (item_id,))
                self.db.conn.commit()
                self.tree.delete(row_id)



    # метод поиска данных
    def search_records(self,name):
        self.db.cur.execute('SELECT * FROM staff WHERE name LIKE ?',
                            ('%' + name + '%', ) )
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i in self.db.cur.fetchall():
            self.tree.insert('', 'end', values=i)










    # вызов дочернего окна
    def open_child(self):
        Child()

    # вызов дочернего окна для редактирования данных
    def open_update_child(self):
        Update()


    # вызов дочернего окна для поиска данных
    def open_search(self):
        Search()






# класс дочернего окна

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


    # инициализация виджетов дочернего окна

    def init_child(self):
        self.title('Добавление данных сотрудника')
        self.geometry('400x200')
        self.resizable(False,False)

        # перехват событий
        self.grab_set()
        # перехват фокуса
        self.focus_set()


        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=30)
        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=50, y=60)
        label_email = tk.Label(self, text='E-mail:')
        label_email.place(x=50, y=90)
        label_salary = tk.Label(self, text='Зарплата:')
        label_salary.place(x=50, y=120)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=30)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=60)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=90)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200, y=120)


        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=200, y=150)


        self.btn_add = tk.Button(self, text='Добавить')
        self.btn_add.bind('<Button-1>', lambda ev: self.view.records(self.entry_name.get(),
                                                                      self.entry_phone.get(),
                                                                      self.entry_email.get(),
                                                                      self.entry_salary.get()))
        self.btn_add.place(x=265, y=150)


# класс дочернего окна для изменения данных

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()


    def init_update(self):
        self.title('Изменение данных сотрудника')
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text='Изменить')
        self.btn_upd.bind('<Button-1>',lambda ev: self.view.update_record(self.entry_name.get(),
                                                                      self.entry_phone.get(),
                                                                      self.entry_email.get(),
                                                                      self.entry_salary.get()))
        self.btn_upd.bind('<Button-1>',lambda ev:self.destroy(),add='+')
        self.btn_upd.place(x=265, y=150)

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT * from staff WHERE id = ?', (id, ))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])





# класс окна для поиска

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


    # инициализация виджетов дочернего окна поиска

    def init_child(self):
        self.title('Поиск сотрудника')
        self.geometry('400x200')
        self.resizable(False,False)

        # перехват событий
        self.grab_set()
        # перехват фокуса
        self.focus_set()


        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)


        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)



        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=200, y=150)


        self.btn_search = tk.Button(self, text='Найти')
        self.btn_search.bind('<Button-1>',
                          lambda ev:self.view.search_records(self.entry_name.get()))
        self.btn_search.bind('<Button-1>',lambda ev:self.destroy(),add='+')
        self.btn_search.place(x=265, y=150)





# класс базы данных

class DB():
    def __init__(self):
        self.conn = sq.connect('Staff.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
                        CREATE TABLE IF NOT EXISTS staff (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            phone TEXT,
                            email TEXT,
                            salary TEXT
                        )''')
        self.conn.commit()
    
    def insert_data(self, name,phone,email, salary):
        self.cur.execute('''
                        INSERT INTO staff (name, phone, email, salary)
                        VALUES (?,?,?,?)''', (name, phone, email, salary))
        self.conn.commit()




# при запуске программы
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('820x450')
    root.resizable(False, False)
    root.mainloop()
