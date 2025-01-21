# Monitoring UPS State
It is necessary to monitor the state of a UPS, not just by the device it so happens to be directly connected to. In many
cases it may be necessary to share the state of the UPS across multiple devices, as multiple devices depend on the
uptime of said UPS. Often times a UPS has a USB interface allowing for direct connection of the UPS to a device, albeit
only a single device. The state of the UPS information can be shared with other devices across an ethernet interface by
the use of the SNMP protocol. While the UPS itself doesn't need to usually react to incoming SNMP packets, the fact that
it can broadcast SNMP messages makes this type of infrastructure useful for an entire system or rack of PCs.

## SNMP Protocol
The SNMP Protocol uses a GET message to fetch data on demand from a remote host. With version 2 of the SNMP protocol,
there is a special string required as part of the GET request that, if it matches the host system community string, will
cause the host to return a GET-RESPONSE packet with a variety of information about the host. Call the community string a
form of authentication, but in reality it is more like a way to segregate the information on the SNMP network. If the
community string does match what is configured on a host, the host simply ignores the GET-REQUEST.

Version 3 of the SNMP protocol has more modern authentication protocol layers which require a node to authenticate
properly with the host before the host will respond to GET-REQUEST packets.

### Addressing
Endpoints of information within an SNMP server space may be addressed using a long string of decimal numbers separated
by periods. The first set of decimal values are always the same due to their designation in the ISO standard they come
from:

```text
  _____________________ ISO Assigned OIDs
 |  ___________________ ISO Identified Organizations
 | |  _________________ US Department of Defense
 | | |  _______________ Internet
 | | | |  _____________ Internet Private
 | | | | |  ___________ Manufacturer OID
 | | | | | |           
 | | | | | |           
 | | | | | |  _________ Device Element Address Level 1
 | | | | | | |  _______ Device Element Address Level 2
 | | | | | | | |
 | | | | | | | |    ___ Device Element Address Level n
 | | | | | | | |   |
 V V V V V V V V   V
.1.3.6.1.4.x.x.x...x
```

Most of the first several decimal values are predefined based on the device being addressed. Only the final few decimal
numbers can be changed to address different data endpoints on the SNMP server itself. More information can be found
[here](https://www.alvestrand.no/objectid/1.3.6.1.4.1.html).

## Tools
The basic tool for monitoring SNMP messages is called **snmpwalk** and allows for decoding of those messages that belong
to a specific community. The snmpwalk command line tool will send a GET-REQUEST to a specific IP address with a specific
community string and then process the GET-RESPONSE as a large dictionary of information.

Syntax of capturing the data from a single SNMP server would be something like this:

```bash
snmpwalk -v2c -c <server community> <server IP> .1.3.6.1.4.1.44738
```

Note how the OID .1.3.6.1.4.1 is a default for most devices and won't need to ever change. Since the IP Address of the
SNMP server is also being defined, there isn't a lot of question as to what is being addressed. However, the response
from an SNMP GET-REQUEST of just a single server can provide an extensive list of data values which is why most vendors
of SNMP Servers provide an MIB file to download which describes the different field and address space breakdown within
the top level reponse table.

## Example Output
Given an Asustor AS6604T NAS and a Triplite SMART1500 UPS attached via USB, along with the NAS running an SNMP Server,
the response from the SNMP Server from the above command will result in an extensively long list of items:

```text
SNMPv2-SMI::enterprises.44738.1.1.0 = STRING: "AS21126604TM032D"
SNMPv2-SMI::enterprises.44738.1.2.0 = STRING: "4.3.3.RC92"
SNMPv2-SMI::enterprises.44738.1.3.0 = STRING: "1.28"
SNMPv2-SMI::enterprises.44738.1.4.0 = STRING: "17 days, 12:01"
SNMPv2-SMI::enterprises.44738.1.5.0 = STRING: "01/21/2025 00:17"
...
SNMPv2-SMI::enterprises.44738.6.1.1.3.1 = STRING: "Tripp Lite UPS "
SNMPv2-SMI::enterprises.44738.6.1.1.4.1 = STRING: "0x09ae"
SNMPv2-SMI::enterprises.44738.6.1.1.5.1 = STRING: "0x2012"
SNMPv2-SMI::enterprises.44738.6.1.1.6.1 = INTEGER: 31
SNMPv2-SMI::enterprises.44738.6.1.1.7.1 = INTEGER: 100
```

Further limiting of the response data can be performed by simply specifying the next order decimal value desired:

```bash
snmpwalk -v2c -c <server community> <server IP> .1.3.6.1.4.1.44738.6
```

The response is now limited to only 8 fields, much more manageable!

```text
SNMPv2-SMI::enterprises.44738.6.1.1.1.1 = INTEGER: 1
SNMPv2-SMI::enterprises.44738.6.1.1.2.1 = STRING: "Tripp Lite "
SNMPv2-SMI::enterprises.44738.6.1.1.3.1 = STRING: "Tripp Lite UPS "
SNMPv2-SMI::enterprises.44738.6.1.1.4.1 = STRING: "0x09ae"
SNMPv2-SMI::enterprises.44738.6.1.1.5.1 = STRING: "0x2012"
SNMPv2-SMI::enterprises.44738.6.1.1.6.1 = INTEGER: 31
SNMPv2-SMI::enterprises.44738.6.1.1.7.1 = INTEGER: 100
```
