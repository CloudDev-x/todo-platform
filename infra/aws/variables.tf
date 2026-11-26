variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "project" {
  description = "Project name used in resource naming"
  default     = "todo-platform"
}

variable "db_username" {
  description = "RDS master username"
  default     = "todoadmin"
}

variable "db_password" {
  description = "RDS master password"
  sensitive   = true
}
