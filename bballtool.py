import os
from tkinter import *
import imagetools as Tools


INPUT_FOLDER_NAME = 'uploadFolder'
OUTPUT_FOLDER_NAME = 'dowloadedFolder'

root = Tk()

selectTeam = Label(root, text='Select Team', bg= 'white', fg = 'black')

team = StringVar(root)

OPTIONS = [
'Atlanta Hawks',
'Boston Celtics',
'Brooklyn Nets',
'Charlotte Hornets',
'Chicago Bulls',
'Cleveland Cavaliers',
'Dallas Mavericks',
'Denver Nuggets',
'Detroit Pistons',
'Golden State Warriors',
'Houston Rockets',
'Indiana Pacers',
'Los Angeles Clippers',
'Los Angeles Lakers',
'Memphis Grizzlies',
'Miami Heat',
'Milwaukee Bucks',
'Minnesota Timberwolves',
'New Orleans Pelicans',
'New York Knicks',
'Oklahoma City Thunder',
'Orlando Magic',
'Philadelphia 76ers',
'Phoenix Suns',
'Portland Trail Blazers',
'Sacramento Kings'
'San Antonio Spurs'
'Toronto Raptors',
'Utah Jazz',
'Washington Wizards'
]
team.set(OPTIONS[0]) # default value
w = OptionMenu(root, team, *OPTIONS)
selectTeam.grid(row=1)
w.grid(row=1,column=1)


def printName():
    print('My Name is Seun Lawal')
    print("name: "+ team.get())


def add():
    Tools.add(team.get(),INPUT_FOLDER_NAME)

def show():
    Tools.show(team.get(),OUTPUT_FOLDER_NAME)


    




addButton = Button(root,text="ADD",command=add)
listButton = Button(root,text="SHOW TEAM IMAGES")
deleteButton = Button(root,text="DELETE", command=printName)

addButton.grid(row=3,column=2)
listButton.grid(row=3,column=3)
deleteButton.grid(row=3,column=4)


root.mainloop()
