from __future__ import annotations
# libs
import yaml
from pathlib import Path

# typing
from typing import Any


class ConfigData:

    __config_path = Path(__file__).absolute().parent

    def __init__(self) -> None:
        self.robot_dir = self.__config_path.joinpath('robot')
        self.detector_dir = self.__config_path.joinpath('detector')
        self.camera_info_dir = self.__config_path.joinpath('camera_info')
        self._check_dir_exists()
        # Load configuration data
        _cfg_data_fp = self.__config_path.joinpath('config_data.yaml')
        if not _cfg_data_fp.exists() or not _cfg_data_fp.is_file():
            raise FileNotFoundError(f"Can not find configuration data file '{_cfg_data_fp}'")
        else:
            with _cfg_data_fp.open('r') as fp:
                try:
                    self._cfg_data: dict[str, Any] = yaml.safe_load(fp)
                except Exception as e:
                    raise RuntimeError(f"Error while reading {_cfg_data_fp} configuration with error msg: {e}")
        # Camera configuration
        self.camera_name = self._cfg_data['camera']['name']
        self.camera_dir = self.camera_info_dir.joinpath(self.camera_name, 'calibration')
        self.camera_cc = self.camera_info_dir.joinpath(self.camera_name, 'calibration', 'coefficients.toml')
        self._validate_camera_config()
        # Detector configuration
        self.detector_two_step_approach = self._cfg_data['detector']['two_step_approach']
        self.detector_time_out = self._cfg_data['detector']['time_out']
        self.detector_configs = {}
        for cfg_dtt in self._cfg_data['detector']:
            if cfg_dtt.startswith('detector_'):
                self.detector_configs[cfg_dtt.strip('detector_')] = self.detector_dir.joinpath(self._cfg_data['detector'][cfg_dtt])
        self._validate_detector_config()
        # Robot configuration
        self.robot_plug_type = self._cfg_data['robot']['plug_type']
        self._validate_robot_config()

    def __str__(self) -> str:
        return f"Configuration with parent path: {self.__config_path}"

    def __repr__(self) -> str:
        return str(self)

    def _check_dir_exists(self) -> None:
        for att_name in dir(self):
            if not att_name.startswith('__'):
                if att_name.endswith('_dir'):
                    att_path_value: Path = self.__getattribute__(att_name)
                    if not att_path_value.exists():
                        raise NotADirectoryError(f"Can't find directory with path {att_path_value}")

    def _validate_camera_config(self) -> None:
        if not self.camera_info_dir.joinpath(self.camera_name).is_dir():
            raise NotADirectoryError(f"Can't find camera configuration with name {self.camera_name}")
        if not self.camera_cc.exists() or not self.camera_cc.is_file():
            raise FileNotFoundError(f"Can't find a camera calibration coefficient file with path {self.camera_cc}")

    def _validate_detector_config(self) -> None:
        for dtt_cfg_fp in self.detector_configs.values():
            if not dtt_cfg_fp.exists() or not dtt_cfg_fp.is_file():
                raise FileNotFoundError(f"Can't find a detector configuration file with path {dtt_cfg_fp}")

    def _validate_robot_config(self) -> None:
        ur_ctrl_fp = self.robot_dir.joinpath('ur_control.toml')
        ur_pl_fp = self.robot_dir.joinpath('ur_pilot.toml')
        if not ur_ctrl_fp.exists() or not ur_ctrl_fp.is_file():
            raise FileNotFoundError(f"Can't find an ur-control configuration file with path {ur_ctrl_fp}")
        if not ur_pl_fp.exists() or not ur_pl_fp.is_file():
            raise FileNotFoundError(f"Can't find an ur-pilot configuration file with path {ur_pl_fp}")


config_data = ConfigData()
