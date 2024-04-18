# host_checker
Software that verifies the status or configuration of a computer or server host.

![Screenshot from 2024-04-16 15-53-30](https://github.com/AuxGrep/host_checker/assets/103135612/b1c27e6a-13e7-4221-9b37-ef6e7b556d4b)

# INSTALL 
1. sudo pip3 install requests
2. sudo pip3 install prettytable

# Usage
1. TCP connections
'sudo python3 check_host.py --host twitter.com --mode tcp
   
3. PING checks
sudo python3 check_host.py --host twitter.com --mode ping

4. HTTP connections
sudo python3 check_host.py --host twitter.com --mode http

5. DNS checks
sudo python3 check_host.py --host twitter.com --mode dns

