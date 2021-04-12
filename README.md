### another rewrite (v3) coming after I finish my [API wrapper](https://github.com/colinhartigan/valclient.py); should be much more optimized and clean

Please read through the README in its entirety before creating issues/messaging me!

```
 _    _____    __    ____  ____  ___    _   ________            ____  ____  ______
| |  / /   |  / /   / __ \/ __ \/   |  / | / /_  __/           / __ \/ __ \/ ____/
| | / / /| | / /   / / / / /_/ / /| | /  |/ / / /    ______   / /_/ / /_/ / /     
| |/ / ___ |/ /___/ /_/ / _, _/ ___ |/ /|  / / /    /_____/  / _, _/ ____/ /___   
|___/_/  |_/_____/\____/_/ |_/_/  |_/_/ |_/ /_/             /_/ |_/_/    \____/   
```

# valorant-rich-presence-client
A feature-rich Discord rich-presence extension for VALORANT.


## Images
![image](https://user-images.githubusercontent.com/42125428/112060312-64764e80-8b33-11eb-843b-2bb457b39a31.png)
![image](https://user-images.githubusercontent.com/42125428/112060125-22e5a380-8b33-11eb-9bbe-5cc9fa5605df.png)
![image](https://user-images.githubusercontent.com/42125428/112060228-4c063400-8b33-11eb-9701-1ff403d7b916.png)
![image](https://user-images.githubusercontent.com/42125428/112060347-73f59780-8b33-11eb-8881-27d291ff9eac.png)


## Installation
> Antivirus might mark the installer executable as malicious, you can run it anyway

For most of you, select **Install for all users**; you'll know if you want to select the other option.

![image](https://user-images.githubusercontent.com/42125428/112061391-d13e1880-8b34-11eb-9b69-c81d43f080b8.png)

If you get a Windows notification from User Account Control, choose yes

![image](https://user-images.githubusercontent.com/42125428/112061494-f16dd780-8b34-11eb-9ffd-c8910cb7c254.png)

Take note or copy of the path to your installation, you'll need it later!

![image](https://user-images.githubusercontent.com/42125428/112074255-4c5ef900-8b4c-11eb-91ae-8cb7340fe970.png)

During installation, you have a decision to make: *"do I want the program to automatically launch with VALORANT (recommended), or do I want to manually launch it every time I play?"*. 
**If you chose the second option**, it is recommended you create a desktop shortcut, otherwise, ignore that option.

![image](https://user-images.githubusercontent.com/42125428/112061652-309c2880-8b35-11eb-9144-b90a0d73be44.png)

It is recommended you run the program after installing; it runs a few first-time setup tasks.


## Editing the configuration
Navigate to %APPDATA%\valorant-rpc and open config.json with your favorite text editor
> press CTRL+R, type *%APPDATA%\valorant-rpc* then press enter

### settings
- `launch_timeout`: time, in seconds, the program should wait for VALORANT to launch. if the time passes before the game fully loads, the program will exit
- `menu_refresh_interval`: how often, in seconds, the program should update your Discord presence while in the menus
- `ingame_refresh_interval`: how often, in seconds, the program should update your Discord presence while in a game 
- `debug`: set to true to show a traceback when the program crashes (useful for bug reports!)

### region
- change this to your client's region, can be found in settings -> about -> game shard

### rpc-oauth
- leave this section blank; it stores the application's Discord authentication data

### rpc-client-override
- leave this section unchanged UNLESS you are setting up your own Discord application to share with friends so you can use the party invites feature. [Read more about it here](https://github.com/colinhartigan/valorant-rpc/wiki/Creating-a-Discord-Application-for-VALORANT-RPC)


## Restarting the application
> this **DOES NOT** close/restart VALORANT

After editing the configuration, locate the tray icon, right click it, and select **restart**
![image](https://user-images.githubusercontent.com/42125428/112065554-3268ea80-8b3b-11eb-928a-9cdb92b9dbb1.png)

The console window will reappear for a few seconds and the program will restart


## Modifying the VALORANT launch target

This section is for the *"I want the program to automatically launch with VALORANT"* people from earlier

1. Locate the VALORANT shortcut
    - if you typically launch from your desktop, locate the VALORANT icon
    - if you typically launch from the search bar, search for VALORANT and open the file location
    - you can also do this for every VALORANT shortcut you have

2. Right click on the shortcut/icon, then select **Properties**

![image](https://user-images.githubusercontent.com/42125428/109582766-bdbb0700-7acc-11eb-914e-40a46e139494.png)

3. In the **Target** box, paste the path to *valorant-rpc.exe* from when you installed (ex. `C:\Program Files (x86)\valorant-rpc\valorant-rpc.exe`), then select **Apply**

![image](https://user-images.githubusercontent.com/42125428/112066464-c38c9100-8b3c-11eb-8e37-96a0b36cb9bc.png)

4. Launch VALORANT! The program console should appear for a few seconds before the game launches.

## Legal Stuff
**This project is not affiliated with Riot Games or any of its employees and therefore does not reflect the views of said parties. This is purely a fan-made project to enhance VALORANT's Discord integration.**

Riot Games does not endorse or sponsor this project. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
