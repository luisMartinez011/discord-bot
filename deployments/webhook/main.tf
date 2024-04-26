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

resource "aws_iam_policy" "cloudwatch-policy" {

  name        = "cloudwatch-discord-webhook-policy"
  path        = "/"
  description = "AWS IAM Policy for managing aws lambda role"
  policy      = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": [
       "logs:CreateLogGroup",
       "logs:CreateLogStream",
       "logs:PutLogEvents"
     ],
     "Resource": "arn:aws:logs:*:*:*",
     "Effect": "Allow"
   }
 ]
}
EOF
}

#Created Policy for IAM Role
resource "aws_iam_policy" "dynamodb_policy" {
  name        = "lambda-dynamodb-automatizacion-webhook-role"
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
				"dynamodb:DescribeContributorInsights",
				"dynamodb:RestoreTableToPointInTime",
				"dynamodb:ListTagsOfResource",
				"dynamodb:CreateTableReplica",
				"dynamodb:UpdateContributorInsights",
				"dynamodb:UpdateGlobalTable",
				"dynamodb:CreateBackup",
				"dynamodb:DeleteTable",
				"dynamodb:UpdateTableReplicaAutoScaling",
				"dynamodb:UpdateContinuousBackups",
				"dynamodb:PartiQLSelect",
				"dynamodb:DescribeTable",
				"dynamodb:PartiQLInsert",
				"dynamodb:GetItem",
				"dynamodb:DescribeContinuousBackups",
				"dynamodb:UpdateGlobalTableVersion",
				"dynamodb:CreateGlobalTable",
				"dynamodb:GetResourcePolicy",
				"dynamodb:DescribeKinesisStreamingDestination",
				"dynamodb:EnableKinesisStreamingDestination",
				"dynamodb:ImportTable",
				"dynamodb:BatchGetItem",
				"dynamodb:DisableKinesisStreamingDestination",
				"dynamodb:UpdateTimeToLive",
				"dynamodb:BatchWriteItem",
				"dynamodb:ConditionCheckItem",
				"dynamodb:PutItem",
				"dynamodb:PartiQLUpdate",
				"dynamodb:Scan",
				"dynamodb:Query",
				"dynamodb:StartAwsBackupJob",
				"dynamodb:DescribeStream",
				"dynamodb:UpdateItem",
				"dynamodb:DeleteTableReplica",
				"dynamodb:DescribeTimeToLive",
				"dynamodb:CreateTable",
				"dynamodb:UpdateGlobalTableSettings",
				"dynamodb:RestoreTableFromAwsBackup",
				"dynamodb:UpdateKinesisStreamingDestination",
				"dynamodb:GetShardIterator",
				"dynamodb:RestoreTableFromBackup",
				"dynamodb:ExportTableToPointInTime",
				"dynamodb:UpdateTable",
				"dynamodb:GetRecords",
				"dynamodb:PartiQLDelete",
				"dynamodb:DescribeTableReplicaAutoScaling"
			],
			"Resource": [
				"arn:aws:dynamodb:us-east-1:${data.aws_caller_identity.current.account_id}:table/Automatizacion-discord-config",
				"arn:aws:dynamodb:us-east-1:${data.aws_caller_identity.current.account_id}:table/Automatizacion-discord-dataset",
				"arn:aws:dynamodb:us-east-1:${data.aws_caller_identity.current.account_id}:table/Automatizacion-discord-config/stream/2024-04-19T17:25:32.948"
			]
		}
	]
}
EOT
}

#Created Policy for IAM Role
resource "aws_iam_policy" "s3_policy" {
  name        = "lambda-s3-automatizacion-webhook-role"
  description = "A test policy"


  policy = <<EOT
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "VisualEditor0",
			"Effect": "Allow",
			"Action": "s3:GetObject",
			"Resource": "arn:aws:s3:::automatizacion-uni-2024/*"
		}
	]
}
EOT
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda-automatizacion-webhook-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}


resource "aws_iam_role_policy_attachment" "test-attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.dynamodb_policy.arn
}

resource "aws_iam_role_policy_attachment" "attach-cloudwatch-policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.cloudwatch-policy.arn
}

resource "aws_iam_role_policy_attachment" "attach-s3-policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_policy.arn
}



# data "archive_file" "zip_the_python_code" {
#   type        = "zip"
#   source_dir  = "${path.module}/../../discord/webhook"
#   output_path = "${path.module}/webhook.zip"
# }

data "aws_dynamodb_table" "dynamodb_table" {
  name = "Automatizacion-discord-config"
}

resource "aws_lambda_event_source_mapping" "source_dynamo" {
  event_source_arn       = data.aws_dynamodb_table.dynamodb_table.stream_arn
  function_name          = aws_lambda_function.automatizacion_discord_webhook.arn
  starting_position      = "LATEST"
  maximum_retry_attempts = 1
  batch_size             = 1
}

data "aws_ecr_repository" "automatizacion-image" {
  name = "automatizacion-discord-webhooks-image"
}


resource "aws_lambda_function" "automatizacion_discord_webhook" {
  #   filename      = "${path.module}/webhook.zip"
  function_name = "automatizacion-discord-webhook-lambda"
  timeout       = 30
  image_uri     = "${data.aws_ecr_repository.automatizacion-image.repository_url}:latest"
  package_type  = "Image"
  role          = aws_iam_role.lambda_role.arn
  environment {
    variables = {
      DISCORD_WEBHOOK = var.discord_webhook
    }
  }

  #   runtime = "python3.10"
  #   handler = "webhook.lambda_handler"

}


resource "aws_lambda_function_url" "test_latest" {
  function_name      = aws_lambda_function.automatizacion_discord_webhook.function_name
  authorization_type = "NONE"
}


