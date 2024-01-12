echo -e "\nDestroying my test VM..."
vagrant destroy test -f

echo -e "\nRemoving all traces of Vagrant VM configurations..."
rm -fr ~/VirtualBox\ VMs/* ~/.vagrant.d .vagrant

# Remove the VM information from VirtualBox
echo -e "\nUnregistering all traces of Vagrant VMs from VirtualBox..."
dead_vms=$(VBoxManage list vms | grep inaccessible | sed -e 's/{//g' | sed -e 's/}//g' | awk '{print $2}')

for thisVM_UUID in ${dead_vms}; do
  VBoxManage unregistervm $thisVM_UUID;
done
