from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.models.ticket_asignacion_model import (
    TicketAsignacion,
)

from app.models.falla_equipo_model import (
    FallaEquipo
)

from app.models.cambio_estilo_model import (
    CambioEstilo
)

from app.models.ticket_historial_model import (
    TicketHistorial,
)

from app.models.ticket_comentario_model import (
    TicketComentario,
)


from app.routes import supervisor_routes


from sqlalchemy import text

from app.database import (
    engine,
    Base,
)
from app.routes.mecanico_routes import (
    router as mecanico_router
)
from fastapi.staticfiles import StaticFiles

# IMPORT ALL MODELS
from app.models.user_model import User
from app.models.linea_model import Linea

from app.models.ticket_model import Ticket

from app.models.ticket_falla_model import (
    TicketFallaEquipo,
)

from app.models.ticket_cambio_model import (
    TicketCambioEstilo,
)

# IMPORT ROUTES
from app.routes.auth_routes import (
    router as auth_router,
)

from app.routes.ticket_routes import (
    router as ticket_router,
)
from app.routes.jefe_mecanicos_routes import (
    router as jefe_mecanicos_router,
)


# CREATE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React dev server
        "http://localhost:3000",   # Alternative React port
        "http://localhost:8000",   # FastAPI itself
    ],
    allow_credentials=True,
    allow_methods=["*"],           # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],           # Allow all headers
)

# INCLUDE ROUTERS
app.include_router(auth_router)

app.include_router(supervisor_routes.router)


app.include_router(
    mecanico_router
)

app.include_router(ticket_router)

app.include_router(jefe_mecanicos_router)

app.include_router(auth_router)

app.include_router(ticket_router)

app.include_router(
    jefe_mecanicos_router
)


@app.on_event("startup")
def startup_db_test():

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

            print(
                "\n✅ PostgreSQL Connected Successfully\n"
            )

            print(
                "\n✅ Using Schema: mechanics_db_schema\n"
            )

            print(
                "\n✅ Tables Created Successfully\n"
            )

    except Exception as e:

        print(
            "\n❌ PostgreSQL Connection Failed\n"
        )

        print(e)


@app.get("/")
def root():

    return {
        "message": "Skyrina Backend Running"
    }