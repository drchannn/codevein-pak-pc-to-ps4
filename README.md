## PAK PC TO PS4 MOD Converter Tool (by drchannn) #

Simple tool for convert pc pak files to ps4 pak files from games that use UnrealEngine 4.x

### Tested on: ###
- CodeVein
- Soul Calibur 4
- Kena: Bridge of Spirits


### Requisites: ###
- orbis-image2gnf (You need to get by your own, this is part of SDK Sony)
- umodel (https://www.gildor.org/en/projects/umodel)
- unrealpak (You can get from unrealengine, that can be installed from epic software)

### How to use: ###
- Simple dran n drop a PAK file to program, select profile that game for this pak file and wait to a new PAK file was generated.

### Options (ini file): ###
- CHECK_REQUISITES - (Default Value is 1) - If is set to 1 program check that requisites are installed, if u want skip this set to 0
- AUTO_SET_PROFILE - (Default Value is 0) - If is set to 1 program save last profile used and dont ask anymore for profile selection. If program detect an error saving or exporting files from PAK file, program will clear profile saved and show again profile selection
- PAUSE_STEP - (Default Value is 0) - If u want that every step program do a pause set to 1. I think that is util for debug or replace files
- PAUSE_FINISH - (Default Value is 1) - If is set to 1 program do a pause on finish work, if dont want this set to 0
- PAK_COMPRESS - (Default Value is 0) - If is set to 1 new PAK file was compressed. I dont know what is better, test yourself

### Profiles: ###
- On tools folder, there is a subfolder called profiles. On this there is a text files with a two values for every game, unreal engine version and unreal engine game path. If your game dont appear you can to create for ur game with correct values. (If you do this please send me to put on repo)

### To-Do: ###
- Read better uexp, uasset files
- Testing more games and resources
