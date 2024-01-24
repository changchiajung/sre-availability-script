resource "aws_lambda_function" "healthcheck_lambda" {
  function_name = var.lambda_name
  timeout       = var.lambda_timeout
  image_uri     = "${aws_ecr_repository.lambda_repo.repository_url}:${var.lambda_image_tag}"
  package_type  = "Image"

  role = aws_iam_role.iam_for_lambda.arn

  environment {
    variables = {
    }
  }
}
