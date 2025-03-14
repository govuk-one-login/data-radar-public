"""

GOV.UK One Login Data Radar
Feb 2025
dan budden, nadine hakedin, jim o'connell

Forked with permission from 6point6 data radar
30 Nov 2021
dan budden, dominic stevenson

dash app in python3

"""

# =============================================================================
# imports
# =============================================================================

# core
import os
import pandas as pd
import ast

# dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# plotly
import plotly.express as px

# =============================================================================
# helper functions
# =============================================================================

from pdAutoRead import pdAutoRead

# =============================================================================
# collect and/or set configs / variables
# =============================================================================

# this refers to the data domain we are displaying, and drives config
# options may include conceptual data entities, or events
# we pick a default here, with an option to choose other domains in callbacks

selected_domain = "Concepts"
#selected_domain = "Tessier-Ashpool"

# get the configs location, in any os
radar_data_config_path = os.path.join(
    os.getcwd(), "data", "radar_data_index.csv")

# read in the configs
radar_data_config = pdAutoRead(radar_data_config_path)
del radar_data_config_path

# grab the radar data filename from configs based on selected domain
data_filename = radar_data_config[radar_data_config["domain"] == 
    selected_domain]["value"].values[0]

# add the radar data filepath, for any os
radar_data_path = os.path.join(os.getcwd(), "data", data_filename)

# get the data radar colour scheme location, if using a separate file for color
radar_colours_path = os.path.join(
    os.getcwd(), "data", "radar_data_colours.csv")

# get the purpose location, if using a separate file to manage this
purpose_path = os.path.join(os.getcwd(), "data", "purpose.txt")

# =============================================================================
# ingest assets and data
# =============================================================================

# read in the data radar file
radar_df = pdAutoRead(radar_data_path)
del radar_data_path

# read in the data radar colour scheme
radar_colours = pdAutoRead(radar_colours_path)
del radar_colours_path
# dash sunburst will want a list of colours
radar_colours = radar_colours["hex"].to_list()

# logo - we don't need os.path here, dash knows to parse from assets folder
logo = "govuk-logotype-crown.png"

# purpose of data collection, processing, and storage, in markdown format
# can be read as text, dash will convert to markdown for us 
with open(purpose_path,'r',newline='') as rf:
    purpose = rf.read()

# =============================================================================
# prepare data
# =============================================================================

# to make the sunburst have a hollow centre label, add a column with domain
radar_df["domain"] = radar_data_config[radar_data_config["domain"] == 
    selected_domain]["domain"].values[0]

# convert plain text to dict so elements can be selected by index 
purpose = ast.literal_eval(purpose)

# =============================================================================
# initialise app
# =============================================================================

app = dash.Dash(
    external_stylesheets=[dbc.themes.FLATLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
    title='GOV.UK One Login Data Radar'
)

# =============================================================================
# bootstrap components
# =============================================================================


navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src=app.get_asset_url(logo),
                                height="30px",
                                className="pb-2" # align crown logo and text
                            )
                        ),
                        dbc.Col(
                            dbc.NavbarBrand("GOV.UK One Login Data Radar",
                                            className="ms-3",
                                            style={"color": "#FFFFFF"},
                                            )
                        ),
                    ],
                    align="centre",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
                className="navbar-brand d-flex align-items-center",
            ),
        ]
    ),
    class_name="navbar",
    color="#000000",
    sticky='top'
)

title = dbc.Container(
    [
        html.P(
            "Controls",
            className="lead text-muted",
        ),
    ],
    class_name="text-center",
)

controls = dbc.Card(
    [
        html.Div(
            [
                #SEARCH
                dbc.Label("Explore a Data Entity"),
                dcc.Dropdown(
                    id="search-picker",
                    options=[],
                    multi=False,
                    placeholder="Type or Select"
                ),
            ]
        ),
        html.Div(
            [
                # COLOUR 
                dbc.Label("Colours"),
                dcc.Dropdown(
                    id="colour-picker",
                    options=[
                        {"label": view, "value": view}
                        for view in ["Default"]
                    ],
                    value="Default",
                    clearable=False
                ),
            ]
        ),
        html.Div(
            [
                # PURPOSE
                dbc.Label("Purpose"),
                dcc.Dropdown(
                    id="purpose-picker",
                    # TODO set these role options in user configs
                    options=[
                        {"label": "Show all", "value": "all"},
                        {"label": "Authentication", "value": "Authentication"},
                        {"label": "Identity", "value": "Identity"},
                        {"label": "User experience", "value": "User experience"},
                        {"label": "Analytics", "value": "Analytics"},
                        {"label": "Audit", "value": "Audit"},
                    ],
                    value="all",
                    clearable=False,
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Retention"),
                # TODO make this dynamic so it only displays good values
                dcc.Dropdown(
                    id="retention-picker",
                    value="all",
                    clearable=False,
                ),
            ]
        ),
        
        html.Div(
            [
                dbc.Label("Storage Type"),
                dcc.Dropdown(
                    id="storage-type-filter",
                    options=[
                        {"label": "Show all", "value": "all"},
                        {"label": "Ephemeral data", "value": "ephemeral"},
                        {"label": "Persisted data", "value": "persisted"},
                    ],
                    value="all",  # Default selection
                    clearable=False,
                ),
            ]
        ),
                
        html.Div(
            [
                dbc.Label(" Storage Technology"),
                dcc.Dropdown(
                    id="storage-technology-picker",
                    value="all",
                    clearable=False,
                ),
            ]
        ),
        
        html.Div(
            [
                dbc.Label("Focus"),
                dcc.Slider(
                    id="num-levels",
                    min=2,
                    max=8,
                    step=1,
                    value=8,
                    marks={
                        2: "Top", # mark 2 because root acts as level 1
                        3: "",
                        4: "",
                        5: "",
                        6: "",
                        7: "",
                        8: "All",
                    },
                ),
            ]
        ),
    ],
    body=True,
)

# Used to add written description for items in picker
purpose_row = dbc.Card(
    dbc.CardBody(
        [
            html.H4("", className="card-title", id="purpose-title"),
            dcc.Markdown("", id="purpose-description"),
        ]
    ),
    id="purpose-card",
)

panels = dbc.Container(
    [
        dbc.Row(title),
        dbc.Row(controls)
    ]
)


# =============================================================================
# app layout
# =============================================================================

app.layout = dbc.Container(
    [
        navbar,
        dbc.Row(
            [
                dbc.Col(panels, md=3),
                dbc.Col(
                    dcc.Graph(
                        id="data-radar", 
                        style={'width': '130vh', 'height': '110vh'},
                        responsive=True
                    ),
                    md=9
                ),
            ],
            align="center",
        ),
        dbc.Row(purpose_row),
    ],
    fluid=True,
)

# =============================================================================
# callbacks
# =============================================================================
# Update data radar
@app.callback(
    Output("data-radar", "figure"),
    Input("search-picker", "value"),
    Input("colour-picker", "value"),
    Input("purpose-picker", "value"),
    Input("retention-picker", "value"),
    Input("storage-technology-picker", "value"),
    Input("storage-type-filter", "value"),
    Input("num-levels", "value"),
)
def pop_data_radar(
    searchValue,
    selectedView,
    selectedPurpose,
    selectedRetention,
    selectedStorageTechnology,
    selectedStorageType,
    selectedNumLevels,
):


#The below functions apply conditional transformations to the values in the df 
    #based on the dimensions enabling independent filtering by each criterion:
    df = radar_df.copy()

    # Check for Storage Technology column -> create 'Storage Type' column
    storage_column_name = None
    for col in df.columns:
        if "storage technology" in col.lower():
            storage_column_name = col
            break

    # Apply search filter to columns 1 to 7 only
    if searchValue:
        search_columns = df.columns[0:8]
        df = df[df[search_columns].apply(lambda row: searchValue in row.values, axis=1)]

    # Create 'Storage Type' based on "AWS Lambda" (Ephemeral) or not (Persisted)
    if storage_column_name:
        df["Storage Type"] = df[storage_column_name].apply(
            lambda x: "Ephemeral" if "AWS Lambda" in str(x) else "Persisted"
        )
    else:
        df["Storage Type"] = "Persisted"  # Default to Persisted if no 'Storage Technology' column found

    # Filter by Purpose (if selected)
    if selectedPurpose and selectedPurpose != "all":
        df = df[df[selectedPurpose] == "y"]

    # Filter by Retention (if selected)
    if selectedRetention and selectedRetention != "all":
        retention_cols = [col for col in df.columns if "retention" in col.lower()]
        df = df[df[retention_cols].apply(lambda row: selectedRetention in row.values, axis=1)]

    # Filter by Storage Technology (if selected)
    if selectedStorageTechnology and selectedStorageTechnology != "all":
        storage_cols = [col for col in df.columns if "storage technology" in col.lower()]
        df = df[df[storage_cols].apply(lambda row: selectedStorageTechnology in row.values, axis=1)]

    # Filter by Storage Type (if selected), with case-insensitive comparison
    if selectedStorageType and selectedStorageType != "all":
        df = df[df["Storage Type"].str.lower() == selectedStorageType.lower()]

    # If no data is available after filtering = return a placeholder page
    if df.empty:
        return px.scatter(title="No data available for selected filters")

    levels = [
        "domain",
        "level 1",
        "level 2",
        "level 3",
        "level 4",
        "level 5",
        "level 6",
        "level 7",
    ]

    # Define custom data columns correctly
    custom_data_columns = [
        "Authentication retention",
        "Identity retention",
        "User experience retention",
        "Analytics retention",
        "Audit retention",
        "Authentication Storage Technology",
        "Identity Storage Technology",
        "Analytics Storage Technology",
        "Audit Storage Technology",
    ]

    # Ensure data has all necessary columns
    df[custom_data_columns] = df[custom_data_columns].fillna("N/A")

    if selectedView == "Default":
        fig = px.sunburst(
            df,
            path=levels[:selectedNumLevels],
            color_discrete_sequence=radar_colours,
            custom_data=custom_data_columns,  # Use the correct column list
        )

    # Add hover information
    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "<b><span style='font-size:18px;'>%{label}</span></b>",
                "<i style='font-size:14px; text-decoration: underline;'>Retention Period & Data Storage Technology:</i><br>",
                "<b>Authentication:</b> %{customdata[0]} | <b>Storage:</b> %{customdata[5]}<br>",
                "<b>Identity:</b> %{customdata[1]} | <b>Storage:</b> %{customdata[6]}<br>",
                "<b>User Experience:</b> %{customdata[2]}<br>",
                "<b>Analytics:</b> %{customdata[3]} | <b>Storage:</b> %{customdata[7]}<br>",
                "<b>Audit:</b> %{customdata[4]} | <b>Storage:</b> %{customdata[8]}<br>",
            ]
        ),
        insidetextorientation="auto",
    )

    # Update font and layout
    fig.update_layout(
        font_family="DM Sans",
        uniformtext=dict(minsize=8, mode="hide"),
    )

    return fig


def filter_data(selectedPurpose, selectedRetention, selectedStorageTechnology):
    """
    Filters the dataset based on the selected Purpose, Retention, and Storage Technology.
    Ensures filtering works across multiple columns dynamically.
    """
    filtered_df = radar_df.copy()

    # Apply Purpose Filter
    if selectedPurpose and selectedPurpose != "all":
        filtered_df = filtered_df[filtered_df[selectedPurpose] == "y"]

    # Apply Retention Filter
    if selectedRetention and selectedRetention != "all":
        retention_cols = [col for col in radar_df.columns if "retention" in col.lower()]
        filtered_df = filtered_df[filtered_df[retention_cols].apply(lambda row: selectedRetention in row.values, axis=1)]

    # Apply Storage Technology Filter
    if selectedStorageTechnology and selectedStorageTechnology != "all":
        storage_cols = [col for col in radar_df.columns if "storage technology" in col.lower()]
        filtered_df = filtered_df[filtered_df[storage_cols].apply(lambda row: selectedStorageTechnology in row.values, axis=1)]

    return filtered_df

################################################################################
# Update Search Picker
################################################################################
@app.callback(
    Output("search-picker", "options"),
    Input("search-picker", "value"),
)
def update_search_options(search_value):
    # Get unique values across all relevant columns (Level 1 to Level 7)
    unique_values = pd.concat([radar_df[col] for col in radar_df.columns if 'level' in col]).unique()

    if search_value:
        filtered_values = [value for value in unique_values if search_value.lower() in str(value).lower()]
    else:
        filtered_values = unique_values

    return [{'label': str(value), 'value': value} for value in filtered_values]

################################################################################
# Update Purpose Picker
################################################################################
@app.callback(
    Output("purpose-picker", "options"),
    Input("storage-technology-picker", "value"),
    Input("retention-picker", "value"),  # Update Purpose dropdown based on selected filters
    Input("search-picker", "value")  # Trigger update when search value changes
)
def update_purpose_options(selectedStorageTechnology, selectedRetention, search_value):
    df_filtered = radar_df.copy()  # Copy the dataset

    # Apply search filter if a search value is provided
    if search_value:
        search_columns = df_filtered.columns[0:8]  # Consider only the first 8 columns for search
        df_filtered = df_filtered[df_filtered[search_columns].apply(lambda row: search_value in row.values, axis=1)]

    # If no data remains after applying the search filter
    if df_filtered.empty:
        return [{"label": "No data found", "value": "none"}]

    # Define the mapping of purposes to their respective columns
    purpose_column_mapping = {
        "Authentication": "Authentication",
        "Audit": "Audit",
        "Identity": "Identity",
        "Analytics": "Analytics",
        "User experience": "User experience"
    }

    # Initialise purpose options with "Show All"
    purpose_options = [{"label": "Show All", "value": "all"}]

    # If a Storage Technology filter is selected, filter by that
    if selectedStorageTechnology and selectedStorageTechnology != "all":
        storage_cols = [col for col in df_filtered.columns if "storage technology" in col.lower()]
        df_filtered = df_filtered[df_filtered[storage_cols].apply(lambda row: selectedStorageTechnology in row.values, axis=1)]

    # If a Retention filter is selected, apply it
    if selectedRetention and selectedRetention != "all":
        retention_cols = [col for col in df_filtered.columns if "retention" in col.lower()]
        df_filtered = df_filtered[df_filtered[retention_cols].apply(lambda row: selectedRetention in row.values, axis=1)]

    # If no data remains after applying filters
    if df_filtered.empty:
        return [{"label": "No data found", "value": "none"}]

    # Initialise a set to store the purposes that match the filters
    filtered_purposes = set()

    # Check each purpose group and see if there is any data that matches the filters
    for purpose, column in purpose_column_mapping.items():
        if column in df_filtered.columns:
            # Only include purposes where the filtered DataFrame contains matching data
            if df_filtered[df_filtered[column] == "y"].shape[0] > 0:
                filtered_purposes.add(purpose)

    # If no filtered purposes are found, return "No data found"
    if not filtered_purposes:
        return [{"label": "No data found", "value": "none"}]

    # Add filtered purpose options to the dropdown
    purpose_options += [{"label": purpose, "value": purpose} for purpose in filtered_purposes]

    return purpose_options

################################################################################
# Update Retention Picker 
################################################################################
@app.callback(
    Output("retention-picker", "options"),
    Input("purpose-picker", "value"),  # Update Retention dropdown based on selected Purpose
    Input("search-picker", "value")  # Trigger update when search value changes
)
def update_retention_options(selectedPurpose, search_value):
    df_filtered = radar_df.copy()  # Copy the dataset

    # Apply search filter if a search value is provided
    if search_value:
        search_columns = df_filtered.columns[0:8]
        df_filtered = df_filtered[df_filtered[search_columns].apply(lambda row: search_value in row.values, axis=1)]

    # Define mapping of purposes to their respective retention columns
    retention_column_mapping = {
        "Authentication": "Authentication retention",
        "Audit": "Audit retention",
        "Identity": "Identity retention",
        "Analytics": "Analytics retention"
    }

    # Initialise retention options with "Show All"
    retention_options = [{"label": "Show All", "value": "all"}]

    # If no Purpose is selected, show ALL unique retention values
    if not selectedPurpose or selectedPurpose == "all":
        all_retention_values = set()
        for col in retention_column_mapping.values():
            if col in df_filtered.columns:
                all_retention_values.update(df_filtered[col].dropna().unique())

        # Add all unique retention values to the dropdown options
        retention_options += [{"label": value, "value": value} for value in sorted(all_retention_values)]
        return retention_options

    # If a Purpose is selected, find the corresponding retention column
    retention_column_name = retention_column_mapping.get(selectedPurpose)
    if not retention_column_name or retention_column_name not in df_filtered.columns:
        return retention_options  # Return only "Show All" if column is missing

    # Filter DataFrame to include only rows where the selected Purpose is present
    df_filtered = df_filtered[df_filtered[selectedPurpose] == "y"]

    # Get unique retention values in the filtered data
    unique_retention_values = df_filtered[retention_column_name].dropna().unique()

    # Add filtered retention options
    retention_options += [{"label": value, "value": value} for value in sorted(unique_retention_values)]
    
    return retention_options

################################################################################
# Update Storage Technology Picker 
################################################################################
@app.callback(
    Output("storage-technology-picker", "options"),
    Input("purpose-picker", "value"),  # When Purpose is selected, update options
    Input("storage-type-filter", "value"),  # When Storage Type is selected, update options
    Input("search-picker", "value")  # Apply search filtering
)
def update_storage_technology_options(selectedPurpose, selectedStorageType, search_value):
    df_filtered = radar_df.copy()  # Work on a copy of the dataset

    # Apply search filter if a search value is provided
    if search_value:
        search_columns = df_filtered.columns[0:8]  # Consider only first 8 columns for search
        df_filtered = df_filtered[df_filtered[search_columns].apply(lambda row: search_value in row.values, axis=1)]

    # Define the mapping of purposes to their respective storage technology columns
    storage_column_mapping = {
        "Authentication": "Authentication Storage Technology",
        "Audit": "Audit Storage Technology",
        "Identity": "Identity Storage Technology",
        "Analytics": "Analytics Storage Technology"
    }

    # Initialise dropdown options with "Show All"
    storage_technology_options = [{"label": "Show All", "value": "all"}]

    # If no Purpose is selected, get all available storage technologies
    if not selectedPurpose or selectedPurpose == "all":
        all_storage_technologies = set()
        for col in storage_column_mapping.values():
            if col in df_filtered.columns:
                all_storage_technologies.update(df_filtered[col].dropna().unique())

        # Apply Storage Type filter if selected
        if selectedStorageType and selectedStorageType != "all":
            df_filtered["Storage Type"] = df_filtered.apply(
                lambda row: "Ephemeral" if "AWS Lambda" in str(row[storage_column_mapping.values()]) else "Persisted",
                axis=1
            )
            all_storage_technologies = df_filtered[df_filtered["Storage Type"].str.lower() == selectedStorageType.lower()][
                storage_column_mapping.values()].stack().unique()

        storage_technology_options += [{"label": tech, "value": tech} for tech in sorted(all_storage_technologies)]
        return storage_technology_options

    # If a Purpose is selected, filter accordingly
    storage_column_name = storage_column_mapping.get(selectedPurpose)
    if not storage_column_name or storage_column_name not in df_filtered.columns:
        return storage_technology_options  # Return only "Show All" if column is missing

    # Filter DataFrame by Purpose
    df_filtered = df_filtered[df_filtered[selectedPurpose] == "y"]

    # Apply Storage Type filter if selected
    if selectedStorageType and selectedStorageType != "all":
        df_filtered["Storage Type"] = df_filtered.apply(
            lambda row: "Ephemeral" if "AWS Lambda" in str(row[storage_column_name]) else "Persisted",
            axis=1
        )
        df_filtered = df_filtered[df_filtered["Storage Type"].str.lower() == selectedStorageType.lower()]

    # Get unique storage technologies from the filtered data
    unique_storage_technologies = df_filtered[storage_column_name].dropna().unique()

    # Convert to dropdown options
    storage_technology_options += [{"label": tech, "value": tech} for tech in sorted(unique_storage_technologies)]
    
    return storage_technology_options

################################################################################
# Update Storage Type Picker 
################################################################################
@app.callback(
    Output("storage-type-filter", "options"),  # Update Storage Type dropdown
    Input("purpose-picker", "value"),
    Input("storage-technology-picker", "value"),
    Input("search-picker", "value")
)
def update_storage_type_options(selectedPurpose, selectedStorageTechnology, search_value):
    df_filtered = radar_df.copy()

    # Apply search filter if a search value is provided
    if search_value:
        search_columns = df_filtered.columns[0:8]
        df_filtered = df_filtered[df_filtered[search_columns].apply(lambda row: search_value in row.values, axis=1)]

    # Define the mapping of purposes to their respective storage technology columns
    storage_column_mapping = {
        "Authentication": "Authentication Storage Technology",
        "Audit": "Audit Storage Technology",
        "Identity": "Identity Storage Technology",
        "Analytics": "Analytics Storage Technology"
    }

    storage_type_options = [{"label": "Show All", "value": "all"}]

    if selectedPurpose and selectedPurpose != "all":
        storage_column_name = storage_column_mapping.get(selectedPurpose)
        if storage_column_name in df_filtered.columns:
            df_filtered = df_filtered[df_filtered[selectedPurpose] == "y"]

    if selectedStorageTechnology and selectedStorageTechnology != "all":
        storage_tech_columns = storage_column_mapping.values()
        df_filtered = df_filtered[df_filtered[storage_tech_columns].apply(
            lambda row: selectedStorageTechnology in row.values, axis=1
        )]

    # Dynamically determine Storage Type based on Storage Technology
    df_filtered["Storage Type"] = df_filtered.apply(
        lambda row: "Ephemeral" if any("AWS Lambda" in str(row[col]) for col in storage_column_mapping.values()) else "Persisted",
        axis=1
    )

    unique_storage_types = df_filtered["Storage Type"].dropna().unique()

    # Convert to dropdown options
    storage_type_options += [{"label": stype, "value": stype.lower()} for stype in sorted(unique_storage_types)]
    
    return storage_type_options

################################################################################
# Update Purpose Title
################################################################################
@app.callback(
    Output(component_id="purpose-title", component_property="children"),
    Input("purpose-picker", "value"),
)
def update_purpose_title(selectedPurpose):

    purposeNames = {
        "all": "",
        "Authentication": "Authentication",
        "Identity": "Identity",
        "User experience": "User experience",
        "Analytics": "Analytics",
        "Audit": "Audit",
    }

    return purposeNames.get(selectedPurpose, "")

################################################################################
# Update Purpose Description
################################################################################
@app.callback(
    Output(component_id="purpose-description", component_property="children"),
    Input("purpose-picker", "value"),
)
def update_purpose_description(selectedPurpose):

    purposeDescriptions = {
        "all": "All purposes are shown.",
        "Authentication": "This involves verifying a user's credentials—such as email address, password, and two-factor authentication—to grant access to government services. The authentication process ensures that only authorised users can sign in to services using their GOV.UK One Login.",
        "Identity": "This pertains to confirming a user's identity by collecting and validating personal information against authoritative sources. The identity verification process enables users to prove they are who they claim to be, allowing access to services that require a higher level of identity assurance.",
        "User experience": "This focuses on enhancing the usability and accessibility of the GOV.UK One Login service. By analysing how users interact with the service, improvements can be made to ensure a seamless and user-friendly experience. This includes allowing users to manage their sign-in details and view the services they've accessed through their account.",
        "Analytics": "This involves collecting data on how users engage with the GOV.UK One Login service to monitor performance and identify areas for improvement. With user consent, tools like Google Analytics are used to gather anonymized information about page visits, duration, navigation paths, and interactions. This data helps in refining the service to better meet user needs.",
        "Audit": "This relates to maintaining records of user interactions and data processing activities to ensure compliance with legal and regulatory requirements. Audit logs are kept to detect and prevent fraud, ensure data integrity, and provide accountability for actions taken within the GOV.UK One Login system. These logs are retained only as long as necessary for the specified purposes and are protected with appropriate security measures.",
    }

    return purposeDescriptions.get(selectedPurpose, "No description available.")


@app.callback(
    Output(component_id="purpose-row", component_property="style"),
    Input("purpose-picker", "value"),
)
def hide_purpose_row(selectedPurpose):

    if selectedPurpose != "all":
        return {"display": "block"}

    return {"display": "none"}

# =============================================================================
# app launch
# =============================================================================

# Expose the server for external / production use (e.g., Gunicorn)
server = app.server

# Run the server for development use
if __name__ == "__main__":
    app.run_server(
        host="0.0.0.0",
        port=8050,
        use_reloader=True,
        dev_tools_hot_reload=True
    )
