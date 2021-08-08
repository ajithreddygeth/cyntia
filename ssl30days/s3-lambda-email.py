import subprocess
import logging
import glob
import boto3
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 


#### Logger function ####
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def run_command(command):
    command_list = command.split(' ')

    try:
        logger.info("Running shell command: \"{}\"".format(command))
        result = subprocess.run(command_list, stdout=subprocess.PIPE);
        logger.info("Command output:\n---\n{}\n---".format(result.stdout.decode('UTF-8')))
    except Exception as e:
        logger.error("Exception: {}".format(e))
        return False

    return True

####

s3 = boto3.resource('s3')
def lambda_handler(event, context):
    now = datetime.now()
    date=now.strftime("%d")
    month=now.strftime("%m")
    year=now.strftime("%Y")
    run_command('/opt/aws s3 cp s3://ssl-report-test/{}/{}/{}/expirey.csv /tmp/report/'.format(year,month,date))
    print(glob.glob("/tmp/"))
    
    msg = MIMEMultipart()
    msg["Subject"] = "Daily logs"
    msg["From"] = "ajithkumarapt@gmail.com"
    msg["To"] = "ajithkumarapt@gmail.com"

    # Set message body
    body = MIMEText("Hello, This is daily log email !", "plain")
    msg.attach(body)
    filename = "/tmp/report/expirey.csv"  # In same directory as script

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
