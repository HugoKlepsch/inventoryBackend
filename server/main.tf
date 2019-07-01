provider "aws" {
    region = "eu-west-2"
    shared_credentials_file = "/home/hugo/.aws/credentials"
    profile = "default"
}

resource "aws_ecs_cluster" "inventory" {
  name = "inventoryServer"
}

resource "aws_ecs_service" "inventoryServerService" {
  name            = "inventoryServerService"
  cluster         = "${aws_ecs_cluster.inventory.id}"
  task_definition = "${aws_ecs_task_definition.inventoryServer.arn}"
  desired_count   = 1
  iam_role        = "${aws_iam_role.inventoryServer.arn}"
  depends_on      = ["aws_iam_role_policy.inventoryServer"]
}
