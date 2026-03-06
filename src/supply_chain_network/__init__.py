import sys
from contextlib import asynccontextmanager

import fastapi

from . import read
from .impact_calculation import (
    get_affected_suppliers_multi_source_dijkstra,
    get_highest_impact_paths_multi_source_dijkstra,
    to_graph,
)

# NOTE This import only works if this file is part of a package;
# write your own pyproj.toml to enable this in your project.
from .models import (
    EventImpactInput,
    EventImpactOutput,
    HighestImpactInput,
    HighestImpactOutput,
)

__all__ = ["app"]

network = {}


@asynccontextmanager
async def lifespan(app: "fastapi.FastAPI"):
    global network
    # Use the default argument, which reads from `
    network = read.supply_chain_network_from_file()
    print(
        f"Supply chain network loaded with \x1b[1m{len(network):,} nodes\x1b[0m",
        file=sys.stderr,
    )
    # Load the ML model
    yield
    # Clean up the ML models and release the resources
    network.clear()


app = fastapi.FastAPI(
    title="Supplier Impact Analysis API",
    description="API for analyzing the impact of events on suppliers in a supply chain graph.",
    version="0.0.1",
    contact={
        "name": "Your Name",
        "email": "your.name@domain.com",
    },
    lifespan=lifespan,
)


@app.post("/event-impact", response_model=EventImpactOutput)
async def event_impact(input_data: EventImpactInput) -> EventImpactOutput:
    """
    Placeholder endpoint for event impact analysis.
    """
    return EventImpactOutput(
        affected_suppliers=list(
            get_affected_suppliers_multi_source_dijkstra(
                graph=to_graph(network),
                sources=set(input_data.impacted_by_event),
                tracked_targets=set(input_data.tracked_suppliers),
                min_impact=input_data.min_impact,
            )
        )
    )


@app.post("/highest-impact", response_model=HighestImpactOutput)
async def highest_impact(input_data: HighestImpactInput) -> HighestImpactOutput:
    """
    Placeholder endpoint for highest impact path analysis.
    """
    return HighestImpactOutput(
        highest_impacts=get_highest_impact_paths_multi_source_dijkstra(
            graph=to_graph(network),
            sources=set(input_data.impacted_by_event),
            tracked_targets=set(input_data.tracked_suppliers),
        )
    )


@app.get("/data")
async def get_data() -> dict:
    """
    Endpoint to retrieve the supply chain network data.

    This is primarily for debugging purposes; this is not part of the
    requirements.
    """
    return network
