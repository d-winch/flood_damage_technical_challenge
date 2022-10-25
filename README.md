# Flood Depth Damage Calculator

A Python script to analyse a csv file of depth values and output the expected damage cost.

Damage costs are located in damage.py in a dictioinary with the upper inclusive depth value as keys and the cost as the values.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

## Usage

```bash
python risk.py --f ".\csv\depths.csv" --p 75.5 --l 10
```
## Arguments

Dillinger is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Flag | Example | Required | Default |
| ------ | ------ | ------ | ------ |
| -f --filepath |./csv/depths.csv | Yes | N/A | 
| -p --percent_inundated | 75 | No | 100 |
| -l --log_level | 10 | No | 40 |

[Valid Log levels](https://docs.python.org/3/library/logging.html#logging-levels)
