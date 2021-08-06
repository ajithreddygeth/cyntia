import csv
import boto3
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


rclient = boto3.client('ec2',region_name='us-west-2')
#timestr = time.strftime("%Y%m%d-%H%M%S")
regions = [region['RegionName'] for region in rclient.describe_regions()['Regions']]
delimiter='\t'
with open('/tmp/acm.csv', 'a',newline='') as file:
    writer = csv.writer(file,delimiter=delimiter, quoting=csv.QUOTE_NONE, quotechar='',  lineterminator='\n')
    writer.writerow(["Region", "Domain_Name", "CertificateArn","Status","Created","Expirey","Issuer","Useby"])
def lambda_handler(event, context):
    for region in regions:
        print (region)
        _session = boto3.Session(region_name=region)

        resp = _session.client('acm').list_certificates(
            CertificateStatuses=[
                'PENDING_VALIDATION', 'ISSUED', 'INACTIVE', 'EXPIRED', 'VALIDATION_TIMED_OUT', 'REVOKED', 'FAILED'
            ],
            MaxItems=500)
        certs = resp.get('CertificateSummaryList')
        res = [ sub['CertificateArn'] for sub in certs ]
        for i in res:
            des= _session.client('acm').describe_certificate(CertificateArn=i)
            dump=(des.get('Certificate'))
            domain=(dump.get('DomainName'))
            arm=(dump.get('CertificateArn'))
            expiery=(dump.get('NotAfter'))
            cert_issu= (dump.get('Issuer'))
            usedby= (dump.get('InUseBy'))
            status= (dump.get("Status"))
            created= (dump.get("CreatedAt"))
            delimiter='\t'
            with open('/tmp/acm.csv', 'a',newline='') as file:
                writer = csv.writer(file,delimiter=delimiter, quoting=csv.QUOTE_NONE, quotechar='',  lineterminator='\n')
                writer.writerow([region, domain, arm,status,created,expiery,cert_issu,usedby])
        
    # Send email         
    msg = MIMEMultipart()
    msg["Subject"] = "Weekly ACM Report"
    msg["From"] = "ajithkumarapt@gmail.com"
    msg["To"] = "ajithkumarapt@gmail.com"
    # Set message body
    body = MIMEText("Hello, This is weekly ACM cert report !", "plain")
    msg.attach(body)
    filename = "/tmp/acm.csv"  # In same directory as script

    with open(filename, "rb") as attachment:
        part = MIMEApplication(attachment.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=filename)
    msg.attach(part)

    # Convert message to string and send
    ses_client = boto3.client("ses", region_name="us-west-2")
    response = ses_client.send_raw_email(
        Source="ajithkumarapt@gmail.com",
        Destinations=["ajithkumarapt@gmail.com"],
        RawMessage={"Data": msg.as_string()}
    )
    print(response)
