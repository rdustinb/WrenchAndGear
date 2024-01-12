# First cleanup any Vagrant VMs
vagrant_cleanup.sh

# Setup the new Vagrant VM
echo -e "\nBuilding the VM with Vagrant..."
vagrant up

echo -e "\nCapturing Vagrant SSH config to the VM into the file 'vagrant-ssh'..."
vagrant ssh-config > vagrant-ssh

echo -e "\nTo SSH directly into the VM, use the command:"
echo -e "\nssh -F vagrant-ssh test"
