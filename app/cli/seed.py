from app.db.database import SessionLocal
from app.services.rbacSeedService import RbacSeedService

def main():
    session = SessionLocal()

    try:
        RbacSeedService(session=session).seed()
        print("RBAC + users seeded successfully")
    except Exception as error:
        session.rollback()
        print("Seeding failed:", error)
        raise
    finally:
        session.close()



if __name__ == "__main__":
    main()