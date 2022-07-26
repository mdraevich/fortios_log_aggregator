# FortiOS Log Aggregator

## Introduction
The goal of the project is to provide an easy way to estimate the percentage of each log category in FortiOS logs.


## How to use
Clone the repository & run Python script:
```
git clone https://github.com/mdraevich/fortios_log_aggregator.git && cd fortios_log_aggregator
python3 stats.py ./logs/test.log
```

> File Format (CSV or Plain text) is determined **by file extension** (`*.log` / `*.csv`)



## Example usage

That's how it looks like:
```bash
matvey@matvey-pc:~$ python3 stats.py logs/test.log 
Filepath:       /home/matvey/logs/test.log
Format:         log
Size (lines):   14410

Status: 100.00%       [14410/14410]

Finished! Check this out...

0100020027  [1]:
    Percent: 20.43%    [2944/14410]
    Type: event
    Subtype: system
    Description: Outdated report files deleted

0100026004  [2]:
    Percent: 17.39%    [2506/14410]
    Type: event
    Subtype: system
    Description: DHCP client lease granted
 
# output is trimmed

```

## Why?

It can be useful for investigation of large log files produced by FortiGate devices.

## License
MIT