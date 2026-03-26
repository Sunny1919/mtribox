#!/bin/bash

# Thiết lập biến môi trường
HOME="/home/container"
HOMEA="$HOME/linux/.apt"
export LD_LIBRARY_PATH="$HOMEA/usr/lib/x86_64-linux-gnu:$HOMEA/usr/lib:$HOMEA/lib/x86_64-linux-gnu:$HOMEA/lib"
export PATH="/bin:/usr/bin:/usr/local/bin:/sbin:$HOMEA/bin:$HOMEA/usr/bin:$HOMEA/sbin:$HOMEA/usr/sbin:$PATH"

bold=$(echo -en "\e[1m")
nc=$(echo -en "\e[0m")
lightblue=$(echo -en "\e[94m")
lightgreen=$(echo -en "\e[92m")

# Banner ASCII Art (Giữ nguyên giao diện của bạn)
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
 ::          ::     :: ::::  ::   :::  ::::: ::       ::::    :::     ::        
 :           :     : :: ::    :   : :   : :  :         :       :      :          
                                                                                                  
                                                                                                                
${bold}${lightgreen}========================================================================
 "
echo "${nc}"

# Hàm xử lý lệnh terminal và lệnh /stop
runcmd() {
    while true; do
        printf "${bold}${lightgreen}Default${nc}@${lightblue}Container${nc}:~ "
        read -r cmdtorun
        
        if [[ "$cmdtorun" == "/stop" || "$cmdtorun" == "stop" ]]; then
            echo "${bold}${lightblue}Đang tắt Container...${nc}"
            exit 0
        fi
        
        # Chạy lệnh qua proot với đường dẫn tuyệt đối để tránh lỗi
        $HOME/libraries/proot -S . /bin/bash -c "$cmdtorun"
    done
}

# Kiểm tra nếu đã cài đặt
if [[ -f "$HOME/installed" ]]; then
    echo "Done (0.000s)! For help, type \"help\""
    echo "Listening on /0.0.0.0:0"
    echo "${bold}${lightgreen}==> Started ${lightblue}Container (Debian 12)${lightgreen} <=="
    
    # Chạy neofetch chào mừng
    $HOME/libraries/proot -S . /bin/bash -c "neofetch"
    runcmd
else
    echo "Downloading files for application (Debian 12 Update)"
    
    # Tạo thư mục làm việc sạch sẽ
    cd $HOME
    mkdir -p libraries
    
    # Tải và giải nén libraries (proot)
    curl -sSLo libs.zip https://github.com/RealTriassic/Ptero-VM-JAR/releases/download/latest/files.zip
    unzip -o libs.zip -d ./libraries/ >/dev/null 2>&1
    
    # Sửa lỗi thư mục lồng nhau (Lỗi phổ biến gây ra "No such file or directory")
    if [ -d "./libraries/libraries" ]; then
        mv ./libraries/libraries/* ./libraries/
        rm -rf ./libraries/libraries
    fi
    rm -f libs.zip
    
    echo -ne '##########           (50%)\r'
    
    # Tải Debian 12 RootFS
    curl -sSLo debian.tar.xz https://github.com/termux/proot-distro/releases/download/v3.16.0/debian-bookworm-x86_64.tar.xz
    tar -xJf debian.tar.xz --exclude='dev' >/dev/null 2>&1
    rm -f debian.tar.xz
    
    # Cấp quyền thực thi
    chmod +x ./libraries/proot
    
    # Cài đặt công cụ và neofetch
    if [ -f "./libraries/proot" ]; then
        ./libraries/proot -S . /bin/bash -c "apt-get update && apt-get install -y sudo curl wget htop nano neofetch python3"
        echo -ne '####################(100%)\r'
        echo -ne '\n'
        touch installed
        echo "Done (0.000s)! For help, type \"help\""
        ./libraries/proot -S . /bin/bash -c "neofetch"
        runcmd
    else
        echo "Lỗi: Không thể cài đặt bộ máy proot. Vui lòng kiểm tra dung lượng ổ đĩa."
        exit 1
    fi
fi
