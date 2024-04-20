data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }

}

data "aws_caller_identity" "current" {}

#Created Policy for IAM Role
resource "aws_iam_policy" "dynamodb_policy" {
  name        = "lambda-dynamodb-automatizacion-config-role"
  description = "A test policy"


  policy = <<EOT
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "VisualEditor0",
			"Effect": "Allow",
			"Action": [
				"dynamodb:DeleteItem",
				"dynamodb:RestoreTableToPointInTime",
				"dynamodb:CreateTableReplica",
				"dynamodb:UpdateContributorInsights",
				"dynamodb:UpdateGlobalTable",
				"dynamodb:CreateBackup",
				"dynamodb:DeleteTable",
				"dynamodb:UpdateTableReplicaAutoScaling",
				"dynamodb:UpdateContinuousBackups",
				"dynamodb:PartiQLInsert",
				"dynamodb:UpdateGlobalTableVersion",
				"dynamodb:CreateGlobalTable",
				"dynamodb:EnableKinesisStreamingDestination",
				"dynamodb:ImportTable",
				"dynamodb:DisableKinesisStreamingDestination",
				"dynamodb:UpdateTimeToLive",
				"dynamodb:BatchWriteItem",
				"dynamodb:PutItem",
				"dynamodb:PartiQLUpdate",
				"dynamodb:StartAwsBackupJob",
				"dynamodb:DescribeStream",
				"dynamodb:UpdateItem",
				"dynamodb:DeleteTableReplica",
				"dynamodb:CreateTable",
				"dynamodb:UpdateGlobalTableSettings",
				"dynamodb:RestoreTableFromAwsBackup",
				"dynamodb:UpdateKinesisStreamingDestination",
				"dynamodb:GetShardIterator",
				"dynamodb:RestoreTableFromBackup",
				"dynamodb:ExportTableToPointInTime",
				"dynamodb:UpdateTable",
				"dynamodb:GetRecords",
				"dynamodb:PartiQLDelete"
			],
			"Resource": [
				"arn:aws:dynamodb:us-east-1:${data.aws_caller_identity.current.account_id}:table/Automatizacion-discord-config",
				"arn:aws:dynamodb:us-east-1:${data.aws_caller_identity.current.account_id}:table/Automatizacion-discord-config/stream/2024-04-19T17:25:32.948"
			]
		}
	]
}
EOT
}


resource "aws_iam_role" "lambda_role" {
  name               = "lambda-automatizacion-task-scheduler-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "test-attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.dynamodb_policy.arn
}

data "archive_file" "zip_the_python_code" {
  type        = "zip"
  source_dir  = "${path.module}/../../task_scheduler"
  output_path = "${path.module}/task_scheduler.zip"
}

resource "aws_lambda_function" "automatizacion_discord_configuration_function" {
  filename      = "${path.module}/task_scheduler.zip"
  function_name = "automatizacion-discord-configuration-lambda"
  timeout       = 30
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.10"
  handler       = "task_scheduler.lambda_handler"

}

resource "aws_lambda_function_url" "test_latest" {
  function_name      = aws_lambda_function.automatizacion_discord_configuration_function.function_name
  authorization_type = "NONE"
}

