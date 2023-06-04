from src.db import SESSION_MAKER, ENGINE
from src.model import BASE

if __name__ == "__main__":
    print("Initialization of database...")
    db_session = SESSION_MAKER()

    # clearing database
    print("Dropping tables... ", end="")
    BASE.metadata.drop_all(bind=ENGINE)

    # creating all tables
    print("Creating tables... ", end="")
    BASE.metadata.create_all(bind=ENGINE)

    db_session.close()

    print("Done! We are on mission from God!")
