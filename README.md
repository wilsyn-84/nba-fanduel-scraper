# FanDuel Scrapper 

 A scrapper for FanDuel Sportbook NBA lines.  Data is extracted from FanDuel via APIs found on their website.  Deployed used AWS CDK to a lambda function which runs everyday at 12pm central time.  Data is stored in S3 to be refernced in other personal projects.

## Scraper
General steps to the process:
* Use a public API to get all matchups for today (this includes a gameID)
* Loop through each gameID and call a separate API to grab all wager markets including Spread, MoneyLine, Over/Under, and player props
* Format data into a long table structure 
* Output CSV file to S3.

Source code is located in `src > FanduelScraper`

## Setup
### Prerequisites
* Python 3.9.1 (CDK)
* Python 3.8 (Scraper function)
* AWS CDK 1.90.1
* AWS SAM 1.18.2
* Docker version 20.10.3

** I am locally using a new Macbook with the M1 chip and have had some trouble installing specific python modules on 3.9

### Local Testing 

#### Virtual Environment
Create a virutal environment, activate the environment, and install necessary dependencies:

```
$ python3 -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

##### Lambda Testing
Since this project leverages the AWS CDK, we can use AWS SAM for local function testing.  First you must synthesize the CloudFormation template and then invoke the function. Stage is a required argument and is defined within `configs.json`
```
cdk synth --no-staging scrapper -c stage=<stage> > template.yaml
```
After synth, you need to find the function name from the `template.yaml` output file.  With that function name, calling the command below will spin in a AWS Lambda specific docker container to replicate the environment.  
```
sam local invoke <MyFunction> --no-event 
```

### Deployment
Once functions are tested and ready for deployment, re-synthesize the CloudFormation template and deploy the stack to the correct environment.
```
cdk synth <stack_name> -c stage=<stage>
cdk deploy <stack_name> -c stage=<stage> --profile <profile>
```
