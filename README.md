# Casualties-Unknown-External-Mod-Manager
An externally managed mod manager for the game Casualties Unknown. Looks in the Plugins folder for Bepinex for mods and modfolders, and creates an info.json and a unusedMods folder for disabled mods. Has a feature for organizing mods, defining them, and customizable presets

# Setup:
Simply drop your Operating system's CUMMgr file into the Bepinex folder (NOT the plugins folder) and run! It's as simple as that. When you first run it, it will create two to three files; a plugins (if it doesn't exist yet) and unusedPlugins folder, and an info.json savedata file. Here should be what you first see, if you have some mods already installed!

<img width="642" height="753" alt="image" src="https://github.com/user-attachments/assets/1eda83f6-98cb-4ddf-81b0-8de96e4ba4f8" />


# Folders and Controlling Mods
These four buttons all control the Mod organization and utility:

<img width="644" height="84" alt="image" src="https://github.com/user-attachments/assets/d86a0ed9-c4d9-4ea5-9045-7e6e513c1101" />

## Refresh Window
Simply closes and reopens the program. Whenever adding, deleting, or moving a mod, this will make it appear in the list. Much easier than doing it manually.

## Add Folder
Now, this is where things get complicated.
Folders aren't actual filepaths in this program. Folders simply help with organization and nothing else. It includes one of the two things that are synced by Plugins (see further), and is very useful especially when dealing with a lot of different types of mods.
When creating a folder, simply type in the name you want and press "Enter" or click "Create". And tada! An empty folder hath been born!
Folders other than the base Uncategorized folder has a "Delete" button that, once completing a confirm dialog will delete the folder and move all it's contents to the base Uncategorized folder.
Categorizing every mod will result in the hiding of the now empty Uncategorized folder.
For example, here's some basic folders for some basic mods:

<img width="600" height="653" alt="image" src="https://github.com/user-attachments/assets/bfc6e1e5-30f9-4c53-acb3-b6548ae4370e" />

## Apply Mod Changes
What you've all been waiting for: how this mod manager manages your mods!
Instead of directly smacking BepInEx whenever it tries to use a disabled mod, CUMMgr simply moves the shit out of the way. It's that simple. BepInEx stays happy, and your mods still get managed how you want.

To disable a mod, uncheck one of the Green mods:

<img width="565" height="57" alt="image" src="https://github.com/user-attachments/assets/bc045da8-b1ae-41ee-bd7c-433b70dbdbad" />

to make it highlighted red:

<img width="565" height="65" alt="image" src="https://github.com/user-attachments/assets/04ab5d0e-1943-46d3-82e2-e062039db287" />

And vice versa for any disabled mods:

<img width="560" height="59" alt="image" src="https://github.com/user-attachments/assets/f6400823-8f92-4425-9800-9d6ad333afed" />

<img width="564" height="56" alt="image" src="https://github.com/user-attachments/assets/313bcf59-15ac-497a-9ac4-3794ddd97198" />

Once you have your mods properly selected, simply click the "Apply Mod Changes" button. CUMMgr will refresh, and your mods will have moved to their desired places.
Note: make sure to finalize changes before closing or doing any action that would refresh the program, as this <ins>will</ins> clear your selections away. So be careful. And yes, this is a result of my laziness.

## Move Mods in Folders
Remember those folders? Now we get to actually use them!
<ins>Once you have __created__ some folders,</ins> click this to have a menu pop up with every single mod in a neat list. Simply select the dropdown, put the mod in the desired folder, and tada! Once you confirm the folder, it will automatically refresh with your mod now in the folder you chose. Allows for changing more than one mod's folder at a time (it's best to do them all at once to get it out of the way)

<img width="483" height="678" alt="image" src="https://github.com/user-attachments/assets/dd0f845f-034d-4afb-bc7f-33b7bbf1432f" />

## Extra: Descriptions
Every mod has an "edit description" button which allows you to fully define a mod's utility inside the mod manager. Simple, yet useful when dealing with strange names or random Assets folders

<img width="563" height="58" alt="image" src="https://github.com/user-attachments/assets/2a1ae9f9-cb70-402a-8a1c-7dfd3c08e126" /><br>

<img width="361" height="269" alt="image" src="https://github.com/user-attachments/assets/2113af12-0681-4929-a527-81c1b0ad0269" />


# Presets Row
This is where things get very complicated.
There are only two things saved in each preset: 
- Mods and their active/disabled state
- Folders and the mods that reside inside
## WARNING
It is __REQUIRED__ for EVERY mod that was existent on the last preset save to remain in the two Mod directories. If any changes are made, the presets must be recreated. This is best done by loading them with the mod you wish to remove, then saving them with said mod actually removed.

<img width="619" height="83" alt="image" src="https://github.com/user-attachments/assets/19651281-6f21-47fe-ba40-240e546ddb5c" />

## Create/Edit
This is the bread and butter right here. Simply click, type in a name, and save whatever you have currently set. Do whatever you need, then if you'd like to return, follow the later steps and tada.
To __EDIT__ an existing preset, type in the exact same name of that preset in the Save/Edit box, then click Create. This essentially overwrites the preset with what you have currently set, which is useful for me since I don't have to code a full on editing system for these.

<img width="336" height="207" alt="image" src="https://github.com/user-attachments/assets/85ababbc-8da6-49db-b839-82ba3a419125" />

## Load Preset
Fairly simple. All you have to do is select your desired preset in the dropdown and click Load. It will check for matching modlists (which is why it's important to have identical mods) and then load in the saved disabled/enabled variables and the Folder variables for each mod. Lastly, it refreshes, and tada!

<table>
  <tr>
    <td align="center">
      <h3>Saved Preset</h3>
      <img width="1041" height="773" alt="image" src="https://github.com/user-attachments/assets/ac408ff9-31ae-48a2-b307-4066ea7f02fa" /><br>
    </td>
    <td align="center">
      <h3>Changes Made</h3>
      <img width="640" height="751" alt="image" src="https://github.com/user-attachments/assets/50956a44-b844-4cde-a4fc-5264041a1f06" /><br>
    </td>
    <td align="center">
      <h3>Reloading Preset</h3>
      <img width="639" height="753" alt="image" src="https://github.com/user-attachments/assets/ca188f6c-03fa-4a3b-b8d0-d79c98be2e87" /><br>
    </td>
  </tr>
</table>

## Delete Preset
Lastly, there is deleting a preset. Simple as it gets; select the preset you want gone and confirm in the popup. It will reload to the Default preset, so make sure that it is either empty or filled with what you want.
Note: Will not be able to delete the Default Preset. Doing so would break my already messy ass code, so I simply made it impossible instead of fixing it.


# For Developers

I severely apologize for my downright disgusting code. I got lost halfway through but the bones I built at the start got me through the confusion, for a little while.
If you have any questions, ask away. And any bugs goes to the Issues tab.
Also, the behavior of the manager for discovering mods is NOT recursive; what this means to non-developers is that instead of looking in folders for mod files, CUMMgr simply takes the whole folder that the mod resides in. Prevents issues like missing assets and stuffs, and some mods require a folder environment to run. While it's an easy solution, it can make it hard to find out what certain mods are; for example, the Assets folder in my CUMMgr modlist is for CUResprite.dll

# Known Windows/Linux Scrolling Bug
On Linux, there simply is no way to scroll on scrollable menus. As a linux main, I feel your x11 pain.
On windows (at least on the install I'm using, Windows 10) has a very odd bug, where it does allow you to scroll but with odd visual artifacts to boot. Nothing crazy or damaging, but can be annoying when scrolling through a lot of mods.
