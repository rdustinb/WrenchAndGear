This script is intended to be launched as a daemon that runs in the background. The PWMLED instance needs to be
maintained to keep the PWM output constant, otherwise it will revert back to 1.0 output which drives the fan to 100%.

Running this script all the time is as easy as adding the following line to crontab:

```bash
@reboot python3 /path/to/fanControl.py
```
