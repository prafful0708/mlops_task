# MLOps Assignment

## Project Description

This project reads cryptocurrency market data from a CSV file, validates it, calculates a rolling mean, generates buy/sell signals, and saves performance metrics.

## Files

- run.py
- config.yaml
- data.csv
- requirements.txt
- Dockerfile
- README.md

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

or

```bash
py -3.14 run.py
```

## Output

The program generates:

- processed_data.csv
- metrics.json
- run.log

## Configuration

config.yaml

```yaml
seed: 42
window: 5
version: "v1"
```
