from .main import app
from .demo_assessment import router as demo_assessment_router

app.include_router(demo_assessment_router)
