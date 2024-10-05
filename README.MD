# Inno Setup Unpacker Extractor and Rebuild by Arch
### Oct 2024 Work In Progress
Fairly close to done, a few small issues remain.

Project
* Extract inno setup and rebuild file structure by architecture
* Dynamically detect if/which arch are present by parsing the iss

ehhhhhhhh

heres the comment block

    Inno Setup Unpacker Script v4.20
    --------------------------------
    Built on innounp by quickener
    https://innounp.sourceforge.net/
    
    This script extracts Inno Setup installer files using 'innounp.exe'. It dynamically processes
    the files and directories, identifies variants (e.g., x64, ARM64), and copies them into 
    architecture-specific output directories.
    
    After processing the script will output a fully built directory for each detected architecture,
    as well as the raw extracted setup.
    
    Key Features:
    - Automatically handles extraction of setup files using innounp.
    - Processes metadata from the .iss script.
    - Dynamically detects and categorizes file variants (x64, ARM64, etc.).
    - Outputs a structured summary with logging support.
    
    Usage:
    1. With file argument:
       python innounpakNrebuild.py --file "inno_setup_file.exe"
    
    2. Without file argument (prompts user):
       python innounpakNrebuild.py
    
    Requirements:
    - 'innounp.exe' must be located in the 'bin' directory.
    - Python 3.x with the following libraries:
        - os, subprocess, shutil, re, datetime, logging, argparse, platform, colorama

Current dishues:
* If setup does not define super explicitly define each arch, it gets confused. So far I have only found 1 installer that has done this.
* Output may look slightly confusing? If the setup doesn't have multiple architectures. I hate UI, don't ask me.
* Have not addressed directories outside of the main 'app' dir, in theroy... shouldn't make a difference.... but... yeah. ymmv.

Demo output:
(Small easy test setup can be found with this cool project https://github.com/moudey/Shell)

    Innoup executable path: C:\Demo\bin\innounp.exe
    Inno Setup File: setup2.exe
    
    ###[ Starting InnoSetup Unpacking Process ]###
    ---------------------------------------------------
    
    ===[ Setting up Environment ]===
    
    Moved setup2.exe to C:\Demo\tmp_setup2_20241005_181354
    Working directory set to C:\Demo\tmp_setup2_20241005_181354\setup2_extracted
    
    ===[ Extracting Inno Setup ]===
    
    ; Version detected: 6100 (Unicode)
    #1 {app}\shell,1.dll
    Reading slice C:\Demo\tmp_setup2_20241005_181354\setup2.exe
    #2 {app}\shell,1.exe
    #3 {app}\shell,2.dll
    #4 {app}\shell,2.exe
    #5 {app}\shell,3.dll
    #6 {app}\shell,3.exe
    #7 {app}\readme.txt
    #8 {app}\shell.nss
    #9 {app}\imports\develop.nss
    #10 {app}\imports\file-manage.nss
    #11 {app}\imports\goto.nss
    #12 {app}\imports\images.nss
    #13 {app}\imports\modify.nss
    #14 {app}\imports\taskbar.nss
    #15 {app}\imports\terminal.nss
    #16 {app}\imports\theme.nss
    #17 install_script.iss
    Initial Extraction Finished
    
    ===[ Parsing ISS File and Processing Files ]===
    
    
    Found Variants and Architecture Mapping:
      Variant 1 -> x64
      Variant 2 -> ARM64
      Variant 3 -> Other
    
    ===[ Building Output Directories ]===
    
    Mapping files detected by arch...
    Copied C:\Demo\tmp_setup2_20241005_181354\setup2_extracted\app\shell,1.dll (Variant: x64)
    Copied C:\Demo\tmp_setup2_20241005_181354\setup2_extracted\app\shell,1.exe (Variant: x64)
    Copied C:\Demo\tmp_setup2_20241005_181354\setup2_extracted\app\shell,2.dll (Variant: ARM64)
    Copied C:\Demo\tmp_setup2_20241005_181354\setup2_extracted\app\shell,2.exe (Variant: ARM64)
    Copied C:\Demo\tmp_setup2_20241005_181354\setup2_extracted\app\shell,3.dll (Variant: Other)
    Copied C:\Demo\tmp_setup2_20241005_181354\setup2_extracted\app\shell,3.exe (Variant: Other)
    Mapping common files...
    
    
    Starting file operations...
    
    Copied shell,1.dll (Variant: x64)
    Copied shell,1.exe (Variant: x64)
    Copied shell,2.dll (Variant: ARM64)
    Copied shell,2.exe (Variant: ARM64)
    Copied shell,3.dll (Variant: Other)
    Copied shell,3.exe (Variant: Other)
    Copied common file install_script.iss
    Copied common file install_script.iss
    Copied common file install_script.iss
    Copied common file readme.txt
    Copied common file readme.txt
    Copied common file readme.txt
    Copied common file shell.nss
    Copied common file shell.nss
    Copied common file shell.nss
    Copied common file develop.nss
    Copied common file develop.nss
    Copied common file develop.nss
    Copied common file file-manage.nss
    Copied common file file-manage.nss
    Copied common file file-manage.nss
    Copied common file goto.nss
    Copied common file goto.nss
    Copied common file goto.nss
    Copied common file images.nss
    Copied common file images.nss
    Copied common file images.nss
    Copied common file modify.nss
    Copied common file modify.nss
    Copied common file modify.nss
    Copied common file taskbar.nss
    Copied common file taskbar.nss
    Copied common file taskbar.nss
    Copied common file terminal.nss
    Copied common file terminal.nss
    Copied common file terminal.nss
    Copied common file theme.nss
    Copied common file theme.nss
    Copied common file theme.nss
    
    Moving setup2.exe
    
    Working directory set to C:\Demo
    
    finished!
    
    ###[ Unpacking and Rebuild Complete ]###
    
    ---------------------------------------------------
    
    
    #####--- Extraction Summary ---#####
    
    ------------------------------------
    App Name: Nilesoft Shell
    App Version: 1.9.15
    App Publisher: Nilesoft
    App Support URL: https://nilesoft.org
    App Comments: Nilesoft Shell Setup
    
    Variants Processed:
      Variant 1 -> x64
      Variant 2 -> ARM64
      Variant 3 -> Other
    
    Output Directories by Arch Created:
      C:\Demo\tmp_setup2_20241005_181354\Output_x64
      C:\Demo\tmp_setup2_20241005_181354\Output_ARM64
      C:\Demo\tmp_setup2_20241005_181354\Output_Other
    
    Output Directory with raw unpack:
      C:\Demo\tmp_setup2_20241005_181354\setup2_extracted
    
    
    Script completed successfully
    
    
    
    PS C:\Demo>





