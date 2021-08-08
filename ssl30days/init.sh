(echo 'Hostname' && echo ',' && echo 'Expiery-date' && echo ',' && echo 'DNS-name') |tr '\n' '\t' >>expirey.csv
aws s3 cp expirey.csv s3://ssl-report-test/$(date +%Y)/$(date +%m)/$(date +%d)/
rm expirey.csv
