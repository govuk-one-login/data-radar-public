"""
GOV.UK One Login Data Radar
27 Nov 2023
Dan Budden, Dominic Stevenson, Jim O'Connell, Nadine Hakedin

Forked with permission from 6point6 data radar
30 Nov 2021
Dan Budden, Dominic Stevenson

"""

import dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks


def create_app():
    """Create and configure the Dash app."""

    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.FLATLY],
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1"
            },
        ],
        title='GOV.UK One Login Data Radar'
    )

    app.layout = create_layout(app)
    register_callbacks(app)

    return app


app = create_app()

# Expose the server for production use (e.g., Gunicorn)
server = app.server

if __name__ == "__main__":
    # This block will only execute when running the script directly
    # (i.e., for local development)
    app.run_server(
        host="0.0.0.0",
        port=8050,
        debug=True,
        dev_tools_hot_reload=True
    )
