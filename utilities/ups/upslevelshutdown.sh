#!/bin/bash
# This is the IP Address the SNMP Server daemon is running on:
SERVERIP=192.168.85.100
# This shouldn't ever change:
OIDBASE=.1.3.6.1.4.1
# This will be defined from the SNMP Server's MIB file:
UPSOFFSET=.44738.6
# UPS Battery Level Field
UPSFIELDOFFSET=7

# Shutdown Threshold in percentage
NOTIFICATIONTHRESHOLD=90
SHUTDOWNTHRESHOLD=50

# Call the SNMP Command
UPSLEVEL=$(snmpwalk -v2c -c mynasups ${SERVERIP} ${OIDBASE}${UPSOFFSET} | head -n${UPSFIELDOFFSET} | tail -n1 | sed -e 's/ /~/g' | sed -e 's/:~/ /g' | awk '{print $2}')

# Determine if the UPS Battery Level is under the threshold
if [ "${UPSLEVEL}" -lt "${SHUTDOWNTHRESHOLD}" ]; then
  echo "The UPS Battery level of ${UPSLEVEL}% is lower than the defined shutdown threshold of ${SHUTDOWNTHRESHOLD}%."
  echo "The system is shutting down..."
elif [ "${UPSLEVEL}" -lt "${NOTIFICATIONTHRESHOLD}" ]; then
  echo "UPS Battery level has dropped to ${UPSLEVEL}%..."
else
  echo "UPS Battery level is full."
fi
