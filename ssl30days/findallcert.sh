#bin/bash
export AWS_ACCESS_KEY_ID=AK********
export AWS_SECRET_ACCESS_KEY=25Gk***********************
export AWS_DEFAULT_REGION=us-west-2

rm list.txt
for i in $(find / -type f -name '*.pem' -o -name '*.crt')
do
  if [[ $(openssl x509 -text -noout -in $i | grep DNS || echo $?) = 1 ]]
  then echo "cert is wrong"
  else echo "$i" >> list.txt
  fi
done



echo "######"
while read p; do
 # aws s3 cp s3://ssl-cert-reports/$(date +%Y)/$(date +%m)/$(date +%d)/expiry.csv .
  echo >> expiry.csv && echo  $(hostname && echo ',' && echo `date --date="$(openssl x509 -in $p -noout -enddate | cut -d= -f 2)" --iso-8601` ; echo "," ;echo `openssl x509 -in $p -text | grep DNS` ; echo ","; echo "$p") |tr '\n' '\t' >> expiry.csv
  #aws s3 cp expiry.csv s3://ssl-cert-reports/$(date +%Y)/$(date +%m)/$(date +%d)/

done <list.txt
