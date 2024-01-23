account_id = "766334116490"
codebuild_params = {
  "NAME"         = "healthcheck_build"
  "GIT_REPO"     = "https://github.com/changchiajung/sre-availability-script.git"
  "IMAGE"        = "aws/codebuild/standard:4.0"
  "TYPE"         = "LINUX_CONTAINER"
  "COMPUTE_TYPE" = "BUILD_GENERAL1_SMALL"
  "CRED_TYPE"    = "CODEBUILD"
}
environment_variables = {
  "AWS_DEFAULT_REGION" = "us-east-1"
  "AWS_ACCOUNT_ID"     = "766334116490"
  "IMAGE_REPO_NAME"    = "lambda-ecr  "
  "IMAGE_TAG"          = "latest"
}
