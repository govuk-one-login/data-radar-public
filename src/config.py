# src/config.py
import os
from helpers import pdAutoRead

# 
# Base Directories
#
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory where  all the data & config backing the data radar is contained
DATA_DIR = os.path.join(BASE_DIR, "data")

# Directory where static assets like CSS, favicon, logo, etc is stored
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Selected domain for the radar
SELECTED_DOMAIN = "Concepts"

# 
# Paths to specific files
#

# Data Paths
RADAR_DATA_DOMAINS_PATH = os.path.join(DATA_DIR, "radar_data_domains.csv")
RADAR_COLOURS_PATH = os.path.join(DATA_DIR, "radar_data_colours.csv")
PURPOSE_PATH = os.path.join(DATA_DIR, "purpose.txt")

# Asset paths
LOGO_PATH = "govuk-logotype-crown.png"


def _load_radar_data_domains():
    """Load the radar data configuration."""
    return pdAutoRead(RADAR_DATA_DOMAINS_PATH)

def _get_radar_data_path(radar_data_domains, selected_domain):
    """Determine the path to the radar data file based on the selected domain."""
    data_filename = radar_data_domains[
        radar_data_domains["domain"] == selected_domain
    ]["value"].values[0]
    return os.path.join(DATA_DIR, data_filename)

def _load_radar_colours():
    """Load the colour scheme for the radar."""
    radar_colours_df = pdAutoRead(RADAR_COLOURS_PATH)
    return radar_colours_df["hex"].tolist()

def _load_purpose():
    """Load the purpose description for the radar."""
    with open(PURPOSE_PATH, 'r', newline='') as rf:
        return rf.read()

# Load configurations
radar_data_domains = _load_radar_data_domains()
RADAR_DATA_PATH = _get_radar_data_path(radar_data_domains, SELECTED_DOMAIN)
radar_colours = _load_radar_colours()
purpose = _load_purpose()
