#!/bin/bash

# sudo check

if (/usr/bin/id -u == 0) then
    echo "[+] You have root access, you may proceed."
    continue
else
    echo "[-] You do not have root access, please run this install script using root."
    exit 1

# Now we check for existing files

# Metasploit and msfvenom

if [test -e /usr/bin/msfconsole] then
    echo "[+] Metasploit already installed"
    if [test -x /usr/bin/msfconsole] then
        echo "[+] Metasploit has execute permissions, proceed..."
        continue
    else
        echo "[-] Metasploit does not have execute permissions"
        echo "[+] Giving metasploit execute permissions"
        chmod +x /usr/bin/msfconsole
else
    echo "[-] Metasploit is not installed"
    echo "[+] Installing metasploit..."
    echo "[+] Run '$ db_status' once msfconsole loads to check that configuration worked"
    curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall
    ./msfconsole
    echo "[+] Completed"