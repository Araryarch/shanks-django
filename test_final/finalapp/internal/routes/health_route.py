"""Health Check Routes"""
from shanks import App
from dto.base_dto import BaseDTO

router = App()


@router.get("/api/health")
def health(req):
    """Health check endpoint"""
    return BaseDTO.success(
        data={"service": "finalapp"},
        message="Service is healthy"
    )
