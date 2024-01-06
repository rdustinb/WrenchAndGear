echo -e "\nDestroying my test VM..."
vagrant destroy test -f

echo -e "\nRemoving all traces of Vagrant VM configurations..."
rm -fr ~/VirtualBox\ VMs/* ~/.vagrant.d .vagrant

echo -e "\nBuilding the VM with Vagrant..."
vagrant up

echo -e "\nCapturing Vagrant SSH config to the VM into the file 'vagrant-ssh'..."
vagrant ssh-config > vagrant-ssh

echo -e "\nTo SSH directly into the VM, use the command:"
echo -e "\nssh -F vagrant-ssh test"
