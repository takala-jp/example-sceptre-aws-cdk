import yaml
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from aws_cdk import aws_lambda as lambda_
from aws_cdk import core


class LambdaCronStack(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        with open("templates/lambda-handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaFn = lambda_.Function(
            self, "Singleton",
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
        )

        # Run every day at 6PM UTC
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='18',
                month='*',
                week_day='MON-FRI',
                year='*'),
        )
        rule.add_target(targets.LambdaFunction(lambdaFn))


def sceptre_handler(P):
    app = core.App()
    LambdaCronStack(app, "LambdaCronExample")
    return yaml.dump(app.synth().get_stack("LambdaCronExample").template)
