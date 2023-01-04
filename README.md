# Sc2ReplayView

## Creating windows exe

Run the following:

```
 .\venv\Scripts\pyinstaller.exe --add-data ".\venv\Lib\site-packages\sc2reader\data\*.*;sc2reader\data" --add-data ".\venv\Lib\site-packages\sc2reader\data\WoL\*.*;sc2reader\data\WoL
" --add-data ".\venv\Lib\site-packages\sc2reader\data\HotS\*.*;sc2reader\data\HotS" --add-data ".\venv\Lib\site-packages\sc2reader\data\LotV\*.*;sc2reader\data\LotV" --add-data 'rplayicon.ico;.' --icon  'rplayicon.ico' --onefile -w sc2replayview.py
```