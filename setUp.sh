chmod +x *.sh
cp setIp.sh /IoT
cp update.sh /IoT
cp lib.sh /IoT
cp 7688 /etc/init.d/
chmod +x /etc/init.d/7688
cd /IoT
./lib.sh
/etc/init.d/7688 enable