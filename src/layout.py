import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from config import LOGO_PATH

# =============================================================================
# Components
# =============================================================================

def create_navbar(app, logo):

    return dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=app.get_asset_url(logo),
                                    height="30px",
                                    className="pb-2"
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

def create_title():
    return dbc.Container(
        [
            html.P(
                "Controls",
                className="lead text-muted",
            ),
        ],
        class_name="text-center",
    )

# Used to add written description for items in picker
def create_purpose_row():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4("", className="card-title", id="purpose-title"),
                dcc.Markdown("", id="purpose-description"),
            ]
        ),
        id="purpose-card",
    )


def create_controls():
    return dbc.Card(
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
                        {"label": "User experience",
                         "value": "User experience"},
                        {"label": "Analytics", "value": "Analytics"},
                        {"label": "Audit", "value": "Audit"},
                    ],
                    value="all",
                    clearable=False
                ),
            ]
        ),
        html.Div(
            [
                # RETENTION
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
                # STORAGE TYPE
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
                # STORAGE TECHNOLOGY
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
                # FOCUS
                dbc.Label("Focus"),
                dcc.Slider(
                    id="num-levels",
                    min=2,
                    max=8,
                    step=1,
                    value=8,
                    marks={
                        2: "Top",  # mark 2 because root acts as level 1
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


def create_panels():
    return dbc.Container(
    [
        dbc.Row(create_title()),
        dbc.Row(create_controls())
    ]
)

# =============================================================================
# app layout
# =============================================================================


def create_layout(app):
    return dbc.Container(
    [
        create_navbar(app, LOGO_PATH),
        dbc.Row(
            [
                dbc.Col(create_panels(), md=3),
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
        dbc.Row(create_purpose_row()),
    ],
    fluid=True,
)
