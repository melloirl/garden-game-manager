import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import json
from sqlmodel import Session
from typing import Dict, Any
import click

from models.race import Race
from models.region import Region

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
        click.echo("✅ All data seeded successfully!")

@cli.command()
def seed_races():
    """Seed only races data"""
    init_db()  # Initialize database tables
    with Session(engine) as session:
        seeder = Seeder(session)
        seeder.seed_races()
        click.echo("✅ Races seeded successfully!")

@cli.command()
def seed_regions():
   """Seed only regions data"""
   init_db() # Initialize database tables
   with Session(engine) as session:
      seeder = Seeder(session)
      seeder.seed_regions()
      click.echo("✅ Regions seeded successfully!")

if __name__ == "__main__":
    cli()
