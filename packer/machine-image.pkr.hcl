packer {
  required_plugins {
    amazon = {
      version = " >= 1.0.0, < 2.0.0"
      source  = "github.com/hashicorp/amazon"
    }

    googlecompute = {
      version = ">= 1.0.0, < 2.0.0"
      source  = "github.com/hashicorp/googlecompute"
    }
  }
}


# AWS variables
variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "source_ami" {
  type    = string
  default = "ami-04b4f1a9cf54c11d0"
}

variable "ssh_username" {
  type    = string
  default = "ubuntu"
}

variable "subnet_id" {
  type    = string
  default = "subnet-09550cd1fa139900a"
}


# GCP variables
variable "gcp_project_id" {
  type    = string
  default = "csye6225-gcp-dev"
}

variable "gcp_region" {
  type    = string
  default = "us-central1"
}

variable "gcp_zone" {
  type    = string
  default = "us-central1-a"
}

variable "gcp_source_image" {
  type = string
  # default = "ubuntu-2404-lts"
  default = "ubuntu-2404-noble-amd64-v20250228"

}

variable "gcp_machine_type" {
  type    = string
  default = "e2-micro"
}

variable "gcp_subnet" {
  type    = string
  default = "default"
}

# variable "" {
#   type = string
#   default = ""
# }


# aws source
source "amazon-ebs" "my-aws-ami" {
  region          = "${var.aws_region}"
  ami_name        = "csye6225_app_${formatdate("YYYY_MM_DD", timestamp())}"
  ami_description = "AMI for csye6225"

  ami_regions = [
    "us-east-1",
  ]

  aws_polling {
    delay_seconds = 120
    max_attempts  = 50
  }

  instance_type = "t2.micro"
  source_ami    = "${var.source_ami}"
  ssh_username  = "${var.ssh_username}"
  subnet_id     = "${var.subnet_id}"

  launch_block_device_mappings {
    delete_on_termination = true
    device_name           = "/dev/sda1"
    volume_size           = 8
    volume_type           = "gp2"
  }
}


# gcp source
source "googlecompute" "csye6225-app-custom-image" {
  project_id   = var.gcp_project_id
  region       = var.gcp_region
  zone         = var.gcp_zone
  source_image = var.gcp_source_image
  machine_type = var.gcp_machine_type
  image_name   = "csye6225-app-${formatdate("YYYYMMDD", timestamp())}"
  image_family = "csye6225-app"
  network      = "default"
  ssh_username = "ubuntu"

  disk_size = 10
  disk_type = "pd-balanced"

  # metadata = {
  #   ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  # }
}



build {
  sources = [
    # "source.amazon-ebs.my-aws-ami",
    "source.googlecompute.csye6225-app-custom-image"
  ]

  provisioner "shell" {
    inline = [
      "sudo mkdir -p /opt/csye6225",
      "sudo chown -R ubuntu:ubuntu /opt/csye6225"
    ]
  }
  # copy webapp.zip
  provisioner "file" {
    source      = "webappFlask.tar.gz"
    destination = "/opt/csye6225/webappFlask.tar.gz"
  }

  provisioner "shell" {
    environment_vars = [
      "DEBIAN_FRONTEND=noninteractive",
      "CHECKPOINT_DISABLE=1",
    ]

    script = "setup.sh"
  }
}