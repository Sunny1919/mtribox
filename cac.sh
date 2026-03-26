#!/bin/bash

HOME="/home/container"
HOMEA="$HOME/linux/.apt"
export LD_LIBRARY_PATH="$HOMEA/usr/lib/x86_64-linux-gnu:$HOMEA/usr/lib:$HOMEA/lib/x86_64-linux-gnu:$HOMEA/lib"
export PATH="/bin:/usr/bin:/usr/local/bin:/sbin:$HOMEA/bin:$HOMEA/usr/bin:$HOMEA/sbin:$HOMEA/usr/sbin:$PATH"

bold=$(echo -en "\e[1m")
nc=$(echo -en "\e[0m")
lightblue=$(echo -en "\e[94m")
lightgreen=$(echo -en "\e[92m")

# Banner ASCII Art
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

# Ham xu ly lenh terminal
runcmd() {
    while true; do
        printf "${bold}${lightgreen}Default${nc}@${lightblue}Container${nc}:~ "
        read -r cmdtorun
        
        # Kiem tra neu nguoi dung nhap /stop
        if [[ "$cmdtorun" == "/stop" ]]; then
            echo "${bold}${lightblue}Đang tắt Container theo yêu cầu...${nc}"
            exit 0
        fi
        
        # Chay lenh thong qua proot
        ./libraries/proot -S . /bin/bash -c "$cmdtorun"
    done
}

if [[ -f "./installed" ]]; then
    # Thong bao trang thai Online cho Pterodactyl
    echo "Done (0.000s)! For help, type \"help\""
    echo "Listening on /0.0.0.0:0"
    echo "${bold}${lightgreen}==> Started ${lightblue}Container (Debian 12)${lightgreen} <=="
    
    # Tu dong chay neofetch khi khoi dong
    ./libraries/proot -S . /bin/bash -c "neofetch"
    
    runcmd
else
    echo "Downloading files for application (Debian 12 Update)"
    
    mkdir -p libraries
    curl -sSLo libs.zip https://github.com/RealTriassic/Ptero-VM-JAR/releases/download/latest/files.zip
    unzip -q libs.zip -d ./libraries/ || python3 -m zipfile -e libs.zip ./libraries/
    
    if [ -d "./libraries/libraries" ]; then
        mv ./libraries/libraries/* ./libraries/
        rm -rf ./libraries/libraries
    fi
    rm -rf libs.zip
    
    echo -ne '##########           (50%)\r'
    curl -sSLo debian.tar.xz https://github.com/termux/proot-distro/releases/download/v3.16.0/debian-bookworm-x86_64.tar.xz
    tar -xJf debian.tar.xz --exclude='dev' >/dev/null 2>&1
    rm debian.tar.xz
    
    chmod +x ./libraries/proot
    
    # Cai dat neofetch va cac cong cu
    cmds=(
        "apt-get update"
        "apt-get install -y sudo curl wget htop nano neofetch python3"
    )

    for cmd in "${cmds[@]}"; do
        ./libraries/proot -S . /bin/bash -c "$cmd >/dev/null 2>&1"
    done

    echo -ne '####################(100%)\r'
    echo -ne '\n'
    touch installed
    
    echo "${bold}${lightgreen}Cài đặt hoàn tất! Đang khởi động...${nc}"
    echo "Done (0.000s)! For help, type \"help\""
    
    ./libraries/proot -S . /bin/bash -c "neofetch"
    runcmd
fi
