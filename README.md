Current schema

For the tasks class:
{
    name = Task name
    body = Task exp value for body
    ki = Task exp value for ki
    soul = Task exp value for soul
    time = duration of the task
    recurring = whether the task is recurring or one time
    d_c = days completed
    c_t = completed today
    fixed = whether the task doesnt change or gets harder gradually(eg making bed in the morning is fixed, meditation can improve as time goes on)
}

for the cultivator branch class
{
    self.name = name
        exp = current exp progress
        level = current level
        exp_cap = current exp cap
}

for the cultivator class
{
        name = cultivator name
        password = the cultivator password
        tasks = tasks that the cultiator has
        path = path to the file containing the user data
        cultivation = a list containing the three cultivation branches and their data    
}

do note that some of the attributes and schema have yet to be used