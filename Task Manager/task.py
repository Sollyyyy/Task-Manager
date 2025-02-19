import os
from datetime import date
import csv
import string
import pandas as pd
import sqlite3
import json
class Task:
    _id_counter = 1
    def __init__(self,title,due_date,flag=None):
        self._task_id = Task._id_counter
        Task._id_counter += 1
        self.title = title
        self.due_date = due_date
        self.status = "pending"
        self._description = 'No description'
        self.flag = flag
    
    def mark_completed(self):
        self.status = "completed"
    
    def __str__(self):
        return f"Task id: {self._task_id}\nTitle: {self.title}\nDue Date: {self.due_date}\nStatus: {self.status}\nDescription: {self._description}"
    
    def get_task_id(self):
        return self._task_id
    
    def set_task_id(self, task_id):
        self._task_id = task_id
    
    def get_description(self):
        return self._description
        
    def set_description(self, description):
        if(len(description) > 15):
            raise ValueError("The length is more than 15")
        self._description = description
    



class PersonalTask(Task):
    def __init__(self,title,due_date,flag="Personal", priority="low"):
        Task.__init__(self,title,due_date,flag)
        self.priority=priority
    def is_high_priority(self):
        return self.priority == "high"
    def set_priority(self,priority):
        priority_list = ["high","medium","low"]
        if(priority in priority_list):
            self.priority = priority
        else:
            print("Invalid priority was give")
    def save_to_db(self):
        conn = sqlite3.connect('task_list.db')
        try:
            conn.execute('''CREATE TABLE IF NOT EXISTS personaltasks (TASK_ID INTEGER PRIMARY KEY ,
            TASK_TYPE TEXT ,
            TITLE TEXT ,
            STATUS TEXT ,
            DUE_DATE DATETIME ,
            PRIORITY TEXT )''')
        except:
            print("Cannot create table")
        try:
            conn.execute("INSERT INTO personaltasks(TASK_ID,TASK_TYPE,TITLE,STATUS,DUE_DATE,PRIORITY) \
                    VALUES(?,?,?,?,?,?)",[self.get_task_id(), self.flag,self.title,self.status,self.due_date,self.priority])
            conn.commit()
            print("saved ")
        except:
            print("Couldn't save it ")
        conn.close()
        
    def load_from_db(self):
        conn = sqlite3.connect('task_list.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personaltasks where TASK_ID = ?",[self._task_id])
        row = cursor.fetchone()
        if row:
            print(row)
            return str(row)
        else:
            return f"ID not found: {self._task_id}"
        conn.close()
        
    def update_in_db(self):
        conn = sqlite3.connect('task_list.db')
        try:
            conn.execute("REPLACE INTO personaltasks (TASK_ID,TASK_TYPE,TITLE,STATUS,DUE_DATE,PRIORITY) VALUES(?,?,?,?,?,?)",[self.get_task_id(),self.flag,self.title,self.status,self.due_date,self.priority])
        except:
            print(f"Task ID: {self.get_task_id()} is not in the database")
        conn.commit()
        conn.close()
        
    def delete_from_db(self):
        conn = sqlite3.connect('task_list.db')
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM personaltasks WHERE TASK_ID = ?",(self.get_task_id(),))
        result = cursor.fetchone()
        conn.execute('DELETE FROM personaltasks WHERE TASK_ID = ?',[self.get_task_id(),])
        if result:
            print("deleted")
        else:
            print("not there")
        conn.commit()
        conn.close()

    def __str__(self):
        return Task.__str__(self) + f"\nPriority is: {self.priority}"


class WorkTask(Task):
    def __init__(self,title,due_date,flag="Work",team_members=[]):
        Task.__init__(self,title,due_date,flag)
        self.team_members = team_members
    def add_team_member(self,member):
        if(member.strip() == ''):
            print("Cannot add member")
            return
        self.team_members.append(member)
    def save_to_db(self):
        conn = sqlite3.connect('task_list.db')
        try:
            conn.execute('''CREATE TABLE IF NOT EXISTS worktasks (TASK_ID INTEGER PRIMARY KEY,
            TASK_TYPE TEXT ,
            TITLE TEXT ,
            STATUS TEXT ,
            DUE_DATE DATETIME )''')
        except:
            print("Cannot create table")
        try:
            conn.execute("INSERT INTO worktasks(TASK_ID,TASK_TYPE,TITLE,STATUS,DUE_DATE) \
                    VALUES(?,?,?,?,?)",[self.get_task_id(), self.flag,self.title,self.status,self.due_date])
            conn.commit()
            print("saved gang")
        except:
            print("Couldnt save it")
        conn.close()
    def load_from_db(self):
        conn = sqlite3.connect('task_list.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM worktasks where TASK_ID = ?",[self._task_id])
        row = cursor.fetchone()
        if row:
            print(row)
            return str(row)
        else:
            return f"ID not found: {self._task_id}"
        conn.close()
        
    def update_in_db(self):
        conn = sqlite3.connect('task_list.db')
        conn.execute("REPLACE INTO worktasks (TASK_ID,TASK_TYPE,TITLE,STATUS,DUE_DATE,TEAM_MEMBERS) VALUES(?,?,?,?,?,?)",[self.get_task_id(),self.flag,self.title,self.status,self.due_date,json.dumps(self.team_members)])
        conn.commit()
        conn.close()
        
    def delete_from_db(self):
        conn = sqlite3.connect('task_list.db')
        conn.execute('DELETE FROM worktasks WHERE TASK_ID = ?',[self.get_task_id()])
        conn.commit()
        conn.close()
        
    def __str__(self):
        str = f"\nTeam members are: {self.team_members}" if len(self.team_members) > 0 else "\nThere are no team members" 
        return Task.__str__(self) + str
