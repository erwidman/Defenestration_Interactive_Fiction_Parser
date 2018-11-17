import re
import json
from modules.util import *

currInventory = []


itemSwitch = re.compile(r"(\{(?:[a-zA-Z]|\s|[.,'–])+\})(\[\d+(?:,\d+)?\])")
def parse(des):
    buf = des
    while True:
        match = itemSwitch.search(buf)
        if not match:
            break

        # print(match.start())
        requirments = json.loads(match.group(2))
        requirmentsMet = 0
        for item in currInventory:
            currID = item.get("id")
            if binary_search(requirments, currID) is not None:
                requirmentsMet += 1
                break

        if requirmentsMet == 0:
            start = match.start()
            end = start + len(match.group(1))
            buf = buf[0:start] + buf[start+1:end-1] + buf[end:]
            buf = itemSwitch.sub("", buf)
            buf = re.sub(r"(\[\d+(?:,\d+)?\])", "", buf)
            break

        else:
            buf = buf[0:match.start()] + buf[match.end():]

    customPrint(buf)


def alternatives(key,action,interactions):
    alternatives = interactions.get('alternatives')
    if alternatives is None or alternatives.get(key) is None:
        return False
    for string in alternatives.get(key):
        if string in action:
            return True
    return False


def checkManipulation(action, item, room):
    interactions = item.get("interactions")
    if interactions is None:
        return False
    for key in interactions:
        if key in action or alternatives(key,action,interactions):
            currInteraction = interactions.get(key)
            itemState = item.get("state")
            if itemState is None:
                itemState = "standard"
            current = currInteraction.get(itemState)
            text = current.get('text')
            customPrint(text)
            update = current.get("updateState")
            if update is not None:
                item["state"] = update
            reveal = current.get('revealItem')
            if reveal is not None:
                for val in reveal:
                    room.get("items").get(val).pop("hidden", None)

            return True
    return False


def look(action, room, plot):
    customPrint(room.get('description'))


def examine(action, room, plot):
    action = action.split(' ')
    obj = " ".join(action[1:])

    if room.get('fixtures').get('hidden'):
        return failPrint()

    types = {"fixtures", "items"}
    for t in types:
        for key in room.get(t):
            if obj in key:
                current = room.get(t).get(key)
                state = current.get('state')
                if state is None:
                    state = "standard"

                if current.get("used") or current.get("hidden"):
                    break
                dec = current.get('description').get(state)
                return parse(dec)

    customPrint("Wrong subject.")


def grab(action, room, plot):
    action = action.split(' ')
    obj = " ".join(action[1:])
    match = False
    for item in room.get("items"):
        currItem = room.get('items').get(item)
        if obj in item:
            if currItem.get("taken") or currItem.get("hidden"):
                continue
            else:
                customPrint(currItem.get("added"))
                match = True
                currItem['taken'] = True
                currInventory.append(currItem)

    if not match:
        failPrint()


def quit(action, room, plot):
    exit()


def inventory(action, room, plot):

    if len(currInventory) == 0:
        return customPrint("Nothing in inventory.")

    msg = "The following is in your inventory:\n"
    for item in currInventory:
        if item.get("used"):
            continue
        msg += "   - %s\n" % item.get("name")
    customPrint(msg)

def use(action,room,plot):
    print(action)


commands = {
    "look": {
        "regex": re.compile("^(?:look|l)$"),
        "invoke": look
    },
    "examine": {
        "regex": re.compile(r"\b(?:examine|x)\b [a-zA-Z]+"),
        "invoke": examine
    },
    "grab": {
        "regex": re.compile(r"\b(?:grab|take|t)\b [a-zA-Z]+"),
        "invoke": grab
    },
    "exit": {
        "regex": re.compile(r"^quit$"),
        "invoke": quit
    },
    "inventory": {
        "regex": re.compile(r"^(?:inventory|i)$"),
        "invoke": inventory
    },
    "use" : {
        "regex" : re.compile(r"(?:\buse\b ([a-zA-Z]+))|(?:\buse\b ([a-zA-Z\s]+)on ([a-zA-Z\s]+))"),
        "invoke" : use
    }
}


def searchCommands(action, room, plot):
    match = False
    for key in commands:
        curr = commands.get(key)
        if curr.get("regex").search(action):
            curr.get("invoke")(action, room, plot)
            match = True
            break

    if not match:
        fixtures = room.get('fixtures')
        for key in fixtures:
            if re.search(r"\b"+key+r"\b",action) is None:
                continue
            curr = fixtures.get(key)
            match = checkManipulation(action, curr, room)
            if match:
                break

    if not match:
        failPrint()
