from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Any
from pymusic.models import Song
class Plugin(Protocol):
    name: str
    def setup(self, host:"PluginHost")->None: ...
    def teardown(self)->None: ...
@dataclass
class PluginHost:
    plugins: dict[str,Any]
    services: dict[str,Any]
    def __init__(self): self.plugins={}; self.services={}
    def register(self,name:str,service:Any)->None: self.services[name]=service
    def get(self,name:str)->Any: return self.services.get(name)
    def install(self,plugin:Plugin)->None:
        if plugin.name in self.plugins: raise ValueError(f"Plugin already installed: {plugin.name}")
        plugin.setup(self); self.plugins[plugin.name]=plugin
    def uninstall(self,name:str)->None:
        plugin=self.plugins.pop(name,None)
        if plugin: plugin.teardown()
class SongTransformPlugin:
    name="song-transform"
    def __init__(self,transform): self.transform=transform
    def setup(self,host): host.register("song_transform",self.transform)
    def teardown(self): pass
