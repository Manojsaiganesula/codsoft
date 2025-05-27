from tkinter import *
from tkinter import messagebox, ttk
import sqlite3 as sql
import os

class TaskDatabase:
    def __init__(self, db_name='listOfTasks.db'):
        if os.path.exists(db_name):
            try:
                conn = sql.connect(db_name)
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT id FROM tasks LIMIT 1")
                    conn.close()
                except sql.OperationalError:
                    conn.close()
                    if os.path.exists(db_name + '.backup'):
                        os.remove(db_name + '.backup')
                    os.rename(db_name, db_name + '.backup')
                    print(f"Old database format detected. Renamed to {db_name}.backup and creating new database.")
            except:
                pass
        
        self.conn = sql.connect(db_name)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT, 
                priority INTEGER DEFAULT 2,
                due_date TEXT,
                completed INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_task(self, title, priority=2, due_date=None):
        self.cursor.execute(
            'INSERT INTO tasks (title, priority, due_date, completed) VALUES (?, ?, ?, ?)', 
            (title, priority, due_date, 0)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def toggle_completed(self, task_id):
        self.cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
        result = self.cursor.fetchone()
        if not result:
            return None
            
        current_status = result[0]
        new_status = 0 if current_status else 1
        self.cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_status, task_id))
        self.conn.commit()
        return new_status

    def delete_task(self, task_id):
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()

    def delete_all_tasks(self):
        self.cursor.execute('DELETE FROM tasks')
        self.conn.commit()

    def get_tasks(self, filter_completed=None):
        query = 'SELECT id, title, priority, due_date, completed FROM tasks'
        params = []
        
        if filter_completed is not None:
            query += ' WHERE completed = ?'
            params.append(filter_completed)
            
        query += ' ORDER BY priority, due_date, title'
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

class TaskManager:
    def __init__(self, root):
        self.db = TaskDatabase()
        self.tasks = []
        self.task_ids = []
        
        root.title("Enhanced To-Do List")
        root.geometry("800x500+550+250")
        root.resizable(0, 0)
        root.configure(bg="#F0F8FF")
        
        self.colors = {
            "bg": "#F0F8FF",
            "header": "#4682B4",
            "button": "#5F9EA0",
            "high_priority": "#FFD1DC",
            "medium_priority": "#FFFACD",
            "low_priority": "#E0FFFF",
            "completed": "#D3D3D3"
        }
        
        self.create_header(root)
        self.create_input_area(root)
        self.create_task_list(root)
        self.create_buttons(root)
        
        self.filter_completed = None
        self.retrieve_database()
        self.update_listbox()

    def create_header(self, parent):
        Label(
            parent,
            text="ENHANCED TO-DO LIST",
            font=("Arial", "16", "bold"),
            bg=self.colors["header"],
            fg="white",
            pady=10,
            width=800
        ).pack(fill="x")

    def create_input_area(self, parent):
        input_frame = Frame(parent, bg=self.colors["bg"], pady=10)
        input_frame.pack(fill="x", padx=20)
        
        Label(
            input_frame,
            text="Task Title:",
            font=("Arial", "12", "bold"),
            bg=self.colors["bg"]
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.task_title = Entry(
            input_frame,
            font=("Arial", "12"),
            width=40
        )
        self.task_title.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        Label(
            input_frame,
            text="Priority:",
            font=("Arial", "12", "bold"),
            bg=self.colors["bg"]
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.task_priority = ttk.Combobox(
            input_frame,
            font=("Arial", "12"),
            width=15,
            values=["High", "Medium", "Low"]
        )
        self.task_priority.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.task_priority.current(1)
        
        Label(
            input_frame,
            text="Due Date:",
            font=("Arial", "12", "bold"),
            bg=self.colors["bg"]
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.task_due_date = Entry(
            input_frame,
            font=("Arial", "12"),
            width=40
        )
        self.task_due_date.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.task_due_date.insert(0, "YYYY-MM-DD (Optional)")
        
        filter_frame = Frame(input_frame, bg=self.colors["bg"])
        filter_frame.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="w")
        
        Label(
            filter_frame,
            text="Status:",
            font=("Arial", "12", "bold"),
            bg=self.colors["bg"]
        ).pack(side=LEFT, padx=5)
        
        self.status_filter = ttk.Combobox(
            filter_frame,
            values=["All", "Active", "Completed"],
            width=10
        )
        self.status_filter.pack(side=LEFT, padx=5)
        self.status_filter.current(0)
        self.status_filter.bind("<<ComboboxSelected>>", self.filter_tasks)

    def create_task_list(self, parent):
        list_frame = Frame(parent, bg=self.colors["bg"], pady=10)
        list_frame.pack(fill="both", expand=True, padx=20)
        
        columns = ("Title", "Priority", "Due Date", "Status")
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.task_tree.heading(col, text=col)
            
        self.task_tree.column("Title", width=350)
        self.task_tree.column("Priority", width=100)
        self.task_tree.column("Due Date", width=150)
        self.task_tree.column("Status", width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side=RIGHT, fill=Y)
        self.task_tree.pack(fill=BOTH, expand=True)
        
        self.task_tree.bind("<Double-1>", self.toggle_task_completion)

    def create_buttons(self, parent):
        button_frame = Frame(parent, bg=self.colors["bg"], pady=10)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        Button(
            button_frame,
            text="Add Task",
            bg=self.colors["button"],
            fg="white",
            font=("Arial", "11", "bold"),
            width=15,
            command=self.add_task
        ).pack(side=LEFT, padx=5)
        
        Button(
            button_frame,
            text="Toggle Complete",
            bg=self.colors["button"],
            fg="white", 
            font=("Arial", "11", "bold"),
            width=15,
            command=self.toggle_selected_task
        ).pack(side=LEFT, padx=5)
        
        Button(
            button_frame,
            text="Delete Task",
            bg=self.colors["button"],
            fg="white",
            font=("Arial", "11", "bold"),
            width=15,
            command=self.delete_task
        ).pack(side=LEFT, padx=5)
        
        Button(
            button_frame,
            text="Delete All",
            bg="#DC143C", 
            fg="white",
            font=("Arial", "11", "bold"),
            width=15,
            command=self.delete_all_tasks
        ).pack(side=LEFT, padx=5)

    def add_task(self):
        title = self.task_title.get().strip()
        priority_text = self.task_priority.get()
        due_date = self.task_due_date.get().strip()
        
        if not title:
            messagebox.showinfo('Error', 'Task title cannot be empty.')
            return
            
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        priority = priority_map.get(priority_text, 2)
        
        if due_date == "YYYY-MM-DD (Optional)":
            due_date = None
            
        self.db.add_task(title, priority, due_date)
        
        self.task_title.delete(0, END)
        self.task_priority.current(1)
        self.task_due_date.delete(0, END)
        self.task_due_date.insert(0, "YYYY-MM-DD (Optional)")
        
        self.retrieve_database()
        self.update_listbox()

    def toggle_task_completion(self, event):
        selected_item = self.task_tree.selection()
        if selected_item:
            self.toggle_selected_task()

    def toggle_selected_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showinfo('Error', 'No task selected.')
            return
            
        index = self.task_tree.index(selected_item[0])
        if index >= len(self.task_ids):
            return
            
        task_id = self.task_ids[index]
        
        self.db.toggle_completed(task_id)
        
        self.retrieve_database()
        self.update_listbox()

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showinfo('Error', 'No task selected.')
            return
            
        index = self.task_tree.index(selected_item[0])
        if index >= len(self.task_ids):
            return
            
        task_id = self.task_ids[index]
        
        if messagebox.askyesno('Delete Task', 'Are you sure?'):
            self.db.delete_task(task_id)
            self.retrieve_database()
            self.update_listbox()

    def delete_all_tasks(self):
        if messagebox.askyesno('Delete All', 'Are you sure?'):
            self.db.delete_all_tasks()
            self.retrieve_database()
            self.update_listbox()

    def filter_tasks(self, event=None):
        status = self.status_filter.get()
        
        if status == "All":
            self.filter_completed = None
        elif status == "Active":
            self.filter_completed = 0
        elif status == "Completed":
            self.filter_completed = 1
            
        self.retrieve_database()
        self.update_listbox()

    def retrieve_database(self):
        self.tasks = self.db.get_tasks(filter_completed=self.filter_completed)
        self.task_ids = [task[0] for task in self.tasks]

    def update_listbox(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
            
        priority_names = {1: "High", 2: "Medium", 3: "Low"}
        priority_colors = {1: self.colors["high_priority"], 2: self.colors["medium_priority"], 3: self.colors["low_priority"]}
        
        for task in self.tasks:
            task_id, title, priority, due_date, completed = task
            
            display_status = "Completed" if completed else "Active"
            display_priority = priority_names.get(priority, "Medium")
            
            values = (title, display_priority, due_date or "", display_status)
            
            item_id = self.task_tree.insert("", END, values=values)
            
            if completed:
                self.task_tree.tag_configure("completed", background=self.colors["completed"])
                self.task_tree.item(item_id, tags=("completed",))
            else:
                tag_name = f"priority_{priority}"
                self.task_tree.tag_configure(tag_name, background=priority_colors.get(priority, "white"))
                self.task_tree.item(item_id, tags=(tag_name,))

    def close(self):
        self.db.close()
        guiWindow.destroy()

if __name__ == "__main__":
    guiWindow = Tk()
    app = TaskManager(guiWindow)
    guiWindow.mainloop()