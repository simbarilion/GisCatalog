import argparse

from geoalchemy2 import WKTElement
from sqlalchemy.orm import Session

from app.db.models import Activity, Building, Organization, Phone
from app.db.session import SessionLocal

from .data import activities, buildings, organizations, phones


def seed_database(db: Session, clear: bool = False, only_if_empty: bool = False) -> None:
    """
    Заполняет базу тестовыми данными:
    1. Здания
    2. Виды деятельности
    3. Организации + телефоны + деятельность
    """
    if only_if_empty:
        existing = db.query(Organization).count()
        if existing > 0:
            print(f"База уже содержит {existing} организаций. Заполнение пропущено")
            return

    if clear:
        print("Очистка базы перед заполнением...")
        db.query(Phone).delete()
        db.query(Organization).delete()
        db.query(Activity).delete()
        db.query(Building).delete()
        db.commit()
        print("База очищена")

    print("Начинаем заполнение тестовыми данными...")

    building_objs = []
    for address, lat, lon in buildings:
        location = WKTElement(f"POINT({lon} {lat})", srid=4326)
        building = Building(address=address, location=location)
        db.add(building)
        building_objs.append(building)
    db.commit()
    print(f"Создано {len(building_objs)} зданий")

    activity_dict = {}  # name: activity_object
    for act_data in activities:
        parent = activity_dict.get(act_data["parent"]) if act_data["parent"] else None

        activity = Activity(name=act_data["name"], parent=parent, level=0 if parent is None else parent.level + 1)
        db.add(activity)
        db.flush()
        activity_dict[act_data["name"]] = activity
    db.commit()
    print(f"Создано {len(activities)} видов деятельности")

    for i, org_name in enumerate(organizations):
        building = building_objs[i % len(building_objs)]

        org = Organization(name=org_name, building=building)
        db.add(org)
        db.flush()

        for j in range(1 + (i % 3)):  # от 1 до 3 телефонов
            phone_str = phones[(i + j) % len(phones)]
            phone = Phone(phone=phone_str, organization=org)
            db.add(phone)

        for k in range(1 + (i % 2)):
            act_name = list(activity_dict.keys())[(i + k) % len(activity_dict)]
            org.activities.append(activity_dict[act_name])

    db.commit()
    print(f"Создано {len(organizations)} организаций с телефонами и видами деятельности")
    print("Заполнение базы тестовыми данными завершено!")


def run_seed(clear: bool = False, only_if_empty: bool = False):
    db = SessionLocal()
    try:
        seed_database(db, clear=clear, only_if_empty=only_if_empty)
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clear", action="store_true")
    parser.add_argument("--only-if-empty", action="store_true")

    args = parser.parse_args()

    run_seed(clear=args.clear, only_if_empty=args.only_if_empty)
