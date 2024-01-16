# Wireless adapter Requirements:
- Monitor mode
- packet injection
- AP mode
# Buy:
https://www.amazon.com/gp/product/B08SJC78FH

# Change to monitor mode:
- iwconfig
- mode=managed, the default setting
   - Only packets with its destination MAC Address that match the wifi adapter are captured
- ifconfig wlan0 down
- Run this command to fix any potential issues (not required)
   - airmon-ng check kill
- enable monitor mode
   - iwconfig wlan0 mode monitor
   - as an alternative
      - 1- airmon-ng start wlan0
- ifconfig wlan0 up
- iwconfig

# Misc
- [[wireless_adapter_setup]]
- [[wireless_find_networks]]
- [[wireless_target_one_network]]
- [[hashcat]]
- [[wireless_deauthenticate]]
- [[wep]]
- [[wps]]
- [[wpa]]
- [[wpa2]]
- [[wpa_enterprise]]
- [[netsh]]
- [[captive_portals]]
- [[evil_twin]]
- [[defending_network]]
