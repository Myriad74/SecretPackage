#!/bin/bash

# sudo check

if [ "$EUID" -eq "0" ] ; then
    echo "[+] You have root access, you may proceed."
else
    echo "[-] You do not have root access, please run this install script using root."
    exit 1
fi

# Now we check for existing files

# Metasploit and msfvenom

if (test -f "/usr/bin/msfconsole") ;
then
    echo "[+] Metasploit already installed"
elif (test -f "/snap/bin/msfconsole") ; 
then
    echo "[+] Metasploit already installed"
else
    echo "[-] Metasploit is not installed"
    echo "[+] Installing metasploit..."
    sudo snap install metasploit-framework
    echo "[+] Run metasploit framework in terminal and configure database"
    echo "[+] Run '$ db_status' once msfconsole loads to check that configuration worked, then exit to run main file."
    sleep 5
    echo "[+] Completed"
fi
