import enum
import functools
import os
import sys
from typing import List

import clr
import System


@functools.lru_cache()
def load_dll():
    dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    sys.path.append(dll_path)
    clr.AddReference("USB2LIN")
    import USB2LINDLL  # pylint: disable=import-outside-toplevel

    return USB2LINDLL


def check_result(result, error_msg: str):
    result_n = System.Convert.ToInt32(result)

    if result_n < 0:
        dll = load_dll()
        if not isinstance(result, dll.Result):
            result = dll.Result(result, True)
        error_string = f"{result.ToString()} ({result_n})"
        raise RuntimeError(f"{error_string}: {error_msg}")
    return result


class Usage(enum.Enum):
    LOADER = enum.auto()
    SENDBOOT = enum.auto()
    GOTOBOOT = enum.auto()
    LINMASTER = enum.auto()
    LINSLAVE = enum.auto()
    ST_BL = enum.auto()
    NEWLOADER = enum.auto()
    SYNCMODE = enum.auto()
    RUNCONFIG = enum.auto()

    @staticmethod
    @functools.lru_cache()
    def to_dlltype(usage: "Usage"):
        dll = load_dll()
        return {
            Usage.LOADER: dll.U2lUsageStates.U2L_USAGE_LOADER,
            Usage.SENDBOOT: dll.U2lUsageStates.U2L_USAGE_SENDBOOT,
            Usage.GOTOBOOT: dll.U2lUsageStates.U2L_USAGE_GOTOBOOT,
            Usage.LINMASTER: dll.U2lUsageStates.U2L_USAGE_LINMASTER,
            Usage.LINSLAVE: dll.U2lUsageStates.U2L_USAGE_LINSLAVE,
            Usage.ST_BL: dll.U2lUsageStates.U2L_USAGE_ST_BL,
            Usage.NEWLOADER: dll.U2lUsageStates.U2L_USAGE_NEWLOADER,
            Usage.SYNCMODE: dll.U2lUsageStates.U2L_USAGE_SYNCMODE,
            Usage.RUNCONFIG: dll.U2lUsageStates.U2L_USAGE_RUNCONFIG,
        }[usage]


class Usb2Lin:
    def __init__(self) -> None:
        dll = load_dll()
        self._usb2lin = dll.USB2LIN()

    def u2l_FindAllLinakDevices(self):
        check_result(
            self._usb2lin.u2l_FindAllLinakDevices(),
            "Error with finding all linak devices occured",
        )

    @property
    def LinakDevices(self):
        return self._usb2lin.LinakDevices

    def u2l_getFirstDevice(self):
        return self._usb2lin.LinakDevices[0]

    def u2l_OpenFirstDevice(self) -> None:
        check_result(
            self._usb2lin.u2l_OpenFirstDevice(),
            "Error with opening first linak device occured",
        )

    def u2l_CloseDevice(self):
        self._usb2lin.u2l_CloseDevice()

    def u2l_GetData(self):
        data_buffer = System.Array[System.Byte]([0 for _ in range(64)])
        result = check_result(
            self._usb2lin.u2l_GetData(data_buffer), "u2l_GetData failed"
        )

        length = result & 0x3F

        return [data_buffer[i] for i in range(length)]

    def u2l_SetData(self, data: List[int]) -> None:
        data_buffer = System.Array[System.Byte](data)
        check_result(
            self._usb2lin.u2l_SetData(data_buffer, 0, len(data)), "u2l_SetData failed"
        )

    def u2l_SetUsageOfControlLink(self, usage: Usage):
        check_result(
            self._usb2lin.u2l_SetUsageOfControlLink(Usage.to_dlltype(usage)),
            "Error with setting usage of control link occured",
        )

    def u2l_OpenSpecificDevice(self, deviceID):
        check_result(
            self._usb2lin.u2l_OpenSpecificDevice(deviceID),
            "Error with opening specific linak device occured",
        )

    def lin_ConnectAnyLinConfig(self, use7Bytes=True):
        hw_id = System.Array[System.Byte]([0 for _ in range(10)])
        check_result(
            self._usb2lin.lin_ConnectAnyLinConfig(hw_id, use7Bytes),
            "Error with connecting to any Lin configuration occured",
        )
        return "".join([chr(c) for c in hw_id]).rstrip("\x00")

    def lin_CloseLinConfig(self):
        self._usb2lin.lin_CloseLinConfig()

    def lin_GetLinConfig(self, address):
        buffer = System.Array[System.UInt32]([0 for _ in range(4)])
        check_result(
            self._usb2lin.lin_GetLinConfig(address, buffer),
            "Error with getting Lin configuration occured",
        )
        value = buffer[0] | (buffer[1] << 8) | (buffer[2] << 16) | (buffer[3] << 24)
        return value

    def lin_SetLinConfig(self, configName, value):
        check_result(
            self._usb2lin.lin_SetLinConfig(configName, value),
            "Error with setting Lin configuration occured",
        )

    def lin_ActivateConfig(self):
        self._usb2lin.lin_ActivateConfig()

    def lin_UseSync(self, useSync):
        self._usb2lin.lin_UseSync(useSync)
