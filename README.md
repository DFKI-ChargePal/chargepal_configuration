# ChargePal Configuration

This repository contains various configurations for the corresponding packages and robots.
The different configurations are separated via branches and have the following style:

```
<pkg_name>/<robot_name>/<tag_name>
```

This repository is currently used by the packages:

- [ChargePal UR-Pilot](https://github.com/DFKI-ChargePal/chargepal_ur_pilot) -- `ur_pilot`
- [ChargePal MAP](https://github.com/DFKI-ChargePal/chargepal_map) -- `map`

Further, in the project we used three different robots with the names:

- `er_flex_00040` (Mobile platform with id 00040)
- `er_flex_00041` (Mobile platform with id 00041)
- `cp_rigid_00022` (Testbed with UR10e arm)

## Initialization steps

To get the configurations, navigate to the target repository and clone this repository into it.

```shell
git clone https://github.com/DFKI-ChargePal/chargepal_configuration.git config
```
You can then select the desired branch
```shell
cd config
git switch -b <pkg_name>/<robot_name>/<tag_name>
```
