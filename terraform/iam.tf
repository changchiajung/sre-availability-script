data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com", "codebuild.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "local_file" "policy" {
  filename = "policy.json"
}

resource "aws_iam_role_policy" "policy" {
  role   = aws_iam_role.iam_for_lambda.name
  policy = replace(replace(data.local_file.policy.content, "ACCOUNT_ID", var.account_id), "CODEBUILD_NAME", var.codebuild_name)
}
