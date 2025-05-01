# src/data.py
from helpers import pdAutoRead
from config import RADAR_DATA_PATH, radar_data_domains, SELECTED_DOMAIN

# Load radar data
radar_df = pdAutoRead(RADAR_DATA_PATH)

# Add domain to the dataframe
radar_df["domain"] = radar_data_domains[radar_data_domains["domain"] == SELECTED_DOMAIN]["domain"].values[0]

LEVELS = ["domain", "level 1", "level 2", "level 3", "level 4", "level 5", "level 6", "level 7"]
