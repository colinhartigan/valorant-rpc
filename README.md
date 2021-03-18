not working on v1 anymore in favor of v2, but if there's any big bugs i'll try to fix them

# valorant-rich-presence-client

Discord rich presence extension for VALORANT

[*Jump to updating*](https://github.com/colinhartigan/valorant-rich-presence/blob/main/README.md#updating)

![](https://media.discordapp.net/attachments/357677064507228171/815690033842880552/unknown.png)
![](https://media.discordapp.net/attachments/357677064507228171/815690322591613008/unknown.png)
![](https://media.discordapp.net/attachments/357677064507228171/815690580386381834/unknown.png)

# Installation
> Following these instructions will result in the program automatically launching with VALORANT

*NOTE: Upon downloading, your browser might mark the file as dangerous, but this is a false-positive and can be ignored (all the code is open-source)*
### Part 1: Creating a folder for the executable
1. Create a folder for the extension; this folder should be stored somewhere safe where it will not be moved
    - it is recommended to create a folder in C:\Program Files\ called "valorant-rpc"
2. Move the executable to the folder created in step 1 

NOTE: Antivirus/Windows Defender might mark the executable as a **potentially unwanted app**, this is a false-positive

**Windows Defender:** Select *Allow on device* and *Start actions* to allow the extension to run
![](https://user-images.githubusercontent.com/42125428/109581460-5439f900-7aca-11eb-86f4-26bae7bae501.png)

3. Copy the path to the executable for a later step
    - if the folder was made under "C:\Program Files\valorant-rpc", the path would be "C:\Program Files\valorant-rpc\valorant-rpc.exe"
### Part 2: Changing the VALORANT launch target

1. Locate the VALORANT shortcut
    - if you typically launch from your desktop, locate the VALORANT icon
    - if you typically launch from the search bar, search for VALORANT and open the file location

2. Right click on the shortcut/icon, then select **Properties**

![image](https://user-images.githubusercontent.com/42125428/109582766-bdbb0700-7acc-11eb-914e-40a46e139494.png)

3. In the **Target** box, paste the path to *valorant-rpc.exe* from [part 1, step 3](https://github.com/colinhartigan/valorant-rich-presence/blob/main/README.md#part-1-creating-a-folder-for-the-executable), then select **Apply**

![image](https://user-images.githubusercontent.com/42125428/109582870-eba04b80-7acc-11eb-8748-7de9376a8e81.png)

4. Launch VALORANT! The console will appear and launch the game, then minimize to the system tray.


# Updating
1. Navigate to the folder created in [part 1, step 3](https://github.com/colinhartigan/valorant-rich-presence/blob/main/README.md#part-1-creating-a-folder-for-the-executable) of installation
2. Delete the old valorant-rpc.exe and replace it with the new executable

NOTE: Antivirus might flag the new executable as malware; follow the same steps outlined in [part 1, step 2](https://github.com/colinhartigan/valorant-rich-presence/blob/main/README.md#part-1-creating-a-folder-for-the-executable) of installation
