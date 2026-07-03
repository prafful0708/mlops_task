import pandas as pd
import numpy as np
import yaml
import json
import logging
import time
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--input", required=True, help="Input CSV file")
parser.add_argument("--config", required=True, help="Config YAML file")
parser.add_argument("--output", required=True, help="Output metrics JSON")
parser.add_argument("--log-file", required=True, help="Log file")

args = parser.parse_args()

# Start timer
start_time = time.time()

# Logging setup
logging.basicConfig(
   filename=args.log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Program Started")

print("All libraries imported successfully!")


with open(args.config, "r") as file:
    config = yaml.safe_load(file)

print("Config Loaded:")
print(config)
logging.info(f"Config Loaded: {config}")

# Set random seed
np.random.seed(config["seed"])


try:
    df = pd.read_csv(args.input)

    if "close" not in df.columns:
        raise ValueError

except:
    df = pd.read_csv(args.input, header=None)
    df = df[0].str.split(",", expand=True)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
logging.info(f"Rows Loaded: {len(df)}")
print("\nCSV Loaded Successfully\n")
print(df.head())
logging.info(f"Rows Loaded: {len(df)}")

# Validate Dataset

if df.empty:
    print("Error: CSV is empty")
    exit()

required_columns = [
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume_btc",
    "volume_usd"
]

for col in required_columns:
    if col not in df.columns:
        print(f"Error: {col} column missing")
        exit()

print("\nDataset Validation Successful\n")


# Convert numeric columns

numeric_columns = [
    "open",
    "high",
    "low",
    "close",
    "volume_btc",
    "volume_usd"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col])


# Rolling Mean

window = config["window"]

df["rolling_mean"] = df["close"].rolling(window=window).mean()

print("Rolling Mean Calculated\n")
print(df[["close", "rolling_mean"]].head(10))
logging.info("Rolling Mean Calculated")

# Generate Signal

df["signal"] = np.where(
    df["close"] > df["rolling_mean"],
    1,
    0
)

print("\nSignals Generated\n")
print(df[["close", "rolling_mean", "signal"]].head(10))
logging.info("Signals Generated")

# Calculate Metrics
# End timer
end_time = time.time()

latency_ms = round((end_time - start_time) * 1000)

signal_rate = float(df["signal"].mean())

metrics = {
    "version": config["version"],
    "rows_processed": len(df),
    "metric": "signal_rate",
    "value": round(signal_rate, 4),
    "latency_ms": latency_ms,
    "seed": config["seed"],
    "status": "success"
}

with open(args.output, "w") as file:
    json.dump(metrics, file, indent=4)


print("\nFinal Metrics")
print(json.dumps(metrics, indent=4))
logging.info(f"Metrics: {metrics}")

print("\nmetrics.json created")

logging.info("Metrics calculated successfully")


# Save Processed Dataset

df.to_csv("processed_data.csv", index=False)

print("processed_data.csv created")

logging.info("Processed data saved")


# Runtime

print(f"\nExecution Time: {latency_ms} ms")

logging.info(f"Execution Time: {latency_ms} ms")
logging.info("Program Finished")