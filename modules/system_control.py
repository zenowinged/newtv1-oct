from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import math 

def set_master_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    scalar = float(level) / 100.0
    volume.SetMasterVolumeLevelScalar(scalar, None)

def get_master_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    scalar = volume.GetMasterVolumeLevelScalar()
    return int(scalar * 100)

def mute_system(mute=True):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(ISimpleAudioVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(ISimpleAudioVolume))
    volume.SetMute(int(mute), None)

def set_app_volume(app_name, level):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and app_name.lower() in session.Process.name().lower():
            volume.SetMasterVolume(level / 100.0, None)

def mute_app(app_name, mute=True):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and app_name.lower() in session.Process.name().lower():
           volume = session._ctl.QueryInterface(ISimpleAudioVolume)
           volume.SetMute(int(mute), None)

