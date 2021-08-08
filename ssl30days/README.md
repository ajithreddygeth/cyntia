GET ALL CERTIFICATE EXPIREY DATES AND SEND AS CSV TO EMAIL

STEP:1 **NOTE: THIS SHOULD BE USED IN ANY ONE OF THE NODE ONLY**

Create a file with the CSV headings:
Copy the init.sh 


```
$ chmod +x init.sh
$ 0 0 * * MON /home/{user}/init.sh
```


STEP:2

Copy the shell script and schedule it for every monday. (on all nodes)


```
$ chmod +x exportcsv.sh
$ crontab -e
$ 2 0 * * MON /home/{user}/exportcsv.sh

```

STEP:3  Create Lambda layer

```
# Automatically detects python version (only works for python3.x)
export PYTHON_VERSION=`python3 -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}".format(*version))'`

# Temporary directory for the virtual environment
export VIRTUAL_ENV_DIR="awscli-virtualenv"

# Temporary directory for AWS CLI and its dependencies
export LAMBDA_LAYER_DIR="awscli-lambda-layer"

# The zip file that will contain the layer
export ZIP_FILE_NAME="awscli-lambda-layer.zip"


# Creates a directory for virtual environment
mkdir ${VIRTUAL_ENV_DIR}

# Initializes a virtual environment in the virtual environment directory
virtualenv ${VIRTUAL_ENV_DIR}

# Changes current dir to the virtual env directory
cd ${VIRTUAL_ENV_DIR}/bin/

# Activate virtual environment
source activate

# install the Package
pip install awscli

sed -i '' "1s/.*/\#\!\/var\/lang\/bin\/python/" aws (mac)

sed -i "1s/.*/\#\!\/var\/lang\/bin\/python/" aws   (linux)

deactivate

# Changes current directory back to where it started
cd ../..

# Creates a temporary directory to store AWS CLI and its dependencies
mkdir ${LAMBDA_LAYER_DIR}

# Changes the current directory into the temporary directory
cd ${LAMBDA_LAYER_DIR}

# Copies aws and its dependencies to the temp directory
cp ../${VIRTUAL_ENV_DIR}/bin/aws .
cp -r ../${VIRTUAL_ENV_DIR}/lib/python${PYTHON_VERSION}/site-packages/ .

# Zips the contents of the temporary directory
zip -r ../${ZIP_FILE_NAME} *

#CLEANUP

# Goes back to where it started
cd ..

# Removes virtual env and temp directories
rm -r ${VIRTUAL_ENV_DIR}
rm -r ${LAMBDA_LAYER_DIR}

```

Go to Lambda--> Layers --> Add layer --> Upload the awscli-lambda-layer.zip to the layer and use it on the lambda
