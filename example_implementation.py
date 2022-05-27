import uvicorn
from fhir.resources.patient import Patient
from starlette.responses import RedirectResponse

from fhirstarter import FHIRProvider, FHIRStarter
from fhirstarter.exceptions import FHIRResourceNotFoundError


# Define a provider for a resource (the functions will define what FHIR operations are supported for
# the resource).
class PatientProvider(FHIRProvider):
    def resource_obj_type(self) -> type:
        return Patient

    @staticmethod
    async def read(id_: str) -> Patient:
        # All Canvas-to-FHIR mapping code for a Patient read operation goes here. For a read
        # operation, a GraphQL request is issued, and then the result is mapped on to the FHIR
        # Patient resource to be returned.

        if id_ != "bilbo":
            raise FHIRResourceNotFoundError

        patient = Patient(**{"name": [{"family": "Baggins", "given": ["Bilbo"]}]})

        return patient


# Create the app
app = FHIRStarter(title="FHIRStarter Example Implementation")

# Add the patient provider to the app. This will automatically generate the API routes that the
# providers need (e.g. create, read, search, and update).
app.add_providers(PatientProvider())


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    """Redirect main page to API docs."""
    return RedirectResponse("/docs")


if __name__ == "__main__":
    # Start the server
    uvicorn.run("example_implementation:app", reload=True)