variable "lambda_repo_name" {
  type    = string
  default = "lambda-ecr"
}

variable "codebuild_name" {
  type    = string
  default = "healthcheck_build"
}

variable "codebuild_timeout" {
  type    = number
  default = "60"
}

variable "account_id" {
  description = "AWS Account ID"
  type        = string
}
variable "codebuild_params" {
  description = "Codebuild parameters"
  type        = map(string)
}

variable "environment_variables" {
  description = "Environment variables"
  type        = map(string)
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "profile" {
  type    = string
  default = "EC2_RW_Role"
}

variable "lambda_timeout" {
  type    = number
  default = 20
}

variable "lambda_name" {
  type    = string
  default = "healthcheck"
}

variable "lambda_image_tag" {
  type    = string
  default = "latest"
}
