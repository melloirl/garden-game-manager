# seeder.py

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import json
from sqlmodel import Session
from typing import Dict, Any
import click

from models.race import Race
from models.region import Region
from models.mana import ManaNature
from models.character import Character

from config.database import init_db, engine


class Seeder:
    def __init__(self, session: Session):
        self.session = session
        self.data_path = Path(__file__).parent / "data"

    def load_json(self, file_name: str) -> Dict[str, Any]:
        with open(self.data_path / file_name, "r") as file:
            return json.load(file)

    def seed_races(self):
        races_data = self.load_json("races.json")
        for race_data in races_data:
            race = Race(**race_data)
            self.session.add(race)
        self.session.commit()

    def seed_regions(self):
        regions_data = self.load_json("regions.json")
        for region_data in regions_data:
            region = Region(**region_data)
            self.session.add(region)
        self.session.commit()

    def seed_characters(self):
        characters_data = self.load_json("characters.json")
        for character_data in characters_data:
            character = Character(**character_data)
            self.session.add(character)
        self.session.commit()

    def seed_mana_natures(self):
        """
        Example of seeding ManaNature (some pure, some composite) from JSON.
        """
        mana_data = self.load_json("mana_natures.json")

        # 1. Create all mana natures and store them by name
        name_to_mana = {}
        for data in mana_data:
            # No 'components' in constructor, because it's handled separately
            mana = ManaNature(
                name=data["name"], description=data["description"], color=data["color"]
            )
            self.session.add(mana)
            name_to_mana[data["name"]] = mana

        # Commit so that 'mana' objects get an ID
        self.session.commit()

        # 2. Second pass: link composites to their components
        for data in mana_data:
            mana = name_to_mana[data["name"]]
            # If it has components, link them
            component_names = data.get("components", [])
            for comp_name in component_names:
                component_mana = name_to_mana[comp_name]
                mana.components.append(component_mana)

        # Commit the links
        self.session.commit()


@click.group()
def cli():
    """Database seeding commands"""
    pass


@cli.command()
def seed_all():
    """Seed all data"""
    init_db()  # Initialize database tables
    with Session(engine) as session:
        seeder = Seeder(session)
        seeder.seed_races()
        seeder.seed_regions()
        seeder.seed_mana_natures()  # seed ManaNature data
        click.echo("✅ All data seeded successfully!")


@cli.command()
def seed_races():
    """Seed only races data"""
    init_db()
    with Session(engine) as session:
        seeder = Seeder(session)
        seeder.seed_races()
        click.echo("✅ Races seeded successfully!")


@cli.command()
def seed_regions():
    """Seed only regions data"""
    init_db()
    with Session(engine) as session:
        seeder = Seeder(session)
        seeder.seed_regions()
        click.echo("✅ Regions seeded successfully!")


@cli.command()
def seed_manas():
    """Seed only ManaNature data"""
    init_db()
    with Session(engine) as session:
        seeder = Seeder(session)
        seeder.seed_mana_natures()
        click.echo("✅ Mana natures seeded successfully!")


@cli.command()
def seed_characters():
    """Seed only characters data"""
    init_db()
    with Session(engine) as session:
        seeder = Seeder(session)
        seeder.seed_characters()
        click.echo("✅ Characters seeded successfully!")


if __name__ == "__main__":
    cli()
