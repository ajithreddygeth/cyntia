#bin/bash
export AWS_ACCESS_KEY_ID=AKIAVH3**********
export AWS_SECRET_ACCESS_KEY=25GkPA*******************
export AWS_DEFAULT_REGION=us-west-2

rm list.txt
rm expiry.csv
for i in $(find / -type f -name '*.pem' -o -name '*.crt')
do
  let DIFF=($(date +%s -d `date --date="$(openssl x509 -in $i -noout -enddate | cut -d= -f 2)" --iso-8601`)-$(date +%s -d $'(date +%m-%d-%Y)'))/86400
  if [ $DIFF = 0 ]
  then
    echo "not a valid certificate"
  elif [ $DIFF -gt 30 ]
  then
    echo "cert is not expering"
  elif [[ $(openssl x509 -text -noout -in $i | grep DNS || echo $?) = 1 ]]
  then
    echo "System managed cert"
  else
    echo "$i" >> list30.txt
  fi
done


echo "######"
while read p; do
  echo >> expiry.csv && echo  $(hostname && echo ',' && echo `date --date="$(openssl x509 -in $p -noout -enddate | cut -d= -f 2)" --iso-8601` ; echo "," ;echo `openssl x509 -in $p -text | grep DNS` ; echo ","; echo "$p") |tr '\n' '\t' >> expiry30.csv
done <list30.txt

s3 cp expiry30.csv s3://ssl-cert-reports/$(date +%Y)/$(date +%m)/$(date +%d)/expiry/$(hostname)
