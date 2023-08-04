import importlib
import os

import fhir.resources
from fastapi import Depends, Request, Response, status

from .fhirstarter import FHIRStarter
from .interactions import InteractionContext
from .providers import FHIRProvider
from .utils import categorize_fhir_request, parse_fhir_request

__all__ = [
    "Depends",
    "FHIRProvider",
    "FHIRStarter",
    "InteractionContext",
    "Request",
    "Response",
    "categorize_fhir_request",
    "parse_fhir_request",
    "status",
]

# Ensure that the specified FHIR sequence is supported by FHIRStarter
FHIR_SEQUENCE = os.getenv("FHIR_SEQUENCE", "R5")
SUPPORTED_FHIR_VERSIONS = ("STU3", "R4", "R4B", "R5")
assert (
    FHIR_SEQUENCE in SUPPORTED_FHIR_VERSIONS
), f"FHIR sequence must be one of: {', '.join(SUPPORTED_FHIR_VERSIONS)}"

# Ensure that a compatible version of fhir.resources is installed
FHIR_RESOURCES_VERSION = importlib.metadata.version("fhir.resources")
if FHIR_SEQUENCE == "R4":
    assert (
        FHIR_RESOURCES_VERSION == "6.4.0"
    ), "fhir.resources package version must be 6.4.0 for FHIR R4 sequence"
else:
    assert (
        FHIR_RESOURCES_VERSION >= "7.0.0"
    ), "fhir.resources package version must be 7.0.0 or greater for FHIR STU3, R4B, and R5 sequences"
    assert (
        fhir.resources.__fhir_version__ == "5.0.0"
    ), f"fhir.resources package references unexpected FHIR version {fhir.resources.__fhir_version__}"
