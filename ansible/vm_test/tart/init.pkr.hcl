packer {
  required_plugins {
    tart = {
      version = ">= 0.6.0"
      source  = "github.com/cirruslabs/tart"
    }
  }
}

variable "username" {
  type =  string
  default = "thisuser"
  // Sensitive vars are hidden from output as of Packer v1.6.5
  sensitive = true
}

variable "password" {
  type =  string
  default = "thispassword"
  // Sensitive vars are hidden from output as of Packer v1.6.5
  sensitive = true
}

source "tart-cli" "tart" {
  #from_iso          = ["debian-12.5.0-arm64-FullDVD.iso"]
  from_iso          = ["debian-12.5.0-arm64-NetInstall.iso"]
  vm_name           = "debian-12.5.0-vanilla"
  cpu_count         = 4
  memory_gb         = 8
  disk_size_gb      = 20
  boot_wait         = "2s"
  boot_command      = [
    "<return>",
    "<wait2s>",
    "<return>",
    "<wait1s>",
    "<return>",
    "<wait1s>",
    "<return>",
    "<wait25s>",
    # This updates the hostname from "debian" to "debian-vm.local":
    "-vm.local",
    "<return>",
    "<wait2s>",
    # Skip setting the Root Password:
    "<return>",
    "<wait1s>",
    "<return>",
    "<wait1s>",
    # Create a user:
    "${var.username}",
    "<return>",
    "<wait1s>",
    "<return>",
    "<wait1s>",
    # Set the User's Password:
    "${var.password}",
    "<return>",
    "<wait1s>",
    # Confirm the User's Password:
    "${var.password}",
    "<return>",
    "<wait1s>",
    # Set the Timezone:
    "m",
    "<return>",
    "<wait5s>",
    # Setup the Disk
    "<return>",
    "<wait1s>",
    "<return>",
    "<wait1s>",
    "<return>",
    "<wait1s>",
    "<return>",
    "<tab>",
    "<return>",
    # Wait for the base system to be installed:
    "<wait45s>",
    # Configure the package manager (US, Default Mirror):
    "<return>",
    "<return>",
    "<return>",
    "<wait10s>",
    # No to popularity contest:
    "<return>",
    "<wait2s>",
    # Software selection:
    "<down>",
    "<down>",
    "<spacebar>",
    "<return>",
    # Wait for OS and Grub to be installed:
    "<wait3m10s>",
    "<return>",
  ]
  ssh_username      = "${var.username}"
  ssh_password      = "${var.password}"
  ssh_timeout       = "10s"
}

build {
  sources = ["source.tart-cli.tart"]

  #provisioner "ansible" {
  #  playbook_file = "../../debian_raspbian_setup.yml"
  #}
}
