import tkinter as tk
from functools import partial
import json
from pathlib import Path
from main import run
import csv
import copy

data = {}
if (Path("./shows.json").exists()):
    f = open("./shows.json", "r")
    data = json.load(f)
    f.close()
# else:
#     f = open("./shows.json", "w")

window = tk.Tk()
window.geometry("500x500")
window.title("PT-Auditioners")
main_frame = tk.Frame(window, height=500, width=500)
load_frame = tk.Frame(window, height=500, width=500)
create_frame = tk.Frame(window, height=500, width=500)
run_frame = tk.Frame(window, height=500, width=500)
current_frame = main_frame
roles_list = []

def switch_frame(frame):
    global current_frame
    current_frame.pack_forget()
    frame.pack()
    current_frame = frame

def save_show(name, roles_text, error_lbl):
    global data
    global run_frame
    global window
    global show_name
    global roles_list
    error_lbl.config(text="")
    if (name.get().strip() == ""):
        error_lbl.config(text="Please name your show!")
        return
    if (name.get().strip() in data.keys()):
        error_lbl.config(text="A show with this name already exists!")
        return
    roles_list = []
    for role in roles_text.get("1.0", "end-1c").split(','):
        if (role.strip() == ""):
            error_lbl.config(text="You've created an empty role, please fix it.")
            return
        roles_list.append(role.strip())
    roles_list = list(set(roles_list))
    data[name.get()] = roles_list
    f = open("./shows.json", "w")
    json.dump(data, f)
    f.close()
    show_name.config(text=name.get())
    switch_frame(run_frame)
    # window.destroy()
    # run(role_list)

def load_show(name):
    global data
    global window
    global run_frame
    global show_name
    global roles_list
    roles_list = data[name.get()]
    show_name.config(text=name.get())
    switch_frame(run_frame)
    # window.destroy()
    # run(roles_list)

def repaint():
    global people_data
    global data_frame
    data_frame.config(state="normal")
    data_frame.delete("1.0", tk.END)
    text = ""
    for name in people_data.keys():
        text += "Name: " + name + "\n"
        text += "Roles: " + ", ".join(people_data[name]) + "\n"
        text += "\n"
    data_frame.insert('1.0', text)
    data_frame.config(state="disabled")

def restore_focus(win):
    win.grab_release()
    win.destroy()

def add_person_handler(win, name, err_lbl):
    global people_data
    if (name.get() == ""):
        err_lbl.config(text="Please enter a name!")
        return
    if (name.get() in people_data.keys()):
        err_lbl.config(text="Name already exists!")
        return
    if ("," in name.get()):
        err_lbl.config(text="Names cannot contain commas!")
        return
    people_data[name.get()] = []
    repaint()
    restore_focus(win)

def add_person():
    global window
    new_window = tk.Toplevel(window)
    new_window.title("Add Person")
    # new_window.geometry("200x100")
    new_window.grab_set()
    # Add widgets to the new window
    tk.Label(new_window, text="Enter the name of the person:").pack(pady=5)
    name = tk.Entry(new_window, width = 25, justify="center")
    name.pack(pady=5)
    error_lbl = tk.Label(new_window, text="")
    tk.Button(new_window, text="Confirm", command=partial(add_person_handler, new_window, name, error_lbl)).pack(pady=5)
    error_lbl.pack()

def add_roles_handler(win, name, role, err_lbl):
    global people_data
    if (role.get() in people_data[name.get()]):
        err_lbl.config(text="This person already has that role!")
        return
    people_data[name.get()].append(role.get())
    repaint()
    restore_focus(win)

def add_roles():
    global window
    global show_name
    global data
    global people_data
    names = list(people_data.keys())

    if (len(names) == 0):
        return
    new_window = tk.Toplevel(window)
    new_window.title("Add Roles to Person")
    new_window.grab_set()

    tk.Label(new_window, text="Select the name of the person:").pack(pady=5, padx=10)

    name = tk.StringVar(value=names[0])  

    tk.OptionMenu(new_window, name, *names).pack()

    tk.Label(new_window, text="Select the role to assign:").pack(pady=5)

    roles = list(data[show_name["text"]])

    role = tk.StringVar(value=roles[0])  
    error_lbl = tk.Label(new_window, text="")
    tk.OptionMenu(new_window, role, *roles).pack()
    tk.Button(new_window, text="Confirm", command=partial(add_roles_handler, new_window, name, role, error_lbl)).pack(pady=5)
    error_lbl.pack()

def run_cli(error_txt):
    global people_data
    global roles_list
    global window
    if (len(roles_list) == 0):
        error_txt.config(text="You have no roles!")
        return
    if (len(list(people_data.keys())) == 0):
        error_txt.config(text="You have no people!")
        return
    for name in people_data.keys():
        if len(people_data[name]) == 0:
            err = name + " has no roles!"
            error_txt.config(text=err)
            return
    window.destroy()
    run(roles_list, people_data)

def save_input(error_lbl):
    global people_data
    global show_name
    try:
        f = tk.filedialog.asksaveasfile(mode='w', defaultextension='.csv', filetypes=[("CSV File", "*.csv")])
    except Exception:
        error_lbl.config(text="An error occurred writing the file (try closing it if it's open).")
        return
    if (f == None):
        return
    f.close()
    path = f.name
    f = open(path, mode='w', newline='')
    csv_w = csv.writer(f, delimiter=",")
    csv_w.writerow([show_name["text"]])
    for name in people_data:
        csv_w.writerow([name] + people_data[name])
    f.close()

def save_template(error_lbl):
    global people_data
    global show_name
    try:
        f = tk.filedialog.asksaveasfile(mode='w', defaultextension='.csv', filetypes=[("CSV File", "*.csv")])
    except Exception:
        error_lbl.config(text="An error occurred writing the file (try closing it if it's open).")
        return
    if (f == None):
        return
    f.close()
    path = f.name
    f = open(path, mode='w', newline='')
    csv_w = csv.writer(f, delimiter=",")
    csv_w.writerow([show_name["text"]])
    csv_w.writerow(["Person 1", "Role 1", "Role 2", "etc..."])
    csv_w.writerow(["Person 2", "Role 1", "Role 2", "etc..."])
    csv_w.writerow(["Person 3", "Role 1", "Role 2", "etc..."])
    csv_w.writerow(["etc..."])
    f.close()

def load_input(error_lbl):
    global people_data
    global show_name
    global roles_list
    try:
        f = tk.filedialog.askopenfile(mode='r', filetypes=[("CSV File", "*.csv")])
    except Exception:
        error_lbl.config(text="An error occurred reading the file (try closing it if it's open).")
        return
    
    if (f == None):
        return
    temp_data = {}
    csv_r = csv.reader(f, delimiter=",")
    count = 0
    for row in csv_r:
        if count == 0:
            name = row[0]
            if (name.strip() != show_name["text"]):
                error_lbl.config(text="Show name does not match currently loaded show!")
                return
        else:
            temp_data[row[0]] = []
            for role in row[1:]:
                if (role.strip() != ""):
                    temp_data[row[0]].append(role.strip())

        count += 1
    for name in temp_data.keys():
        for role in temp_data[name]:
            if (role not in roles_list):
                err = name + "\'s role " + role + " does not exist on the currently loaded show!"
                error_lbl.config(text=err)
                return
    people_data = copy.deepcopy(temp_data)
    repaint()

button = tk.Button(
    main_frame,
    text="Load Show",
    width=20,
    height=2,
    command=partial(switch_frame, load_frame)
)

button2 = tk.Button(
    main_frame,
    text="Create New Show",
    width=20,
    height=2,
    command=partial(switch_frame, create_frame)
)

button3 = tk.Button(
    load_frame,
    text="Back",
    command=partial(switch_frame, main_frame)
)

button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=25)
button2.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=-25)

if (len(list(data.keys())) > 0):
    # Dropdown options  
    days = list(data.keys())

    # Selected option variable  
    opt = tk.StringVar(value=days[0])  

    # Dropdown menu  
    tk.OptionMenu(load_frame, opt, *days).place(relx=0.5, rely=0.5, anchor=tk.CENTER) 

    tk.Button(load_frame, text="Load", command=partial(load_show, opt)).place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=30) 
    button3.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=60)
else:
    tk.Label(load_frame, text = "You have no shows! You should probably make one.").place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    button3.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=30)

# create show frame
roles_text = tk.Text(create_frame, height = 20, width = 52)
name = tk.Entry(create_frame, width = 25, justify="center")
l = tk.Label(create_frame, text = "Create New Show")
l.config(font =("TkDefault", 20))
name_lbl = tk.Label(create_frame, text = "Enter a name for your show.")
roles_lbl = tk.Label(create_frame, text = "Enter all the roles for your show, separated by commas.")
error_lbl = tk.Label(create_frame, text = "")
cont_btn = tk.Button(create_frame, text="Continue",width=10,height=1,command=partial(save_show, name, roles_text, error_lbl))
back_btn = tk.Button(create_frame, text="Back",width=10,height=1,command=partial(switch_frame, main_frame))

l.pack()
name_lbl.pack()
name.pack()
roles_lbl.pack()
roles_text.pack()
cont_btn.pack()
back_btn.pack()
error_lbl.pack()

# run frame
people_data = {}
show_name = tk.Label(run_frame, text = "")
show_name.config(font =("TkDefault", 20))
data_frame = tk.Text(run_frame, height = 25, width = 41)
data_frame.insert('1.0', "You have no people!\nAdd a person to get started.")
data_frame.config(state="disabled")
error_text = tk.Label(run_frame, text = "", justify="center")
add_btn = tk.Button(run_frame, text="Add Person",width=20,height=2,command=add_person)
add_role = tk.Button(run_frame, text="Add Role To Person",width=20,height=2,command=add_roles)
save_btn = tk.Button(run_frame, text="Save Data",width=20,height=2, command=partial(save_input, error_text))
load_btn = tk.Button(run_frame, text="Load Data",width=20,height=2,command=partial(load_input, error_text))
save_temp_btn = tk.Button(run_frame, text="Save Template",width=20,height=2,command=partial(save_template, error_text))
run_btn = tk.Button(run_frame, text="Run (launches CLI)",width=20,height=2, command=partial(run_cli, error_text))
show_name.place(anchor="n", relx=0.5, rely=0)
data_frame.place(x=10, y=50)
add_btn.place(anchor="e", relx=0.995, rely=0.14)
add_role.place(anchor="e", relx=0.995, rely=0.24)
save_btn.place(anchor="e", relx=0.995, rely=0.34)
load_btn.place(anchor="e", relx=0.995, rely=0.44)
save_temp_btn.place(anchor="e", relx=0.995, rely=0.54)
run_btn.place(anchor="e", relx=0.995, rely=0.64)
error_text.place(relx = 0.5, rely = 0.95, anchor="center")
main_frame.pack()
window.mainloop()