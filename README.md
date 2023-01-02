# Sc2ReplayView

## Creating windows exe

Run the following:

```
.\venv\Scripts\pyinstaller.exe --add-data ".\venv\Lib\site-packages\sc2reader\data\*.*;sc2reader\data" --add-data ".
\venv\Lib\site-packages\sc2reader\data\WoL\*.*;sc2reader\data\WoL" --add-data ".\venv\Lib\site-packages\sc2reader\data\HotS\*.*;sc2reader\data\HotS" --add-data ".\ve
nv\Lib\site-packages\sc2reader\data\LotV\*.*;sc2reader\data\LotV" --onefile -w sc2replayview.py
```