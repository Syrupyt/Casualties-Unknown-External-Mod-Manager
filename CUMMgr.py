import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from pathlib import Path
import json, os, sys, shutil

ctk.set_appearance_mode('Dark')

app = ctk.CTk()
app.title("CUMMgr")
app.geometry("640x720")


if getattr(sys, 'frozen', False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent


INFO_FILE = APP_DIR / "info.json"
PLUGINS_DIR = APP_DIR / "plugins"
UNUSED_DIR = APP_DIR / "unusedPlugins"
DEFAULT_INFO = {
    "modList": {},
    "modDescriptions": {},
    "modFolders": {},
    "presets": {
        "Default": {}
    },
    "setPreset": "Default"
}

def initialize():
    PLUGINS_DIR.mkdir(exist_ok=True)
    UNUSED_DIR.mkdir(exist_ok=True)

    if INFO_FILE.exists():
        try:
            with INFO_FILE.open("r") as f:
                info = json.load(f)
        except (json.JSONDecodeError, TypeError):
            info = {}
    else:
        info = {}

    for key, default in DEFAULT_INFO.items():
        info.setdefault(key, default)

    with INFO_FILE.open("w") as f:
        json.dump(info, f, indent=4)

    return info


info = initialize()

with INFO_FILE.open("r") as f:
    info = json.load(f)

#Check mods
reboot = False
def refreshModList():
    if reboot:
        with open("info.json", "w") as infofile:
            json.dump(info, infofile, indent=4)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    activemodlist = [x.name for x in PLUGINS_DIR.iterdir()]
    disabledmodlist = [x.name for x in UNUSED_DIR.iterdir()]
    info["modList"] = {}
    for mod in activemodlist:
        info["modList"][mod] = True
    for mod in disabledmodlist:
        info["modList"][mod] = False
    for mod in activemodlist:
        info["modDescriptions"].setdefault(mod, "")
    for mod in disabledmodlist:
        info["modDescriptions"].setdefault(mod, "")
    with open("info.json", "w") as infofile:
        json.dump(info, infofile, indent=4)
    
refreshModList()
reboot = True


# -- Header -- #

#Buttons

#Frame
topframe = ctk.CTkFrame(app, fg_color="transparent")
topframe.pack(fill="x", padx=20, pady=15)
tf_label = ctk.CTkLabel(master=topframe, text="Presets:  Saves mod toggles and folders --- REQUIRES THE SAME MODS")
tf_label.pack(padx=10, pady=10)

#Create preset
def createPreset():
    query = ctk.CTkInputDialog(text="Name your Preset\nTo edit a preset's info, set the same name below\nNote: Preset names can't be changed once created!", title="Preset Name")
    name = query.get_input()
    if name != None and name.strip() != '':
        info["setPreset"] = name
        info["presets"][name] = {"modList": info["modList"], "modFolders": info["modFolders"]}
        refreshModList()
create_preset = ctk.CTkButton(topframe, text="Create/Edit", command=createPreset)
create_preset.pack(side="left", padx=5)

#Load preset
def loadPreset():
    selectedPreset = presetwheel.get()
    if not selectedPreset in info["presets"].keys():
        selectedPreset = 'Default'
        info["presets"][selectedPreset] = {"modList": info["modList"], "modFolders": info["modFolders"]}
    if info["presets"][selectedPreset] or info["presets"][selectedPreset] != {}:
        if not all([mod in info["presets"][selectedPreset]["modList"] for mod in info["modList"]]):
            errorstr = ''
            for mod in info["modList"]:
                if not mod in info["presets"][selectedPreset]["modList"]:
                    errorstr += '- ' + mod + '\n'
            errormsg = CTkMessagebox(
                            title="Warning", 
                            message=f"These mods are either not in the proper directories or the preset doesn't have them\nAdd or overwrite to fix:\n\n" + errorstr, 
                            icon="warning", 
                            option_1="Close")
            return None
        enabledMods = []
        disabledMods = []
        for obj in zip(sorted(list(info["modList"])), sorted(list(info["presets"][selectedPreset]["modList"]))):
            current, preset = obj
            currentvar, presetvar = (info["modList"][current], info["presets"][selectedPreset]["modList"][preset])
            if currentvar != presetvar and current == preset:
                #print(f"Name: {current}, Value: {currentvar}, Compared: {preset}: {presetvar}, Enumerate: {x}")
                if currentvar:
                    disabledMods.append(current)
                else:
                    enabledMods.append(current)
        info['modFolders'] = info['presets'][selectedPreset]['modFolders']
        info['setPreset'] = selectedPreset
        refreshMods(enabledMods, disabledMods)
load_preset = ctk.CTkButton(topframe, text="Load Preset", command=loadPreset)
load_preset.pack(side="left", padx=5)

#delete preset
def deletePreset():
    selectedPreset = presetwheel.get()
    if selectedPreset == 'Default':
        warnmsg = CTkMessagebox(
            title="Failed", 
            message=f'Deleting the default preset would break things.\nOverwriting is allowed; simply make what you want and save.', 
            icon="warning", 
            option_1="Cancel")
        return None
    warnmsg = CTkMessagebox(
                    title="Are you sure?", 
                    message=f'Are you sure you want to permanently delete the preset "{selectedPreset}"?\n\nThis cannot be undone (without a backup)!', 
                    icon="warning", 
                    option_1="DELETE", 
                    option_2="Cancel")
    if warnmsg.get() == 'DELETE':
        del info['presets'][selectedPreset]
        info["setPreset"] = 'Default'
        loadPreset()
delete_preset = ctk.CTkButton(topframe, text="Delete Selected", command=deletePreset)
delete_preset.pack(side="left", padx=5)

#Dropdown
current_preset = ctk.StringVar(value=info["setPreset"] if info["setPreset"] in info["presets"].keys() else "Default")
presetwheel = ctk.CTkOptionMenu(topframe, values=list(info["presets"].keys()), variable=current_preset)
presetwheel.pack(side="left", padx=5)

# Horizontal separator
separator = ctk.CTkFrame(app, height=2, fg_color=("gray70", "gray30"))
separator.pack(fill="x", padx=20, pady=15)


# -- Mod and Folder Classes -- #
class Folder:
    def __init__(self, name, scrollframe):
        self.name = name
        if name in info["modFolders"]:
            self.mods = info["modFolders"][name]
        else:
            self.mods = list(info["modList"].keys())
            for folder in info["modFolders"].values():
                for mod in folder:
                    if mod in self.mods:
                        self.mods.remove(mod)

        self.frame = ctk.CTkFrame(scrollframe, fg_color="#00284D")
        self.frame.pack(fill="x", padx=5, pady=10)

        self.titleFrame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.titleFrame.pack(fill="x", padx=5, pady=5)

        self.label = ctk.CTkLabel(master=self.titleFrame, text=self.name, font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(side="left", padx=10, pady=10)

        def delete():
            msg = CTkMessagebox(
                title="Are you sure?", 
                message=f'Are you sure you want to permanently delete the folder "{self.name}"?\n\nNote: Deleting a folder with mods inside will default to "Uncategorized" while not delete the mods inside', 
                icon="warning", 
                option_1="DELETE", 
                option_2="Cancel",
                height=250,
                width=500)
            if msg.get() == "DELETE":
                del info["modFolders"][self.name]
                refreshModList()

            
        if self.name != "Uncategorized":
            self.button = ctk.CTkButton(self.titleFrame, text="Delete", command=delete)
            self.button.pack(side="right", padx=10, pady=10)
        else:
            if self.mods == []:
                self.frame.destroy()
        
class MyInputDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Input", text="Enter value:", preset=""):
        super().__init__(parent)
        self.title(title)
        self.geometry("360x240")
        self.resizable(False, False)
        self.lift()
        self.focus_force()
        
        # Make the dialog modal
        self.transient(parent)
        self.grab_set()
        
        self.value = None

        # Label
        self.label = ctk.CTkLabel(self, text=text)
        self.label.pack(padx=20, pady=(20, 10))

        # Multiline Textbox with preset text
        self.textbox = ctk.CTkTextbox(self, width=410, height=80)
        self.textbox.pack(padx=20, pady=5, fill="both", expand=True)
        self.textbox.insert("1.0", preset)  
        self.textbox.focus()

        # Submit Button
        self.btn = ctk.CTkButton(self, text="OK", command=self.on_ok)
        self.btn.pack(padx=20, pady=(10, 20))

    def on_ok(self):
        self.value = self.textbox.get("1.0", "end-1c")
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self.value

    
enabledMods = []
disabledMods = [] 


class Mod:
    def __init__(self, name, folders, uncategorized):
        self.name = name
        self.enabled = info["modList"][name]
        self.original = self.enabled
        self.description = info["modDescriptions"][self.name]
        self.folder = uncategorized.frame
        for f_frame, folder in folders.items():
            if self.name in folder.mods:
                self.folder = folders[f_frame].frame
        
        
        self.frame = ctk.CTkFrame(self.folder, fg_color="#065f21" if self.enabled else "#5f0621")
        self.frame.pack(fill="x", padx=5, pady=5)

        modNameFont = ctk.CTkFont(family="Arial", size=13)
        self.label = ctk.CTkLabel(master=self.frame, text=self.name, font=modNameFont)
        self.label.pack(side="left", padx=10, pady=10)

        self.checkboxvar = ctk.BooleanVar(value=self.enabled)
        self.checkbox = ctk.CTkCheckBox(self.frame, text='', command=self.toggle, variable=self.checkboxvar, width=24)
        self.checkbox.pack(side="right", padx=10, pady=10)

        self.descedit = ctk.CTkButton(self.frame, text="Edit desc.", width=10, command=self.editDesc)
        self.descedit.pack(side="right", padx=5, pady=10)

        self.descframe = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.descframe.pack(fill="x", expand=True, padx=5, pady=5)

        nameSize = modNameFont.measure(self.label.cget('text'))
        self.descobj = ctk.CTkLabel(master=self.descframe, text=self.description, wraplength=(-1.018*nameSize + 400), font=("Arial", 10, "italic"))
        self.descobj.pack()

    def editDesc(self):
        name = MyInputDialog(app, title="Edit description", text=f"Type in the description for the mod: \n{self.name}\nFormatting is done automatically", preset=self.description)
        nameInput = name.get_input()
        if nameInput != None:
            info["modDescriptions"][self.name] = nameInput
            refreshModList()

    def toggle(self):
        self.enabled = self.checkboxvar.get()
        if self.original and self.enabled:
            self.frame.configure(fg_color="#065f21")
        elif self.original and not self.enabled:
            self.frame.configure(fg_color="#bd023a") 
        elif not self.original and self.enabled:
            self.frame.configure(fg_color="#1fbb00")
        else:    
            self.frame.configure(fg_color="#5f0621") 

        if self.enabled:       
            if not self.name in enabledMods:
                enabledMods.append(self.name)
                if self.name in disabledMods:
                    disabledMods.remove(self.name)
            else:
                enabledMods.remove(self.name)              
        else:
            if not self.name in disabledMods:
                disabledMods.append(self.name)
                
                if self.name in enabledMods:
                    enabledMods.remove(self.name)
            else:
                disabledMods.remove(self.name)
                

#Move mods when modRefresh is triggered
def refreshMods(enabledModsPreset=None, disabledModsPreset=None):
    for mod in enabledModsPreset if enabledModsPreset != None else enabledMods:
        source = UNUSED_DIR / mod
        dest = PLUGINS_DIR / mod

        shutil.move(source, dest)

    for mod in disabledModsPreset if disabledModsPreset != None else disabledMods:
        source = PLUGINS_DIR / mod
        dest = UNUSED_DIR / mod

        shutil.move(source, dest)

    refreshModList()


#Open a simple prompt window to CREATE a folder
def queryCreateFolder():
    name = ctk.CTkInputDialog(text="Type in your folder name:", title="Create a folder")
    nameInput = name.get_input()
    if nameInput != None and nameInput.strip() != '':
        info["modFolders"][nameInput] = []
        refreshModList()

#Open a complicated custom window to MOVE mods in folders
class ModOrganizer:
    def __init__(self, name, frame):
        self.name = name
        self.folder = "uncategorized"
        for folder, mod in info["modFolders"].items():
            if self.name in mod:
                self.folder = folder

        self.frame = ctk.CTkFrame(frame, fg_color="#00449c")
        self.frame.pack(fill="x", padx=5, pady=5)
        
        self.label = ctk.CTkLabel(master=self.frame, text=self.name, wraplength=250)
        self.label.pack(side="left", padx=10, pady=10)

        self.folderVar = ctk.StringVar(value=self.folder)
        self.folderSelector = ctk.CTkOptionMenu(self.frame, values=["uncategorized"] + list(info["modFolders"].keys()), variable=self.folderVar)
        self.folderSelector.pack(side="right", padx=5)

def customMoveFolder():
    window = ctk.CTkToplevel(app)
    window.title("Move mods")
    window.geometry("480x640")
    window.attributes("-topmost", True)
    window.after(10, lambda: window.attributes("-topmost", False))
    window.focus_force()

    title = ctk.CTkLabel(master=window, text="Change mod folders", font=ctk.CTkFont(size=16, weight="bold"))
    title.pack(padx=10, pady=10)

    separator = ctk.CTkFrame(window, height=2, fg_color=("gray70", "gray30"))
    separator.pack(fill="x", padx=20, pady=15)

    scrollFrame = ctk.CTkScrollableFrame(window)
    scrollFrame.pack(fill="both", expand=True, padx=10, pady=10)

    modList = []
    for mod in sorted(list(info["modList"])):
        modList.append(ModOrganizer(mod, scrollFrame))

    def confirmChanges():
        for mod in modList:
            if mod.folder != mod.folderVar.get():
                if mod.folder != "uncategorized":
                    info["modFolders"][mod.folder].remove(mod.name)
                if mod.folderVar.get() != "uncategorized":
                    info["modFolders"][mod.folderVar.get()].append(mod.name)
        window.destroy()
        refreshModList()


    saveChanges = ctk.CTkButton(window, text="Save changes", command=confirmChanges)
    saveChanges.pack(side="left", padx=5, pady=10)



#Buttons
bottomFrame = ctk.CTkFrame(app, height=50, fg_color="transparent")
bottomFrame.pack(fill="x", padx=20, pady=5)
refreshButton = ctk.CTkButton(bottomFrame, text="Refresh Window", command=refreshModList)
refreshButton.pack(side="left", padx=5, pady=10)
addFolderButton = ctk.CTkButton(bottomFrame, text="Add Folder", command=queryCreateFolder)
addFolderButton.pack(side="left", padx=5, pady=10)
refreshModButton = ctk.CTkButton(bottomFrame, text="Apply Mod Changes", command = refreshMods)
refreshModButton.pack(side="left", padx=5, pady=10)
customizeFolders = ctk.CTkButton(bottomFrame, text="Move Mods in Folders", command=customMoveFolder)
customizeFolders.pack(side="left", padx=5, pady=10)

modframe = ctk.CTkScrollableFrame(app)
modframe.pack(fill="both", expand=True, padx=20, pady=20)



folders = {}
for folder in info["modFolders"]:
    folders[folder] = Folder(folder, modframe)

uncategorized = Folder("Uncategorized", modframe)

for mod in sorted(list(info["modList"])):
    Mod(mod, folders, uncategorized)


app.mainloop()

