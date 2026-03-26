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

runcmd() {
    while true; do
        printf "${bold}${lightgreen}Default${nc}@${lightblue}Container${nc}:~ "
        read -r cmdtorun
        
        if [[ "$cmdtorun" == "/stop" || "$cmdtorun" == "stop" ]]; then
            echo "${bold}${lightblue}Đang tắt Container...${nc}"
            exit 0
        fi
        
        if [ -f "./libraries/proot" ]; then
            ./libraries/proot -S . /bin/bash -c "$cmdtorun"
        else
            echo "Lỗi: Không tìm thấy ./libraries/proot. Vui lòng xóa file 'installed' và khởi động lại."
            exit 1
        fi
    done
}

if [[ -f "./installed" ]]; then
    echo "Done (0.000s)! For help, type \"help\""
    echo "Listening on /0.0.0.0:0"
    echo "${bold}${lightgreen}==> Started ${lightblue}Container (Debian 12)${lightgreen} <=="
    
    if [ -f "./libraries/proot" ]; then
        ./libraries/proot -S . /bin/bash -c "neofetch"
    fi
    runcmd
else
    echo "Downloading files for application (Debian 12 Update)"
    
    # Tao thu muc va tai file
    mkdir -p libraries
    curl -sSLo libs.zip https://github.com/RealTriassic/Ptero-VM-JAR/releases/download/latest/files.zip
    
    # Giai nen bang cach thuc an toan hon
    unzip -o libs.zip -d ./libraries/ >/dev/null 2>&1
    
    # Sua loi thu muc long nhau (Rat quan trong)
    if [ -d "./libraries/libraries" ]; then
        mv ./libraries/libraries/* ./libraries/
        rm -rf ./libraries/libraries
    fi
    rm -f libs.zip
    
    echo -ne '##########           (50%)\r'
    curl -sSLo debian.tar.xz https://github.com/termux/proot-distro/releases/download/v3.16.0/debian-bookworm-x86_64.tar.xz
    tar -xJf debian.tar.xz --exclude='dev' >/dev/null 2>&1
    rm -f debian.tar.xz
    
    chmod +x ./libraries/proot
    
    # Cai dat neofetch va cac cong cu
    if [ -f "./libraries/proot" ]; then
        ./libraries/proot -S . /bin/bash -c "apt-get update && apt-get install -y sudo curl wget htop nano neofetch python3"
        echo -ne '####################(100%)\r'
        echo -ne '\n'
        touch installed
        echo "Done (0.000s)! For help, type \"help\""
        ./libraries/proot -S . /bin/bash -c "neofetch"
        runcmd
    else
        echo "Lỗi nghiêm trọng: Không thể giải nén proot."
        exit 1
    fi
fi
