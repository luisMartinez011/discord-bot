
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

resource "aws_iam_policy" "cloudwatch-policy" {

  name        = "aws_iam_policy_for_terraform_aws_lambda_role22"
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
resource "aws_iam_policy" "s3_policy" {
  name        = "lambda-s3-discord-bot-role"
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


data "aws_iam_policy" "dynamodb_policy" {
  name = "lambda-dynamodb-automatizacion-config-role"
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda-automatizacion-bot-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "attach-s3-policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_policy.arn

}

resource "aws_iam_role_policy_attachment" "attach-cloudwatch-policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.cloudwatch-policy.arn
}

resource "aws_iam_role_policy_attachment" "attach-dynamodb-policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = data.aws_iam_policy.dynamodb_policy.arn
}


data "aws_ecr_repository" "automatizacion-image" {
  name = "automatizacion-discord-bot-image"
}

resource "aws_lambda_function" "lambda_function" {
  function_name = "automatizacion-discord-bot-lambda"
  timeout       = 30
  image_uri     = "${data.aws_ecr_repository.automatizacion-image.repository_url}:latest"
  package_type  = "Image"
  role          = aws_iam_role.lambda_role.arn
  # runtime       = "python3.10"
  # handler       = "main.lambda_handler"
}

resource "aws_lambda_function_url" "lambda_url" {
  function_name      = aws_lambda_function.lambda_function.function_name
  authorization_type = "NONE"
}
