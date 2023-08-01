import wx
from wx import stc
import json
import os


def convertName(name: str):
    name = name.replace(":", ".")
    name = name + ".json"
    return name

def getKeys(filename: str):
    filename = "functions_scripts/gencore/json_data/recipes/" + filename
    with open(filename) as json_file:
        listObj = json.load(json_file)

        for dictionary in listObj:
            if dictionary["dict_type"] == "keys":
                retKeys = dictionary["keys"]

    return retKeys

def getValida(filename: str, valida: str):
    filename = "functions_scripts/gencore/json_data/recipes/" + filename
    with open(filename) as json_file:
        listObj = json.load(json_file)

        for dictionary in listObj:
            if dictionary["dict_type"] == "validas":
                retValida = dictionary[valida]

    return retValida

def getDefaults(key = str):
    with open("functions_scripts/gencore/json_data/defaults.json") as json_file:
        DefDict = json.load(json_file)
        for i in DefDict:
            if i == key:
                retDef = DefDict[i]
    return retDef

def createDict(recipe_type: str):
    recipeType = recipe_type
    recipeFile = convertName(recipe_type)

    #  default dict for any future additions
    SusDict = dict(type = recipeType)

    if getValida(recipeFile, "hardIngredient") == True:
        SusDict["ingredient"] = {}
    else:
        SusDict["ingredients"] = []
    if getValida(recipeFile, "hardResult") == True:
        SusDict["result"] = "placeholder"
    else:
        SusDict["results"] = []



    Keys = getKeys(recipeFile)
    for i in Keys:
        val = getDefaults(i)
        SusDict[i] = val

    return SusDict







#print("sus")


#print(getKeys(convertName(input())))
