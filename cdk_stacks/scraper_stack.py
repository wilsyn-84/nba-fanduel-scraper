from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_lambda,
    aws_lambda_python,
    aws_events as events,
    aws_events_targets as targets,
)
import os


class ScraperStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, configs, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        bucket = s3.Bucket(self, "ScraperBucket-{}".format(configs['stage']),
            bucket_name = 'scraper-{}-{}'.format(configs['stage'],configs['aws_account'])
        )

        scrapper_fn = aws_lambda.Function(self, "ScraperCronFn-{}".format(configs['stage']),
            function_name = "scraper-{}".format(configs['stage']),
            code=aws_lambda.Code.from_asset("src/fanduelscraper",
                bundling={
                    "image": aws_lambda.Runtime.PYTHON_3_8.bundling_docker_image,
                    "command": ["bash", "-c", 
                                "pip install -r requirements.txt -t /asset-output && cp -au index.py NBA /asset-output"
                            ]
                }
            ),
            handler="index.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            timeout = core.Duration.seconds(300),
            memory_size = 1048,
            environment={
                "BUCKET_NAME": bucket.bucket_name
            }

        )

        #Make sure to give lambda permission to write to S3 bucket
        bucket.grant_write(scrapper_fn)

        if(configs['stage'] == 'prod'):
            rule = events.Rule(self, "ScraperCronRule-{}".format(configs['stage']),
                schedule=events.Schedule.cron(
                    minute='0',
                    hour='9',
                    month='*',
                    week_day='*',
                    year='*'),
            )
            rule.add_target(targets.LambdaFunction(scrapper_fn))