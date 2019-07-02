provider "aws" {
    region = "eu-west-2"
    shared_credentials_file = "/home/hugo/.aws/credentials"
    profile = "default"
}

resource "aws_ecs_cluster" "inventoryECSCluster" {
  name = "inventoryECSCluster"
}

resource "aws_ecs_task_definition" "inventoryTaskDefinition" {
  family                = "inventoryServerTaskDefinition"
  container_definitions = "${file("server/task-definition.json")}"
}

resource "aws_ecs_service" "inventoryECSService" {
  name            = "inventoryECSService"
  cluster         = "inventoryECSCluster"
  task_definition = "inventoryTaskDefinition"
  desired_count   = 1
  //iam_role        = "${aws_iam_role.inventoryServer.arn}"
  //depends_on      = ["aws_iam_role_policy.inventoryServer"]
  depends_on        = [
    "aws_ecs_task_definition.inventoryTaskDefinition",
    "aws_ecs_cluster.inventoryECSCluster"
  ]
}
