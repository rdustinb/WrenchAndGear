packer {
  required_plugins {
    tart = {
      version = ">= 0.6.0"
      source  = "github.com/cirruslabs/tart"
    }
  }
}

source "tart-cli" "tart" {
  vm_base_name = "ghcr.io/cirruslabs/debian:latest"
  vm_name      = "debian"
  cpu_count    = 2
  memory_gb    = 4
  disk_size_gb = 20
  ssh_password = "@str0n0my!"
  ssh_timeout  = "120s"
  ssh_username = "sudood"
}

build {
  provisioner "ansible" {
    playbook_file = "../../debian_raspbian_setup.yml"
  }
}

