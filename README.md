# iZone Custom Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

The `iZone` integration allows access of control of a local [iZone](https://izone.com.au/) ducted reverse-cycle climate control devices. These are largely available in Australia.

This is a fork (by the same author) of the `iZone` integration installed by default in homeassistant. The default integration is no longer being maintained and will be removed in the future in favor of this HACS component.

## Supported hardware

Any current iZone unit with ducted reverse cycle air-conditioning, and the CB wired or wireless bridge device installed should currently work. There is currently no support for the iZone lights, reticulation, or other devices. Support for power monitoring is complete and will be available soon.

## Installation

Install using HACS is the simple way.

### Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `izone`.
1. Download _all_ the files from the `custom_components/izone/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant

## Configuration

1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "iZone"
1. The integration should find the iZone device on your local network.

### Network settings

The iZone system uses UDP broadcasts over the local network to find and communicate with iZone devices. For this to work properly, UDP port  12107 must be able to be broadcasted on, 7005 needs to be listened to for broadcasted messages, and TCP port 80 for HTTP data to the bridge. The integration currently listens on `0.0.0.0` and broadcasts to all broadcast IPv4 local addresses, which is not configurable.

### Manual Configuration

Alternatively, the iZone integration can be configured manually via the
`configuration.yaml` file if there is more than one iZone system on the local
network and one or more must be excluded use manual configuration:

```yaml
# Full manual example configuration.yaml entry
izone:
  exclude:
    - "000013170"
```

## Using the integration

Each zone and the master controller are presented to HA as separate but connected devices.

### Master controller

Unit modes `off`, `heat`, `cool`, `heat/cool`, `dry`, and `fan only` are supported. For units fitted with the 'iSave' system, which vents in external air into the house, this is available as `eco` preset and will run in `fan only` mode.

### Zones

Zones have three modes available, closed, open, and auto. These are mapped to Home Assistant modes off, fan only, and auto, respectively. Only the auto mode supports setting the temperature.

### Control zone (climate control mode)

With multiple climate-controlled zones, you can't set the target temperature of the control but set the target temperature
for each individual zone.

The climate controller then selects the zone that is furthest away from the target and feeds the current temperature and
target temperature into the air conditioner unit, closing any other zones that have already reached their target.

In this mode the current control zone that has been selected is reported, as is the read-only target temperature for that
zone (read-only, set the value via the individual zones). The current temperature will also be that of the control
zone.

You can add configure to read these values into sensors (in `configuration.yaml`),
along with the supply temperature (use the ID of your unit):

```yaml
# Example configuration.yaml entry to create sensors
# from the izone controller state attributes
template:
  - sensor:
    - name: "Control zone"
      state: "{{ state_attr('climate.izone_controller_0000XXXXX','control_zone_name') }}"
    - name: "Target temperature"
      state: "{{ state_attr('climate.izone_controller_0000XXXXX','control_zone_setpoint') }}"
      unit_of_measurement: "°C"
    - name : "Supply temperature"
      state: "{{ state_attr('climate.izone_controller_0000XXXXX','supply_temperature') }}"
      unit_of_measurement: "°C"
```

And then graph them on a dashboard, along with the standard values such as the current temperature. Either add the sensor entities via the visual editor, or cut and paste this
snippet into the code editor:

```yaml
# Example snippet for dashboard card configuration (code editor)
entities:
  - entity: sensor.control_zone_target
  - entity: sensor.control_zone
  - entity: sensor.temperature_supply
  - entity: climate.izone_controller_0000XXXXX
hours_to_show: 24
refresh_interval: 0
type: history-graph
```

### Services

#### Service `izone.airflow_min`

Set the minimum airflow for a particular zone.

| Service data attribute | Optional | Description |
| ---------------------- | -------- | ----------- |
| `entity_id` | yes | izone Zone entity. For example `climate.bed_2`
| `airflow` | no | Airflow percent in 5% increments

#### Service `izone.airflow_max`

Set the maximum airflow for a particular zone.

| Service data attribute | Optional | Description |
| ---------------------- | -------- | ----------- |
| `entity_id` | yes | izone Zone entity. For example `climate.bed_2`
| `airflow` | no | Airflow percent in 5% increments

## Debugging

If you're trying to track down issues with the component, set up logging for it:

```yaml
# Example configuration.yaml with logging for iZone
logger:
  default: warning
  logs:
    homeassistant.components.izone: debug
    pizone: debug
```

This will help you to find network connection issues etc.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[izone]: https://github.com/Swamp-Ig/homeassistant_izone
[commits-shield]: https://img.shields.io/github/commit-activity/y/Swamp-Ig/homeassistant_izone.svg?style=for-the-badge
[commits]: https://github.com/Swamp-Ig/homeassistant_izone/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/Swamp-Ig/homeassistant_izone.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Swamp--Ig-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/Swamp-Ig/homeassistant_izone.svg?style=for-the-badge
[releases]: https://github.com/Swamp-Ig/homeassistant_izone/releases
