resource "aws_cloudwatch_event_rule" "execution-lambda" {
  name                = "run-lambda-function"
  description         = "Schedule lambda function"
  schedule_expression = "cron(00 */6 * * *)"
}

resource "aws_cloudwatch_event_target" "lambda-function-target" {
  target_id = "lambda-function-target"
  rule      = aws_cloudwatch_event_rule.execution-lambda.name
  arn       = aws_lambda_function.test_lambda_function.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.test_lambda_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.execution-lambda.arn
}
