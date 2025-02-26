packer {
  required_plugins {
    amazon = {
      version = " >= 1.0.0, < 2.0.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}



variable "aws_region" {
  type = string
  default = "us-east-1"
}

variable "source_ami" {
  type = string
  default = "ami-04b4f1a9cf54c11d0"
}

variable "ssh_username" {
  type = string
  default = "ubuntu"
}

variable "subnet_id" {
  type = string
  default = "subnet-09550cd1fa139900a"
}

# variable "" {
#   type = string
#   default = ""
# }



source "amazon-ebs" "my-aws-ami" {
  region            = "${var.aws_region}"
  ami_name          = "csye6225_app_${formatdate("YYY_MM_DD", timestamp())}"
  ami_description   = "AMI for csye6225"

  ami_regions = [
    "us-east-1",
  ]

  aws_polling {
    delay_seconds = 120
    max_attempts = 50
  }

  instance_type    = "t2.micro"
  source_ami       = "${var.source_ami}"
  ssh_username     = "${var.ssh_username}"
  subnet_id        = "${var.subnet_id}"

  launch_block_device_mappings {
    delete_on_termination = true
    device_name           = "/dev/sda1"
    volume_size           = 8
    volume_type           = "gp2"
  }
}

# source "googlecompute" "csye6225-app-custom-image"{
#   ...
# }


build {
  source = [
    "source.amazon-ebs.my-aws-ami", 
    # "source.csye6225-app-custom-image",
  ]

  provisioner "shell" {
    inline = [
      "sudo mkdir -p /opt/csye6225",
    ]
  }
  # copy webapp.zip
  provisioner "file" {
    source      = "webapp.zip"
    destination = "/opt/csye6225/webapp.zip"
  }

  provisioner "shell" {
    environment_vars = [
      "DEBIAN_FRONTEND=noninteractive",
      "CHECKPOINT_DISABLE=1",
    ]

    script = "setup.sh",
  }
}