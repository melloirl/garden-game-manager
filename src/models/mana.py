from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class ManaNatureCompositionLink(SQLModel, table=True):
    """
    Pivot/link table representing which ManaNatures
    are "components" of a given "composite" ManaNature.
    Example:
      If Lightning is composed of Fire & Wind,
      you'll have two rows here:
       (composite_mana_id=Lightning, component_mana_id=Fire)
       (composite_mana_id=Lightning, component_mana_id=Wind)
    """
    composite_mana_id: Optional[int] = Field(
        foreign_key="mananature.id", primary_key=True
    )
    component_mana_id: Optional[int] = Field(
        foreign_key="mananature.id", primary_key=True
    )

class ManaNature(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    color: str  # Hex code or some representation

    # -- Relationship Fields --

    # 1) "components": the Manas that form *this* ManaNature
    components: List["ManaNature"] = Relationship(
        link_model=ManaNatureCompositionLink,
        sa_relationship_kwargs={
            "primaryjoin": "ManaNature.id==ManaNatureCompositionLink.composite_mana_id",
            "secondaryjoin": "ManaNature.id==ManaNatureCompositionLink.component_mana_id",
        },
        back_populates="composed_in",
    )

    # 2) "composed_in": the Manas that include *this* ManaNature as a component
    composed_in: List["ManaNature"] = Relationship(
        link_model=ManaNatureCompositionLink,
        sa_relationship_kwargs={
            "primaryjoin": "ManaNature.id==ManaNatureCompositionLink.component_mana_id",
            "secondaryjoin": "ManaNature.id==ManaNatureCompositionLink.composite_mana_id",
        },
        back_populates="components",
    )
