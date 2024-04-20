
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
resource "aws_iam_policy" "s3_policy" {
  name        = "lambda-s3-automatizacion-role"
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

data "aws_ecr_repository" "automatizacion-image" {
  name = "automatizacion-discord-datasets-image"
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda-automatizacion-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "test-attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_policy.arn
}


resource "aws_lambda_function" "test_lambda_function" {
  function_name = "automatizacion-discord-lambda"
  timeout       = 40
  image_uri     = "${data.aws_ecr_repository.automatizacion-image.repository_url}:latest"
  package_type  = "Image"
  role          = aws_iam_role.lambda_role.arn
  # runtime       = "python3.10"
  # handler       = "main.lambda_handler"
}
