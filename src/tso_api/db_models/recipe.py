from datetime import datetime, timezone
import enum
import functools
from sqlalchemy import Computed, ForeignKey, Index, String, UniqueConstraint, create_engine
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import ARRAY
from tso_api.db_models import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship

datetime_now_utc = functools.partial(datetime.now, timezone.utc)

class Recipe(Base, kw_only=True):
    __tablename__ = "recipe"

    __table_args__ = (
        UniqueConstraint('slug', 'subject'),
        Index('recipe_slug_hash', 'slug', postgresql_using='hash'),
        Index('recipe_subject_hash', 'subject', postgresql_using='hash'),
        #Index('recipe_subject_slug_hash', 'subject', 'slug', postgresql_using='hash')
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str]
    slug: Mapped[str] = mapped_column(String(50))
    title: Mapped[str]
    description: Mapped[str | None]
    servings: Mapped[str | None]
    original_url: Mapped[str| None]
    added: Mapped[datetime] = mapped_column(insert_default=datetime_now_utc())
    modified: Mapped[datetime] = mapped_column(default_factory=datetime_now_utc)
    last_made: Mapped[datetime]
    prep_time: Mapped[int]
    cook_time: Mapped[int]
    rest_time: Mapped[int]
    total_time: Mapped[int] = mapped_column(Computed("prep_time + cook_time + rest_time"))
    note: Mapped[str | None]

    ingredients: Mapped[list['Ingredient']] = relationship(back_populates='recipe', cascade='all, delete-orphan')


class MeasurementSystem(enum.Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"

class Ingredient(Base):
    __tablename__ = "ingredient"

    id: Mapped[int] = mapped_column(primary_key=True)
    idx: Mapped[int]

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"))

    raw_ingredient: Mapped[str]

    parsed_ingredient: Mapped[str | None]
    parsed_original_amount: Mapped[float | None]
    parsed_original_unit: Mapped[float | None]
    original_measurement_system: Mapped[MeasurementSystem | None]

    parsed_converted_amount: Mapped[float | None]
    parsed_converted_unit: Mapped[str]
    parsed_converted_measurement_system: Mapped[MeasurementSystem | None]
    
    recipe: Mapped['Recipe'] = relationship(back_populates="ingredients")


class StepType(enum.Enum):
    SECTION = 'section'
    STEP = 'step'

class Step(Base):
    __tablename__ = "step"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    images: Mapped[list[str]] = mapped_column(MutableList.as_mutable(ARRAY(String)))


engine = create_engine(
    'postgresql+psycopg://postgres:postgres@localhost:5432/postgres', echo=True
)

Base.metadata.create_all(engine)
