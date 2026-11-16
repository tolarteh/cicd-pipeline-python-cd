# infra/backend.hcl
bucket       = "tfstate-calculadora-tolarteh"
key          = "calculadora/terraform.tfstate"
region       = "us-east-1"
use_lockfile = true