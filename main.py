import modules.contentControl as content
import modules.commands as commands
from modules.util import customPrint

currentRoom=0
currentPlot=0

content.loadContent()
print("\n%s" %content.title)





while True:
    room = content.rooms.get(currentRoom)
    plot = content.plot.get(currentPlot)
    if not room.get("visited"):
        room["visited"] = True
    if not plot.get("trigger"):
        plot["trigger"]=True
        customPrint(plot.get("description"))

    action=input(">> ")
    action.lower()
    commands.searchCommands(action,room,plot)




 





