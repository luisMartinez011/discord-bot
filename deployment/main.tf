data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }

  # statement {
  #   sid       = "Stmt1712810836593"
  #   effect    = "Allow"
  #   actions   = ["s3:PutObject"]
  #   resources = ["arn:aws:s3:::automatizacion-uni-2024/*"]
  # }
}

#Created Policy for IAM Role
resource "aws_iam_policy" "s3_policy" {
  name        = "lambda-s3-automatizacion-role"
  description = "A test policy"


  policy = <<EOF
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
    EOF
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda-automatizacion-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "test-attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_policy.arn
}

data "archive_file" "python_lambda_package" {
  type        = "zip"
  source_dir  = "${path.module}/../data_scraping"
  output_path = "data_scraping.zip"
}

resource "aws_lambda_function" "test_lambda_function" {
  function_name    = "automatizacion-pia-lambda"
  filename         = "data_scraping.zip"
  source_code_hash = data.archive_file.python_lambda_package.output_base64sha256
  role             = aws_iam_role.lambda_role.arn
  runtime          = "python3.10"
  handler          = "initializer.lambda_handler"
  timeout          = 10
}
