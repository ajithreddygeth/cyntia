# IF the insisnce has no profile attched to access S3 use the keys to do that 
# $ export AWS_ACCESS_KEY_ID=AKIAI******
# $ export AWS_SECRET_ACCESS_KEY=wJalrXUt**************
# $ export AWS_DEFAULT_REGION=us-west-2

(echo 'Hostname' && echo ',' && echo 'Expiery-date' && echo ',' && echo 'DNS-name') |tr '\n' '\t' >>expirey.csv
aws s3 cp expirey.csv s3://ssl-report-test/$(date +%Y)/$(date +%m)/$(date +%d)/
rm expirey.csv
