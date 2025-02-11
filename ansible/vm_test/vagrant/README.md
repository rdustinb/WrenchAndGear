# Packaging a Box

## Hashicorp Cloud
The URL to manage boxes can be found here:

https://portal.cloud.hashicorp.com

Navigate under default-project -> Vagrant -> KrampusBoxes

## Commands to Package
After a VM has been created in VirtualBox, it can be packaged with the following command:

```bash
vagrant package --base <name of VB VM>
```

The final file 'package.box' can be uploaded to the Hashicorp Portal.

## Issues Encountered

### The UEFI Shell
It seems the VM on VirtualBox always starts with UEFI shell, so it needs to be bypassed in the VM before the box is
packaged. The following UEFI shell commands:

```shell
fs0:
edit startup.nsh
```

Then add the following line to the file:

```text
\EFI\debian\<image name>.efi
```

Where image name is whatever is found from the UEFI shell \EFI\debian\. The 'ls' command works in this shell.

A nice [StackExchange](https://unix.stackexchange.com/questions/326956/virtualbox-guest-suddenly-boots-only-into-uefi-interactive-shell)
article about this needed modification can be found.
