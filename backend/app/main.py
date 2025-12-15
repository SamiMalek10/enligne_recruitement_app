from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import PlainTextResponse
import time

from app.config import settings
from app.database import connect_to_database, close_database_connection
from app.api import candidates, jobs, matching, analytics

# Prometheus metrics
REQUEST_COUNT = Counter(
    'recruitment_app_requests_total',
    'Total request count',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'recruitment_app_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Intelligent Recruitment Application with ML-based Matching"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware for metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    
    # Record metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response


# Event handlers
@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    await connect_to_database()
    print("Application started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    print("Shutting down application...")
    await close_database_connection()


# Include routers
app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(matching.router)
app.include_router(analytics.router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "metrics": "/metrics"
    }


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Prometheus metrics endpoint
@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()
