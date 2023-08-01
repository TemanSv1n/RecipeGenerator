import json
import logging
import webbrowser

import wx
from wx import stc

#import functions_scripts.gencore.recipeGen
from functions_scripts import styledTextCtrlFormat, darkmode  # StyledTextCtrl black bg & json lexer
from functions_scripts.gencore import recipeGen
#print(MyDict)


# Ids
APP_EXIT = 1
APP_DARK = 2

"""Car interaction"""


def pCin():
    with open("car.json", 'w') as json_file:
        json.dump(wnd.MyDict, json_file,
                  indent=4,
                  separators=(',', ': '))
        #wnd.panel.tvc.SaveFile(filename="car.json")
        print(wnd.MyDict)

def pCout():
    with open("car.json") as json_file:
        wnd.MyDict = json.load(json_file)
        #wnd.panel.tvc.LoadFile(filename= "car.json")
        print(wnd.MyDict)


"""car & text ctrl sync"""
def pRefresh():
    #pCin()
    try:
        wnd.panel.tvc.SaveFile(filename="car.json")
    except json.JSONDecodeError:
        print("no way")
    else:
        pCout()
    finally:
        print(wnd.MyDict)



def pSync():
    pCout()
    wnd.panel.tvc.LoadFile(filename="car.json")

def pDictRefresh():
    pCin()
    pSync()

def AddEntry():
    l = wnd.panel
    wnd.EntryDict = dict()
    # item/fluid key
    if l.agg_choice.GetSelection() == 0:
        print("ok!")
        if l.tag_choice.GetSelection() == 0:
            print("ok Tag!")
            wnd.EntryDict["item"] = l.iden_text.GetValue()
        elif l.tag_choice.GetSelection() == 1:
            wnd.EntryDict["tag"] = l.iden_text.GetValue()
    elif l.agg_choice.GetSelection() == 1 and l.pot_choice.GetSelection() == 0:
        if l.tag_choice.GetSelection() == 0:
            wnd.EntryDict["fluid"] = l.iden_text.GetValue()
        elif l.tag_choice.GetSelection() == 1:
            wnd.EntryDict["fluidTag"] = l.iden_text.GetValue()
    elif l.agg_choice.GetSelection() == 1 and l.pot_choice.GetSelection() == 1:
        wnd.EntryDict["fluid"] = "create:potion"
        wnd.EntryDict["nbt"] = dict(Bottle = "REGULAR", Potion = l.iden_text.GetValue())
    #count/amount key
    if l.quan_text.GetValue() != "":
        if l.agg_choice.GetSelection() == 0:
            wnd.EntryDict["count"] = int(l.quan_text.GetValue())
        elif l.agg_choice.GetSelection() == 1:
            wnd.EntryDict["amount"] = int(l.quan_text.GetValue())
    #chance key
    if l.chance_text.GetValue() != "":
        wnd.EntryDict["chance"] = float(l.quan_text.GetValue())

    #wnd.EntryDict["item"] = "sus"
    print(wnd.EntryDict)
    print(l.tag_choice.GetSelection())
    print(l.iden_text.GetValue())

    #Adding
    if l.inp_choice.GetSelection() == 0:
        if recipeGen.getValida(recipeGen.convertName(wnd.MyDict["type"]), "hardIngredient") == True:
            wnd.MyDict["ingredient"] = wnd.EntryDict
        else:
            if recipeGen.getValida(recipeGen.convertName(wnd.MyDict["type"]), "multipleIngredients") == False:
                listd = wnd.MyDict["ingredients"]
                if listd:
                    listd[0] = wnd.EntryDict
                    wnd.MyDict["ingredients"] = listd
                else:
                    listd.append(wnd.EntryDict)
                    wnd.MyDict["ingredients"] = listd
            else:
                listd = wnd.MyDict["ingredients"]
                listd.append(wnd.EntryDict)
                wnd.MyDict["ingredients"] = listd
    elif l.inp_choice.GetSelection() == 1:
        if recipeGen.getValida(recipeGen.convertName(wnd.MyDict["type"]), "hardResult") == True:
            wnd.MyDict["result"] = l.iden_text.GetValue()
        else:
            if recipeGen.getValida(recipeGen.convertName(wnd.MyDict["type"]), "multipleResults") == False:
                listd = wnd.MyDict["results"]
                if listd:
                    listd[0] = wnd.EntryDict
                    wnd.MyDict["results"] = listd
                else:
                    listd.append(wnd.EntryDict)
                    wnd.MyDict["results"] = listd
            else:
                listd = wnd.MyDict["results"]
                listd.append(wnd.EntryDict)
                wnd.MyDict["results"] = listd

    print(wnd.EntryDict)
    pDictRefresh()



class InputContextMenu(wx.Menu):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()

        it_dlg_open = self.Append(wx.ID_ANY, "Enter recipe type")
        self.Bind(wx.EVT_MENU, self.onDlgOpen, it_dlg_open)

    def onDlgOpen(self, event):
        dlg = wx.TextEntryDialog(self.parent, "Enter recipe type", "Recipe Type", "create:milling")
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            wnd.MyDict = recipeGen.createDict(dlg.GetValue())
            pDictRefresh()
            wnd.panel.choicesLogics()

class MyPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.defaultColor = self.GetBackgroundColour()
        darkmode.darkMode(self, self.defaultColor)

        panel = self

        # creating light gray panel and sizer
        tvp = wx.Panel(panel)
        tvp.SetBackgroundColour('#454545')
        tvpbox = wx.BoxSizer()
        tvpbox.Add(tvp, wx.ID_ANY, flag=wx.RIGHT | wx.TOP | wx.EXPAND, border=10)
        # sizer
        panel.SetSizer(tvpbox)  # needed
        # sizer 2 for TVC (text ctrl)
        tvpbox2 = wx.BoxSizer(wx.HORIZONTAL)
        tvp.SetSizer(tvpbox2)
        self.tvc = wx.stc.StyledTextCtrl(tvp, style=wx.TE_MULTILINE|wx.TE_RICH|wx.HSCROLL) #text ctrl, idk why .self
# Choice !
        chbox = wx.BoxSizer(wx.VERTICAL)
        txbox = wx.BoxSizer(wx.VERTICAL) #  Not actually choice, it's for text fields
        tvpbox2.Add(chbox, wx.ID_ANY, flag=wx.RIGHT | wx.TOP, border=10)
        tvpbox2.Add(txbox, wx.ID_ANY, flag=wx.TOP, border=10)

        self.inp_choice = wx.Choice(tvp, choices=["Ingredient", "Result"], validator=wx.DefaultValidator)
        self.inp_choice.SetSelection(0)
        chbox.Add(self.inp_choice, proportion = 10, flag=wx.LEFT | wx.TOP, border=5)
        self.Bind(wx.EVT_CHOICE, self.onChosen, self.inp_choice)

        self.agg_choice = wx.Choice(tvp,choices = ["Item", "Fluid"], validator=wx.DefaultValidator)
        chbox.Add(self.agg_choice, proportion = 10, flag=wx.LEFT | wx.TOP, border=5)
        self.agg_choice.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.onChosen, self.agg_choice)

        self.tag_choice = wx.Choice(tvp, choices=["Name", "Tag"], validator=wx.DefaultValidator)
        chbox.Add(self.tag_choice, proportion=10, flag=wx.LEFT | wx.TOP, border=5)
        self.tag_choice.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.onChosen, self.tag_choice)

        self.pot_choice = wx.Choice(tvp, choices=["Basic", "Potion"], validator=wx.DefaultValidator)
        chbox.Add(self.pot_choice, proportion=10, flag=wx.LEFT | wx.TOP, border=5)
        self.pot_choice.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.onChosen, self.pot_choice)
# Choice ^
# TextFields !
        self.quan_text = wx.TextCtrl(tvp, name = "quantity")
        txbox.Add(self.quan_text, proportion = 10, flag=wx.LEFT | wx.TOP, border=5)
        self.quan_tp = wx.StaticText(tvp, label = "Quantity", pos = self.quan_text.GetPosition())
        txbox.Add(self.quan_tp, proportion=10, flag=wx.LEFT | wx.TOP, border=5)

        self.chance_text = wx.TextCtrl(tvp, name="chance")
        txbox.Add(self.chance_text, proportion=10, flag=wx.LEFT | wx.TOP, border=5)
        self.chance_tp = wx.StaticText(tvp, label="Chance", pos=self.chance_text.GetPosition())
        txbox.Add(self.chance_tp, proportion=10, flag=wx.LEFT | wx.TOP, border=5)

        self.iden_text = wx.TextCtrl(tvp, name="ident")
        txbox.Add(self.iden_text, proportion=10, flag=wx.LEFT | wx.TOP, border=5)
        self.iden_tp = wx.StaticText(tvp, label="Identificator", pos=self.chance_text.GetPosition())
        txbox.Add(self.iden_tp, proportion=10, flag=wx.LEFT | wx.TOP, border=5)
# TextFields ^




        tvpbox2.Add(self.tvc, wx.ID_ANY, flag=wx.LEFT | wx.EXPAND, border=-100, )

        #json lexer & dark bg. !this values needed there!
        self.tvc.SetLexer(stc.STC_LEX_JSON)
        #there are just stc.JSON_*STYLES* in one line
        styleList = [1, 32, stc.STC_JSON_DEFAULT, stc.STC_JSON_NUMBER, stc.STC_JSON_KEYWORD, stc.STC_JSON_STRING, stc.STC_JSON_PROPERTYNAME, stc.STC_JSON_BLOCKCOMMENT, stc.STC_JSON_COMPACTIRI, stc.STC_JSON_ERROR, stc.STC_JSON_ESCAPESEQUENCE, stc.STC_JSON_LDKEYWORD, stc.STC_JSON_LINECOMMENT, stc.STC_JSON_OPERATOR, stc.STC_JSON_STRINGEOL, stc.STC_JSON_URI]
        #methods from funcs_scripts
        styledTextCtrlFormat.stcf_SetBlackBg(self.tvc, styleList)
        styledTextCtrlFormat.stcf_SetJsonFormat(self.tvc)


        # creating a sizer for the ing/res type combobox

        # rtcbox = wx.BoxSizer
        # tvp.SetSizer(rtcbox)

    def choicesLogics(self):
        if wnd.MyDict["type"]:
            #item-liquid
            if recipeGen.getValida(recipeGen.convertName(wnd.MyDict["type"]), "items") == False:
                self.agg_choice.SetSelection(1)
                self.agg_choice.Enable(False)
            elif recipeGen.getValida(recipeGen.convertName(wnd.MyDict["type"]), "fluids") == False:
                self.agg_choice.SetSelection(0)
                self.agg_choice.Enable(False)
            else:
                self.agg_choice.Enable(True)
            #name-tag
            if self.pot_choice.GetSelection() == 1 or (recipeGen.getValida(recipeGen.convertName(wnd.MyDict["type"]), "hardResult") == True and self.inp_choice.GetSelection == 1):
                self.tag_choice.SetSelection(0)
                self.tag_choice.Enable(False)
            else:
                self.tag_choice.Enable(True)
            #basic-potion
            if self.agg_choice.GetSelection() == 0 or self.tag_choice.GetSelection() == 1:
                self.pot_choice.SetSelection(0)
                self.pot_choice.Enable(False)
            else:
                self.pot_choice.Enable(True)
            #chances
            if self.inp_choice.GetSelection() == 1:
                if self.agg_choice.GetSelection() == 1 or self.pot_choice.GetSelection() == 1 or (self.agg_choice.GetSelection() == 0 and recipeGen.getValida(recipeGen.convertName(wnd.MyDict["type"]), "chances") == False):
                    self.chance_text.SetValue("")
                    self.chance_text.Enable(False)
                else:
                    self.chance_text.Enable(True)
            else:
                self.chance_text.Enable(False)
            #quantity
            if self.agg_choice.GetSelection() == 0:
                if self.inp_choice.GetSelection() == 0:
                    if recipeGen.getValida(recipeGen.convertName(wnd.MyDict["type"]), "countIngredient") == False:
                        self.quan_text.SetValue("")
                        self.quan_text.Enable(False)
                    else:
                        self.quan_text.Enable(True)
                elif self.inp_choice.GetSelection() == 1:
                    if recipeGen.getValida(recipeGen.convertName(wnd.MyDict["type"]), "countResult") == False:
                        self.quan_text.SetValue("")
                        self.quan_text.Enable(False)
                    else:
                        self.quan_text.Enable(True)
            else:
                self.quan_text.Enable(True)



        # if self.agg_choice.GetSelection() == 2:
        #     self.tag_choice.SetSelection(0)
        #     self.tag_choice.Enable(False)
        # else:
        #     self.tag_choice.Enable(True)

    def onChosen(self, event):
        self.choicesLogics()


    def onToggleDark(self):
        """"""
        darkmode.darkMode(self, self.defaultColor)


class Window(wx.Frame):
    def __init__(self, parent, title, size):
        super().__init__(parent, title=title, size=size)
        self.Centre()
        self.panel = MyPanel(self)
        self.Show(True)
        self.MyDict = {"cock": 15}
        self.EntryDict = {}



#menu
        menubar = wx.MenuBar()
        fileMenu = wx.Menu() #file menu

        exitItem = fileMenu.Append(APP_EXIT, "Exit", "Esc the app") #Exit item \tCtrl+E
        fileMenu.AppendSeparator()


        menubar.Append(fileMenu, "File")
        self.SetMenuBar(menubar)

#Binds
        self.Bind(wx.EVT_MENU, self.onQuit, exitItem)

#Toolba

        toolbar = self.CreateToolBar(wx.TB_LEFT)
        tb_initi = toolbar.AddTool(wx.ID_ANY, "Json initialization", wx.Bitmap("assets/icon_add_32.png"))
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        tb_refresh = toolbar.AddTool(wx.ID_ANY, "Json Refresh", wx.Bitmap("assets/icon_upload_32.png"))
        tb_sync = toolbar.AddTool(wx.ID_ANY, "Json Sync", wx.Bitmap("assets/icon_download_32.png"))
        tb_debug_dict = toolbar.AddTool(wx.ID_ANY, "Dict debug", wx.Bitmap("assets/icon_refresh_32.png"))
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        tb_add_entry = toolbar.AddTool(wx.ID_ANY, "Add Entry", wx.Bitmap("assets/icon_add_entry_32.png"))
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        toolbar.AddSeparator()
        tb_question = toolbar.AddTool(wx.ID_ANY, "Question", wx.Bitmap("assets/icon_question_32.png"))

        self.Bind(wx.EVT_MENU, self.onIniti, tb_initi)
        self.Bind(wx.EVT_MENU, self.onRefresh, tb_refresh)
        self.Bind(wx.EVT_MENU, self.onSync, tb_sync)
        self.Bind(wx.EVT_MENU, self.onDictRefresh, tb_debug_dict)
        self.Bind(wx.EVT_MENU, self.onAddEntry, tb_add_entry)
        self.Bind(wx.EVT_MENU, self.onQuestion, tb_question)


        toolbar.Realize()



#Text view panel



        """Sus"""
        self.Maximize()
        self.Maximize(False)
        """Sus"""



    def onDebug(self, event):
        print(self.MyDict)
    def onQuit(self, event):
        self.Close()

    def onIniti(self, event):
        self.ppm = InputContextMenu(parent=self)
        self.PopupMenu(self.ppm)

    def onRefresh(self, event):
        pRefresh()

    def onSync(self, event):
        pSync()
        #print(MyDict)

    def onDictRefresh(self, event):
        pDictRefresh()
        #print(self.panel.inp_choice.GetSelection())

    def onAddEntry(self, event):
        AddEntry()

    def onQuestion(self, event):
        webbrowser.open_new_tab("https://stackoverflow.com/questions/29508872/how-to-use-webbrowser-to-open-the-link-when-it-is-clicked-in-wxpython-frame")

app = wx.App()
wnd = Window(None, "Recipe gen", size = (760,480))
app.MainLoop()


#EntraDict generates pretty cool, but it doesn't wantto write into a MyDict// Method AddEntry(), #Adding