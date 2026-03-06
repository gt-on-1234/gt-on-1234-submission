"""
Input/Output models for the :mod:`fastapi` host.
"""

from typing import TypeAlias, TypedDict

from pydantic import BaseModel, ConfigDict, Field, alias_generators

COMMON_MODEL_CONFIG = ConfigDict(
    populate_by_name=True,
    alias_generator=alias_generators.to_camel,
)
"""
Shared configuration for Pydantic models to use camelCase aliases.
"""

SupplierIndex: TypeAlias = "str"
"""
A unique identifier for a supplier.
"""

SupplierIndices: TypeAlias = "list[SupplierIndex]"
"""
A list of unique identifiers for suppliers.
"""

ImpactPath: TypeAlias = "SupplierIndices"
"""
A list of supplier IDs representing a path of impact.
"""

ImpactScore: TypeAlias = "float"
"""
A numerical score representing the impact level.
"""


class SupplyChainRelationship(TypedDict):
    """
    A typed dictionary representing a relationship in the supply chain network.
    """

    index: "SupplierIndex"
    impact: "float"


class SupplyChainNode(TypedDict):
    """
    A typed dictionary representing a node in the supply chain network.
    """

    index: "SupplierIndex"
    neighbours: "list[SupplyChainRelationship]"


SupplyChainNetwork: TypeAlias = "dict[SupplierIndex, SupplyChainNode]"
"""
A type alias for the supply chain data structure in our provided
data files.
"""


class ImpactPathAndScore(BaseModel):
    """
    Model representing an impact path along with its associated impact.
    """

    path: "ImpactPath"
    impact: "ImpactScore"


class EventImpactInput(BaseModel):
    """
    Model representing the input for an event impact analysis.
    """

    model_config = COMMON_MODEL_CONFIG

    impacted_by_event: "SupplierIndices" = Field(
        ...,
        description="List of supplier IDs directly impacted by the event.",
    )
    tracked_suppliers: "SupplierIndices" = Field(
        ...,
        description="List of supplier IDs being tracked for impact analysis.",
        max_length=50,
    )
    min_impact: "ImpactScore" = Field(
        default=0.3,
        description="Minimum impact score threshold to consider. Optional, defaults to 0.3.",
        ge=0.0,
        le=1.0,
    )


class EventImpactOutput(BaseModel):
    """
    Model representing the output of an event impact analysis.
    """

    model_config = COMMON_MODEL_CONFIG

    affected_suppliers: SupplierIndices = Field(
        default_factory=list,
        description="List of supplier IDs affected by the event.",
    )


class HighestImpactInput(BaseModel):
    """
    Model representing the input for highest impact analysis.
    """

    model_config = COMMON_MODEL_CONFIG

    impacted_by_event: "SupplierIndices" = Field(
        ...,
        description="List of supplier IDs directly impacted by the event.",
    )
    tracked_suppliers: "SupplierIndices" = Field(
        ...,
        description="List of supplier IDs being tracked for impact analysis.",
        max_length=50,
    )


class HighestImpactOutput(BaseModel):
    """
    Model representing the output of highest impact analysis.
    """

    model_config = COMMON_MODEL_CONFIG

    highest_impacts: "dict[SupplierIndex, ImpactPathAndScore]" = Field(
        default_factory=dict,
        description=(
            "For each tracked supplier, the highest impact path and its score. "
            "If no impact, the tracked supplier is omitted from the dictionary."
        ),
    )
