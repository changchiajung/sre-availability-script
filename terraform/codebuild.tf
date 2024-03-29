# simple codebuild project
resource "aws_codebuild_project" "codebuild_project" {
  name          = var.codebuild_name
  description   = "Codebuild for healthcheck lambda image"
  build_timeout = var.codebuild_timeout
  service_role  = aws_iam_role.iam_for_lambda.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  source {
    type            = "GITHUB"
    location        = lookup(var.codebuild_params, "GIT_REPO")
    git_clone_depth = 1

    git_submodules_config {
      fetch_submodules = true
    }
  }

  environment {
    image                       = lookup(var.codebuild_params, "IMAGE")
    type                        = lookup(var.codebuild_params, "TYPE")
    compute_type                = lookup(var.codebuild_params, "COMPUTE_TYPE")
    image_pull_credentials_type = lookup(var.codebuild_params, "CRED_TYPE")
    privileged_mode             = true

    dynamic "environment_variable" {
      for_each = var.environment_variables
      content {
        name  = environment_variable.key
        value = environment_variable.value
      }
    }
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "codebuild-log-group"
      stream_name = "codebuild-log-stream"
    }

    s3_logs {
      status = "DISABLED"
    }
  }
}
