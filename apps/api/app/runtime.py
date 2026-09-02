from .main import app
from .demo_assessment import router as demo_assessment_router
from .organization_registration import router as organization_registration_router

app.include_router(demo_assessment_router)
app.include_router(organization_registration_router)
