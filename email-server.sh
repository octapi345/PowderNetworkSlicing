sudo apt-get update
sudo apt-get upgrade

#postfix setup
sudo debconf-set-selections <<< "postfix postfix/mailname string emailserver.emulab.net"
sudo debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"
sudo apt-get install --assume-yes postfix

#program for viewing network statistics
sudo apt-get install vnstat

#uneeded
#sudo apt-get install dovecot-pop3d

