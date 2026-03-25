#!/bin/bash

HOME="/home/container"
HOMEA="$HOME/linux/.apt"

# Toi uu hoa duong dan thu vien cho Debian moi
export LD_LIBRARY_PATH="$HOMEA/usr/lib/x86_64-linux-gnu:$HOMEA/usr/lib:$HOMEA/lib/x86_64-linux-gnu:$HOMEA/lib:$HOMEA/usr/local/lib"
export PATH="/bin:/usr/bin:/usr/local/bin:/sbin:$HOMEA/bin:$HOMEA/usr/bin:$HOMEA/sbin:$HOMEA/usr/sbin:$HOMEA/etc/init.d:$PATH"
export BUILD_DIR=$HOMEA

bold=$(echo -en "\e[1m")
nc=$(echo -en "\e[0m")
lightblue=$(echo -en "\e[94m")
lightgreen=$(echo -en "\e[92m")

echo "
${bold}${lightgreen}========================================================================
                                                                                                  
${bold}${lightblue}@@@@@@@   @@@@@@@  @@@@@@@@  @@@@@@@    @@@@@@      @@@  @@@  @@@@@@@@@@
${bold}${lightblue}@@@@@@@@  @@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@     @@@  @@@  @@@@@@@@@@@    
${bold}${lightblue}@@!  @@@    @@!    @@!       @@!  @@@  @@!  @@@     @@!  @@@  @@! @@! @@!    
${bold}${lightblue}!@!  @!@    !@!    !@!       !@!  @!@  !@!  @!@     !@!  @!@  !@! !@! !@!     
${bold}${lightblue}@!@@!@!     @!!    @!!!:!    @!@!!@!   @!@  !@!     @!@  !@!  @!! !!@ @!@      
${bold}${lightblue}!!@!!!      !!!    !!!!!:    !!@!@!    !@!  !!!     !@!  !!!  !@!   ! !@!        
${bold}${lightblue}!!:         !!:    !!:       !!: :!!   !!:  !!!     :!:  !!:  !!:     !!:        
${bold}${lightblue}:!:         :!:    :!:       :!:  !:!  :!:  !:!      ::!!:!   :!:     :!:            
${bold}${lightblue} ::          ::     :: ::::  ::   :::  ::::: ::       ::::    :::     ::        
${bold}${lightblue} :           :     : :: ::    :   : :   : :  :         :       :      :          
                                                                                                  
                                                                                                                
${bold}${lightgreen}========================================================================
 "
 
echo "${nc}"

if [[ -f "./installed" ]]; then
    echo "${bold}${lightgreen}==> Started ${lightblue}Container${lightgreen} <=="
    function runcmd1 {
        printf "${bold}${lightgreen}Default${nc}@${lightblue}Container${nc}:~ "
        read -r cmdtorun
        ./libraries/proot -S . /bin/bash -c "$cmdtorun"
        runcmd
    }
    function runcmd {
        printf "${bold}${lightgreen}Default${nc}@${lightblue}Container${nc}:~ "
        read -r cmdtorun
        ./libraries/proot -S . /bin/bash -c "$cmdtorun"
        runcmd1
    }
    runcmd
else
    echo "Downloading files for application (Debian 12 Update)"
    
    # Tai proot va cac cong cu ho tro
    curl -sSLo libraries.zip https://github.com/RealTriassic/Ptero-VM-JAR/releases/download/latest/files.zip >/dev/null 2>err.log
    echo -ne '###                 (15%)\r'
    
    # Tai RootFS Debian 12 moi nhat (x86_64)
    curl -sSLo debian.tar.xz https://github.com/termux/proot-distro/releases/download/v3.16.0/debian-bookworm-x86_64.tar.xz >/dev/null 2>err.log
    echo -ne '#######             (35%)\r'
    
    curl -sSLo unzip https://raw.githubusercontent.com/afnan007a/Ptero-vm/main/unzip >/dev/null 2>err.log
    chmod +x unzip
    ./unzip libraries.zip >/dev/null 2>err.log
    echo -ne '##########          (50%)\r'
    
    # Giai nen Debian 12
    tar -xJf debian.tar.xz --exclude='dev' >/dev/null 2>err.log
    echo -ne '#############       (65%)\r'
    
    chmod +x ./libraries/proot >/dev/null 2>err.log
    
    # Don dep file tam
    rm -rf libraries.zip debian.tar.xz unzip >/dev/null 2>err.log
    echo -ne '#################   (85%)\r'

    # Thiet lap ban dau cho Debian moi
    cmds=(
        "apt-get update"
        "apt-get install -y sudo curl wget htop nano neofetch python3 python3-pip"
        "echo 'root:root' | chpasswd"
    )

    for cmd in "${cmds[@]}"; do
        ./libraries/proot -S . /bin/bash -c "$cmd >/dev/null 2>err.log"
    done
    
    echo -ne '####################(100%)\r'
    echo -ne '\n'
    touch installed
    
    echo "
${bold}${lightgreen}========================================================================
                                                                                                  
${bold}${lightblue}@@@@@@@   @@@@@@@  @@@@@@@@  @@@@@@@    @@@@@@      @@@  @@@  @@@@@@@@@@
${bold}${lightblue}@@@@@@@@  @@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@     @@@  @@@  @@@@@@@@@@@    
${bold}${lightblue}@@!  @@@    @@!    @@!       @@!  @@@  @@!  @@@     @@!  @@@  @@! @@! @@!    
${bold}${lightblue}!@!  @!@    !@!    !@!       !@!  @!@  !@!  @!@     !@!  @!@  !@! !@! !@!     
${bold}${lightblue}@!@@!@!     @!!    @!!!:!    @!@!!@!   @!@  !@!     @!@  !@!  @!! !!@ @!@      
${bold}${lightblue}!!@!!!      !!!    !!!!!:    !!@!@!    !@!  !!!     !@!  !!!  !@!   ! !@!        
${bold}${lightblue}!!:         !!:    !!:       !!: :!!   !!:  !!!     :!:  !!:  !!:     !!:        
${bold}${lightblue}:!:         :!:    :!:       :!:  !:!  :!:  !:!      ::!!:!   :!:     :!:            
${bold}${lightblue} ::          ::     :: ::::  ::   :::  ::::: ::       ::::    :::     ::        
${bold}${lightblue} :           :     : :: ::    :   : :   : :  :         :       :      :          
                                                                                                  
                                                                                                                
${bold}${lightgreen}========================================================================
 "
 
    echo "${nc}"
    echo "${bold}${lightgreen}==> Started ${lightblue}Container (Debian 12)${lightgreen} <=="
    
    function runcmd1 {
        printf "${bold}${lightgreen}Default${nc}@${lightblue}Container${nc}:~ "
        read -r cmdtorun
        ./libraries/proot -S . /bin/bash -c "$cmdtorun"
        runcmd
    }
    function runcmd {
        printf "${bold}${lightgreen}Default${nc}@${lightblue}Container${nc}:~ "
        read -r cmdtorun
        ./libraries/proot -S . /bin/bash -c "$cmdtorun"
        runcmd1
    }
    runcmd
fi
