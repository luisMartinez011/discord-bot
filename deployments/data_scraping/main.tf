
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

#Created Policy for IAM Role

resource "aws_iam_policy" "cloudwatch-policy" {

  name        = "cloudwatch-discord-datascraping-policy"
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
  name        = "lambda-dynamodb-automatizacion-data-scraping-role"
  description = "A test policy"


  policy = <<EOT
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "VisualEditor0",
			"Effect": "Allow",
			"Action": "dynamodb:PutItem",
			"Resource": "arn:aws:dynamodb:us-east-1:675863513298:table/Automatizacion-discord-dataset"
		}
	]
}
EOT
}

#Created Policy for IAM Role
resource "aws_iam_policy" "s3_policy" {
  name        = "lambda-s3-automatizacion-data-scraping-role"
  description = "A test policy"


  policy = <<EOT
{
	"Version": "2012-10-17",
	"Statement": [
		{
      "Sid": "Stmt1712810836593",
      "Action": [
        "s3:PutObject"
      ],
			"Effect": "Allow",
			"Resource": "arn:aws:s3:::automatizacion-uni-2024/*"
		}
	]
}
EOT
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda-automatizacion-data-scraping-role"
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


data "aws_ecr_repository" "automatizacion-image" {
  name = "automatizacion-discord-datasets-image"
}
resource "aws_lambda_function" "test_lambda_function" {
  function_name = "automatizacion-discord-data-scraping-lambda"
  timeout       = 40
  image_uri     = "${data.aws_ecr_repository.automatizacion-image.repository_url}:latest"
  package_type  = "Image"
  role          = aws_iam_role.lambda_role.arn
  # runtime       = "python3.10"
  # handler       = "main.lambda_handler"
}
