resource "aws_lambda_function" "profile_faker_function" {
  function_name = "profile-faker-${var.env_name}"
  timeout       = var.lambda_timeout
  image_uri     = "${aws_ecr_repository.lambda_repo.repository_url}:${var.env_name}"
  package_type  = "Image"

  role = aws_iam_role.profile_faker_function_role.arn

  environment {
    variables = {
      ENVIRONMENT = var.env_name
    }
  }
}
