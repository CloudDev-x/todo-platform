variable "location" {
  description = "Azure region"
  default     = "southafricanorth"
}

variable "project" {
  description = "Project name used in resource naming"
  default     = "todo-platform"
}

variable "db_admin_user" {
  description = "PostgreSQL admin username"
  default     = "todoadmin"
}

variable "db_admin_password" {
  description = "PostgreSQL admin password"
  sensitive   = true
}

variable "subscription_id" {
  description = "Azure subscription ID"
}
