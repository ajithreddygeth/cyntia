#bin/bash
export AWS_ACCESS_KEY_ID=AKIAVH3PWEMQ6WJ3T742
export AWS_SECRET_ACCESS_KEY=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
export AWS_DEFAULT_REGION=us-west-2

rm list.txt
rm expiry.csv
for i in $(find /etc -type f -name '*.pem' -o -name '*.crt')
do
  let DIFF=($(date +%s -d `date --date="$(openssl x509 -in $i -noout -enddate | cut -d= -f 2)" --iso-8601`)-$(date +%s -d $'(date +%m-%d-%Y)'))/86400
  if [ $DIFF = 0 ]
  then
    echo "not a valid certificate"
  elif [ $DIFF -gt 30 ]
  then
    echo "cert is not expering"
  elif [[ $(openssl x509 -text -noout -in $i | grep DNS || echo $?) = 1 ]
  then
    echo "System managed cert"
  else
    echo "$i" >> list.txt
  fi
done


echo "######"
while read p; do
  echo >> expiry.csv && echo  $(hostname && echo ',' && echo `date --date="$(openssl x509 -in $p -noout -enddate | cut -d= -f 2)" --iso-8601` ; echo "," ;echo `openssl x509 -in $p -text | grep DNS` ; echo ","; echo "$p") |tr '\n' '\t' >> expiry.csv
done <list.txt


#openssl req -x509 -newkey rsa:4096 -sha256 -days 25 -nodes   -keyout example.key -out 25.crt -subj "/CN=example.com"   -addext "subjectAltName=DNS:example.com,DNS:www.example.net,IP:10.0.0.1"
