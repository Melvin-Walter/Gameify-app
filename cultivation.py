import os
import json

admin = True
FILE_PATH = "users_data.json"
class Task():
    def __init__(self, name, body, ki, soul, time=None, recurring=True, d_c=1, fixed=True):
        self.name = name
        self.body = body
        self.ki = ki
        self.soul = soul
        self.time = time
        self.recurring = recurring
        self.d_c = 1
        self.fixed = fixed
    
    def schema(self):
        return {"name": self.name, "body": self.body, "ki": self.ki, "soul": self.soul, "time": self.time, "recurring": self.recurring, "d_c": self.d_c, "fixed": self.fixed}
    

                 
class CultivationBranch():
    def __init__(self, name, exp = 0, level = 0):
        self.name = name
        self._exp = exp
        self._level = level
        
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
            "level": self.level
        }

class Cultivator():
    default_tasks = [
    Task("Sleep", 5, 0, 5, time=360),
    Task("Arranging bed", 0, 0, 5),
    Task("Walk after meal", 15, 0, 0, time=5, fixed=False),
    Task("Code everyday", 0, 10, 0, fixed=False, time=5),
    Task("Embedded systems learning", 0, 10, 0, fixed=False, time=10),
    Task("Meditation", 0, 0, 10, fixed=False, time=5)
    ]
    def __init__(self, name, password, cultivation = None, tasks = default_tasks):
        self.name = name
        self._password = password
        self._tasks = tasks
        self._cultivation = [CultivationBranch("Body"), CultivationBranch("Spirit"), CultivationBranch("Ki")] if cultivation == None else cultivation
        
    @property
    def tasks(self):
        return [i.schema() for i in self._tasks]
    
    def get_status(self):
        print(f"Cultivator name: {self.name}")
        print(f"Current cultivation level:")
        for i in self._cultivation:
            print(f"{i.name}: Level is {i.level}, Current exp progress is {i.exp}")

    def schema(self):
        scheme = {
            "name": self.name,
            "password": self._password,
            "tasks": [j.schema() for j in self._tasks],
            "cultivation": [i.schema() for i in self._cultivation]  
        }
        return json.dumps(scheme, indent=4)
    
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
        return cls(name, password, cul, tasks)
    
    @classmethod
    def register(cls, name, password):
        with open (FILE_PATH, "r") as f:
            users = json.load(f)
        path = "user" + str(users["count"] + 1) + ".json"
        users["users"].append({"username": name, "password": password, "file_loc": path})
        users["count"] += 1
                    
        with open (FILE_PATH, "w") as f:
            json.dump(users, f, indent=4)
        
        user = cls(name, password)            
        with open(path, "w") as f:
            json.dump(json.loads(user.schema()), f, indent=4)
                    
        print("Cultivator initialized")
        return user
        
        
    

       
if __name__ == "__main__":
    if not os.path.exists(FILE_PATH):
        with open (FILE_PATH, "w") as f:
            data = {"users": [], "count": 0}
            json.dump(data, f, indent=4)
            f.close()
    
    
    while(True):
        print("Login or register?")
        answer = input("L/R: ")
        if(answer.upper() == "L"):
            uname = input("Please input your username: ")
            pword = input("Please input your password: ")
            with open(FILE_PATH, "r") as f:
                users = json.load(f)
                user = [i for i in users["users"] if i["username"] == uname and i["password"] == pword]
                if user == []:
                    print("User does not exist or wrong password")
                else:
                    user_current = Cultivator.login(user[0]["file_loc"], uname, pword)           
        
        elif(answer.upper() == "R"):
            print("Welcome new user.")
            uname = input("Enter a username to get started: ")
            pword = input("Enter a password: ")
            user = Cultivator.register(uname, pword)
            print("Successful registration")
            stat = input("Would you like to view your status? Y/N")
            if stat.upper() == "Y":
                user.get_status()
                
        elif(answer.lower() in ("exit", "stop", "break")):
            break
        
        else:
            print("Invaild entry. Please enter either l or r")