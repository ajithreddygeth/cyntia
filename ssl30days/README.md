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
