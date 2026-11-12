import os
import json
from pydantic import BaseModel, Field, ValidationError
admin = True
FILE_PATH = "users_data.json"

def create_folder():
    if not os.path.exists(FILE_PATH):
        with open (FILE_PATH, "w") as f:
            data = {"users": [], "count": 0}
            json.dump(data, f, indent=4)
            
def info_verification(username, password, mode, path=FILE_PATH):
    with open(path, "r") as f:
        data = json.load(f)
    if mode.lower() == "l":
        if data["users"] == []:
            print("No user has been initialized. Please head to the register page")
            return 0
        else:
            user_data = [user for user in data["users"] if user["username"] == username]
            if user_data == []:
                print("User does not exist, please try again")
                return 0
            else:
                if user_data[0]["password"] == password:
                    print("Successful login")
                    user = Cultivator.login(user_data[0]["file_loc"], username, password)
                    return user
                else:
                    print("Wrong password")
                    return 0
    else:
        conflicts = [user for user in data["users"] if user["username"] == username]
        if conflicts == []:
            user = Cultivator.register(username, password)
            return user
        else:
            print("Username already exists")
            return 0

class Task():
    def __init__(self, name, body, ki, soul, time=None, recurring=True, d_c=0, c_t = False, fixed=True):
        self.name = name
        self.body = body
        self.ki = ki
        self.soul = soul
        self.time = time
        self.recurring = recurring
        self.d_c = d_c
        self.c_t = c_t
        self.fixed = fixed
    
        
    def schema(self):
        return {"name": self.name, "body": self.body, "ki": self.ki, "soul": self.soul, "time": self.time, "recurring": self.recurring, "d_c": self.d_c, "c_t": self.c_t, "fixed": self.fixed}
    
    def complete(self):
        self.d_c += 1
        self.c_t = True
        return {"body": self.body, "ki": self.ki, "soul": self.soul}
    

                 
class CultivationBranch():
    def __init__(self, name, exp = 0, level = 0, exp_cap = 100):
        self.name = name
        self._exp = exp
        self._level = level
        self._exp_cap = exp_cap
        
    def update(self, value):
        self._exp += value
        if self._exp >= self.exp_cap:
            self._exp -= self._exp_cap
            self._level += 1
                
        
    @property
    def exp(self):
        return self._exp
    
    @exp.setter
    def exp(self, new_exp):
        if(admin == True):
            if new_exp >= 0:
                self._exp = new_exp
                print("Set successfully")
            else:
                print("Needs to be greater than 0")
        else:
            print("You need admin access for this")
    
    @property
    def level(self):
        return self._level
        
    @level.setter
    def level(self, new_level):
        if(admin == True):
            if new_level >= 1:
                self._level = new_level
                print("Set successfully")
            else:
                print("Needs to be greater than 1")
        else:
            print("You need admin access for this")
            
    def schema(self):
        return {
            "name": self.name,
            "exp": self.exp,
            "level": self.level,
            "exp_cap": self._exp_cap
        }
    
    @property
    def exp_cap(self):
            return self._exp_cap
        
    @exp_cap.setter
    def exp_cap(self, new_exp_cap):
        if(admin == True):
            if new_exp_cap >= self._exp_cap:
                self._exp_cap = new_exp_cap
                print("Set successfully")
            else:
                print("Needs to be greater than old exp cap")
        else:
            print("You need admin access for this")

class Cultivator():
    default_tasks = [
    Task("Sleep", 5, 0, 5, time=360),
    Task("Arranging bed", 0, 0, 5),
    Task("Walk after meal", 15, 0, 0, time=5, fixed=False),
    Task("Code everyday", 0, 10, 0, fixed=False, time=5),
    Task("Embedded systems learning", 0, 10, 0, fixed=False, time=10),
    Task("Meditation", 0, 0, 10, fixed=False, time=5)
    ]
    
    def __init__(self, name, password, path, cultivation = None, tasks = default_tasks):
        self.name = name
        self._password = password
        self._tasks = tasks
        self.path = path
        self._cultivation = [CultivationBranch("body"), CultivationBranch("soul"), CultivationBranch("ki")] if cultivation == None else cultivation
        
    @property
    def tasks(self):
        return self._tasks
    
    
    def get_status(self):
        print(f"Cultivator name: {self.name}")
        print(f"Current cultivation level:")
        for i in self._cultivation:
            print(f"{i.name}: Level is {i.level}, Current exp progress is {i.exp}, Exp cap is {i.exp_cap}")
        print("Current tasks are:")
        count = 1
        for i in self._tasks:
            print(f"{count}. {i.name}")
            count+=1

    def schema(self):
        scheme = {
            "name": self.name,
            "password": self._password,
            "path": self.path,
            "tasks": [j.schema() for j in self._tasks],
            "cultivation": [i.schema() for i in self._cultivation]  
        }
        return json.dumps(scheme, indent=4)
    
    def complete(self, task_no):
        if task_no.isdigit():
            selected_task = self._tasks[int(task_no) - 1] if len(self._tasks) >= int(task_no) else None
            if selected_task == None:
                return 1
        else:
            return -1
        value = selected_task.complete()
        for branch in self._cultivation:
            if branch.name.lower() in value.keys():
                branch.update(value[branch.name])
                print(f"{branch.name} was updated")
        self.update()
        return 0
    
    def update(self):
        with open (self.path, "w") as f:
            f.write(self.schema()) 
    
    def remove_task(self, task_no):
        if task_no.isdigit():
            try:
                removed = self._tasks.pop(int(task_no)-1)
                self.update()
                print(f"{removed.name} has been deleted")
            
            except IndexError:
                print("The index you specified doesnt exist")
                
    def add_task(self, task: dict):
        self._tasks.append(Task(**task))
        self.update()
        
    @classmethod
    def login(cls, path, name, password):
        with open(path, "r") as f:
            user_data = json.load(f)
        tasks = []
        for task in user_data["tasks"]:
            tasks.append(Task(**task))
        
        cul =[]
        for c in user_data["cultivation"]:
            cul.append(CultivationBranch(**c))
        print("Okay")
        return cls(name, password, path, cul, tasks)
    
    @classmethod
    def register(cls, name, password):
        with open (FILE_PATH, "r") as f:
            users = json.load(f)
        path = "user" + str(users["count"] + 1) + ".json"
        users["users"].append({"username": name, "password": password, "file_loc": path})
        users["count"] += 1
                    
        with open (FILE_PATH, "w") as f:
            json.dump(users, f, indent=4)
        
        user = cls(name, password, path)            
        with open(path, "w") as f:
            json.dump(json.loads(user.schema()), f, indent=4)
                    
        print("Cultivator initialized")
        return user
        
        
def user_interface(user: Cultivator):
    user.get_status()
    while True:
        print("Would you like to complete, delete or add a task? Nb to exit type 'exit'")
        check = input("C - complete, D - delete, A - add: ")
        if check.lower() == "c":
            t = input("Input the number corresponding to the task: ")
            if t > 0:
                answer = user.complete(t)
            else:
                print("Input a number greater than 1")
                continue
            if answer == 0:
                print("update successful")
            elif answer == -1:
                print("Not enough tasks")
                
            else:
                print("Bad input")
            user.get_status()
        
        elif check.lower() == "d":
            t = input("Input the number corresponding to the task: ")
            user.remove_task(t)
            user.get_status()
        
        elif check.lower() == "a":
            task = {
                "name": input("Enter a name for the task: "),
                "body": 0,
                "ki": 0,
                "soul": 0,
                "time": 0,
                "recurring": True if input("Is the task recurring? True or false: ").lower() in ("true", "t", "yes", "y") else False,
                "d_c": 0,
                "c_t": 0,
                "fixed": True if input("Is the task fixed? True or false: ").lower() in ("true", "t", "yes", "y") else False
            }
            cultivation = input("Enter the body, ki and soul values for the tasks separated by space eg 0 5 0: ")
            cultivation = cultivation.split()
            cultivation = [int(i) for i in cultivation]
            task["body"], task["ki"], task["soul"] = cultivation
            user.add_task(task)
            user.get_status()
        elif check.lower() in ("exit", "break", "leave"):
            break
        else:
            print("Invalid input")
            t = input("Do you want to try again: Y/N:")
            if t.lower() == "y":
                continue
            else:
                break

       
if __name__ == "__main__":
    create_folder()
    
    while(True):
        print("Login or register?")
        answer = input("L/R: ")
        if answer.lower() in ("exit", "leave", "break"):
            break
        if answer.lower() not in ("l", "r"):
            print("invalid input")
            continue
        uname = input("Please input your username: ")
        pword = input("Please input your password: ")
        user = info_verification(uname, pword, answer.lower())
        if user:
            print("Verified")
            user_interface(user=user)
        else:
            print("Not verified")