# Test task

## Install

### Install .kkrieger

DirectX9, WinXP(SP2) compatibility mode required

[Get .kkrieger](http://www.ag.ru/games/kkrieger/demos# )

[Mirror](http://web.archive.org/web/20110717024227/http://www.theprodukkt.com/kkrieger#20)
***

### Install FRAPS

[Get FRAPS](https://fraps.com/download.php)
***

### Install packages

> pip install -r requirements.txt
***

### Configure FRAPS

1. Open FRAPS
2. Choose FPS in menu
3. Set folder to save benchmarks
4. Set the hotkey
5. Mark "MinMaxAvg" in "Benchmark Settings" checkbox
6. Close FRAPS

***

### Set config.ini file

> fraps_path = <path_where_fraps.exe_installed>

> fraps_output = <path_where_fraps_saves_benchmarks>

> fraps_benchmark_hotkey = <key_that_starts_benchmark>

## Run script

> python main.py <path_to_kkrieger> [-o <path_to_output ]
