# SMA Sunnyboy Solar Integration for Home Assistant

A Home Assistant custom integration to monitor SMA Sunnyboy solar inverters. This integration retrieves real-time and historical solar power production data directly from your inverter via local network connection.

## Features

- **Real-time Power Monitoring**: Track current power production in Watts
- **Daily Energy Production**: Monitor daily energy yield in kWh
- **Total Energy Production**: View total lifetime energy production in kWh
- **Local Communication**: All data is retrieved directly from your inverter - no cloud required
- **Easy Configuration**: Simple setup through Home Assistant UI

## Supported Devices

This integration supports SMA Sunnyboy inverters with WebConnect interface, including:
- Sunny Boy 3.0 / 3.6 / 4.0 / 5.0
- Sunny Boy Storage
- Other modern SMA inverters with local web interface

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/TNTBA/sunnyboy_homekit`
6. Select category: "Integration"
7. Click "Add"
8. Find "SMA Sunnyboy Solar" in the integration list and install it
9. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/sunnyboy` directory from this repository
2. Copy it to your Home Assistant `custom_components` directory:
   ```
   <config_dir>/custom_components/sunnyboy/
   ```
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "SMA Sunnyboy Solar"
4. Enter your inverter details:
   - **IP Address**: The local IP address of your Sunnyboy inverter (e.g., `192.168.1.100`)
   - **Username**: Your inverter username (default is usually `user`)
   - **Password**: Your inverter password
5. Click **Submit**

The integration will automatically create sensors for:
- Current Power (W)
- Daily Energy (kWh)
- Total Energy (kWh)

## Finding Your Inverter IP Address

1. Check your router's DHCP client list for a device named "SMA" or "Sunnyboy"
2. Or use your inverter's display to find its network settings
3. Consider setting a static IP for your inverter in your router

## Default Credentials

Most SMA Sunnyboy inverters come with default credentials:
- **Username**: `user`
- **Password**: Check the label on your inverter or use the password you set during initial setup

## Sensors

The integration provides the following sensors:

### Current Power
- **Entity ID**: `sensor.sunnyboy_current_power`
- **Unit**: W (Watts)
- **Description**: Real-time power production

### Daily Energy
- **Entity ID**: `sensor.sunnyboy_daily_energy`
- **Unit**: kWh (Kilowatt-hours)
- **Description**: Energy produced today

### Total Energy
- **Entity ID**: `sensor.sunnyboy_total_energy`
- **Unit**: kWh (Kilowatt-hours)
- **Description**: Total lifetime energy production

## Update Interval

The integration polls the inverter every 30 seconds by default to retrieve updated values.

## Troubleshooting

### Cannot Connect to Inverter

1. Verify the IP address is correct
2. Ensure your Home Assistant instance can reach the inverter on your network
3. Check that the username and password are correct
4. Try accessing the inverter's web interface directly in a browser: `http://YOUR_INVERTER_IP`

### Sensors Show "Unavailable"

1. Check that the inverter is powered on and connected to your network
2. Verify the inverter is producing power (it may be offline at night)
3. Check Home Assistant logs for error messages

## Support

For issues, questions, or feature requests, please [open an issue](https://github.com/TNTBA/sunnyboy_homekit/issues) on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for the Home Assistant community
- Inspired by the need for local, privacy-focused solar monitoring