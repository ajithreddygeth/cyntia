#bin/bash
#cron to run on every week monday.. make sure to change the permission of the file to (chmod +x filename.sh)
export path=/home/ec2-user/server.crt
let DIFF=($(date +%s -d `date --date="$(openssl x509 -in $path -noout -enddate | cut -d= -f 2)" --iso-8601`)-$(date +%s -d $'(date +%m-%d-%Y)'))/86400
if [ $DIFF -lt 30 ];
then
    aws s3 cp s3://ssl-report-test/$(date +%Y)/$(date +%m)/$(date +%d)/expirey.csv .
    echo >> expirey.csv && echo  $(hostname && echo ',' && echo `date --date="$(openssl x509 -in $path -noout -enddate | cut -d= -f 2)" --iso-8601` ; echo "," ;echo `openssl x509 -in $path -text | grep DNS`) |tr '\n' '\t' >> expirey.csv
    aws s3 cp expirey.csv s3://ssl-report-test/$(date +%Y)/$(date +%m)/$(date +%d)/
    rm expirey.csv
else
echo "All good"   
fi
