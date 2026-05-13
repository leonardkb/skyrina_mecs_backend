import uuid

from sqlalchemy.orm import Session

from app.database import SessionLocal

# IMPORTANT
# IMPORT RELATED MODELS
from app.models.linea_model import Linea

from app.models.user_model import User

from app.core.security import hash_password


def create_users():

    db: Session = SessionLocal()

    try:

        users = []

        # =====================================
        # GET ALL LINES
        # =====================================

        lineas = db.query(Linea).order_by(
            Linea.numero.asc()
        ).all()

        # =====================================
        # 20 JEFE LINEA USERS
        # =====================================

        for i in range(1, 21):

            username = f"jefe_linea_{i}"

            existing_user = db.query(User).filter(
                User.username == username
            ).first()

            if existing_user:
                continue

            linea = next(

                (
                    l for l in lineas
                    if l.numero == i
                ),

                None
            )

            users.append(

                User(

                    id=uuid.uuid4(),

                    username=username,

                    nombre=f"Jefe Linea {i}",

                    hashed_password=hash_password(
                        f"jefe_l{i}"
                    ),

                    role="jefe_linea",

                    linea_id=(
                        linea.id
                        if linea
                        else None
                    ),

                    status=True,
                )
            )

        # =====================================
        # JEFE MECANICOS
        # =====================================

        existing_jefe_mec = db.query(User).filter(
            User.username == "jefe_mecanicos"
        ).first()

        if not existing_jefe_mec:

            users.append(

                User(

                    id=uuid.uuid4(),

                    username="jefe_mecanicos",

                    nombre="Jefe Mecanicos",

                    hashed_password=hash_password(
                        "jefe_mec"
                    ),

                    role="jefe_mecanicos",

                    status=True,
                )
            )

        # =====================================
        # MECANICOS
        # =====================================

        mechanics = [

            {
                "username":
                    "fernando_reyes",

                "nombre":
                    "Fernando Reyes",

                "password":
                    "123456",
            },

            {
                "username":
                    "gregoro_cuevas",

                "nombre":
                    "Gregoro Cuevas",

                "password":
                    "123456",
            },

            {
                "username":
                    "jose_luis_carcano",

                "nombre":
                    "Jose Luis Carcano",

                "password":
                    "123456",
            },

            {
                "username":
                    "javier_juarez",

                "nombre":
                    "Javier Juarez",

                "password":
                    "123456",
            },

            {
                "username":
                    "emmanuel_corona",

                "nombre":
                    "Emmanuel Corona",

                "password":
                    "123456",
            },

            {
                "username":
                    "juan_carlos_vega",

                "nombre":
                    "Juan Carlos Vega",

                "password":
                    "123456",
            },

            {
                "username":
                    "ivan_becerra",

                "nombre":
                    "Ivan Becerra",

                "password":
                    "123456",
            },
        ]

        for mechanic in mechanics:

            existing_mec = db.query(User).filter(
                User.username ==
                mechanic["username"]
            ).first()

            if existing_mec:
                continue

            users.append(

                User(

                    id=uuid.uuid4(),

                    username=
                        mechanic["username"],

                    nombre=
                        mechanic["nombre"],

                    hashed_password=
                        hash_password(
                            mechanic["password"]
                        ),

                    role="mecanico",

                    status=True,
                )
            )

        # =====================================
        # SUPERVISOR
        # =====================================

        existing_supervisor = db.query(User).filter(
            User.username == "supervisor"
        ).first()

        if not existing_supervisor:

            users.append(

                User(

                    id=uuid.uuid4(),

                    username="supervisor",

                    nombre="Supervisor",

                    hashed_password=hash_password(
                        "supervisor"
                    ),

                    role="supervisor",

                    status=True,
                )
            )

        # =====================================
        # SAVE USERS
        # =====================================

        if users:

            db.add_all(users)

            db.commit()

            print(
                f"\n✅ {len(users)} users created successfully\n"
            )

        else:

            print(
                "\nℹ️ Users already exist\n"
            )

    except Exception as e:

        db.rollback()

        print(
            "\n❌ Error creating users\n"
        )

        print(e)

    finally:

        db.close()


if __name__ == "__main__":

    create_users()