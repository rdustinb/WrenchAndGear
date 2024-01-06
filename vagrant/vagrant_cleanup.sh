echo -e "\nDestroying my test VM..."
vagrant destroy test -f

echo -e "\nRemoving all traces of Vagrant VM configurations..."
rm -fr ~/VirtualBox\ VMs/* ~/.vagrant.d .vagrant

