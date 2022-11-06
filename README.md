# Code Documentation for mygeneboleh's DSA4262 project

## Purpose of script 
The following document contains instructions to run the m6A classifier determined by mygeneboleh, as part of the final project for DSA4262 Sense-making Case Analysis : Health and Medicine for Academic Year 2022/23

## Getting started
We first start an AWS Ubuntu instance on the [Research Gateway Portal](https://research.rlcatalyst.com/catalog/GenomicsProject13/6316e36f623db700a93756aa)
> Please choose a size that is at least large

Once the instance has been created, we will search for the InstanceDNSName which can be found under the 'Outputs' tab
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/rg_home.png)
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/get_dns.png)

Copy the InstanceDNSName onto your clipboard.
> This guide will be done on your local terminal. You can simply SSH into the instance and run the commands provided, if you prefer.

## SSH
Open your Terminal application

SSH into the instance by running the following command :
`ssh -i (Path to your pem file for the Ubuntu instance) ubuntu@(InstanceDNSName you copied earlier)`

Hence, for someone whose pem file is in his 'Downloads' folder and InstanceDNSName 'ec2-13-229-219-200.ap-southeast-1.compute.amazonaws.com', he will run :
`ssh -i Downloads/jasin-tut-aws.pem ubuntu@ec2-13-229-219-200.ap-southeast-1.compute.amazonaws.com`
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/ssh.png)

## Git Clone
The next step would be to clone [our repository](https://github.com/shienkoh/mygeneboleh.git) into the home directory you just SSH-ed into.

This is done by running : `git clone https://github.com/shienkoh/mygeneboleh.git`

## Getting the packages
The script you will be running requires the numpy and sklearn packages on Python.
We will do this using the `set_up.sh` script created.

First enter the repository.
`cd mygeneboleh`
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/cd_mygeneboleh.png)

Then run the script. This will take about a minute.

`sh set_up.sh`
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/run_shell.png)

## Running the script
Now you are all set to run the script.

Run the following command :

`env/bin/python script3.py -ipath finalized_model.sav evaluator.json`

The script will output the predictions file into the current directory, titled 'data_with_preds_and_scores.csv', which can be verified by listing the current files with `ls`.
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/running_script.png)

This contains the Transcript ID, Gene ID, Position, aggregated features we used as well as the predicted scores and labels.

## Next steps

You can view and explore the data in 2 ways.

### Python on Ubuntu
Enter Python with `env/bin/python` then use pandas to view the data :
```python
import pandas as pd
data = pd.read_csv('data_with_preds_and_scores.csv')
data
```
![alt text](https://github.com/shienkoh/mygeneboleh/blob/main/images/output_python.png)

Use `exit()` to exit the Python environment.

### Save to local
You may wish to copy the csv file onto your local machine for you to do further inspections on, say, a Jupyter Notebook.

Logout of the instance : `logout`

Copy the csv file into the local directory of your choice with :

`scp -i (Path to your pem file for the Ubuntu instance) ubuntu@(InstanceDNSName you copied earlier):/home/ubuntu/mygeneboleh/data_with_preds_and_scores.csv (Local directory of your choice)`

Hence, for a user who :
1) Has his pem file in his 'Downloads' directory
2) Has an InstanceDNSName 'ec2-13-229-219-200.ap-southeast-1.compute.amazonaws.com'
3) Wishes to move the csv file into his 'Downloads' directory

He will run : 

`scp -i Downloads/jasin-tut-aws.pem ubuntu@ec2-13-229-219-200.ap-southeast-1.compute.amazonaws.com:/home/ubuntu/mygeneboleh/data_with_preds_and_scores.csv Downloads`
