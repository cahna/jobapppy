from typing import Iterable, Literal, Mapping, Optional

from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.dataclasses import dataclass


@dataclass
class Info:
    """Personal and contact info"""

    name: str
    title: str
    phone: str
    email: str
    address1: str
    address2: Optional[str] = Field(None)


class BaseSectionContent(BaseModel):
    """All section contents type must subclass this type to work"""

    pass


class DatedListItems(BaseSectionContent):
    """Bullet points with date as annotation"""

    description1: str
    title: str
    start_date: str
    end_date: str
    items: Iterable[str]
    description2: Optional[str] = Field(None)


class DescribeItem(BaseSectionContent):
    """Single item with description, text, optional secondary text, and annotation"""

    description: str
    annotation: str
    text1: str
    text2: Optional[str] = Field(None)


class HighlightItemList(BaseSectionContent):
    """Categorized item list. Ex: Skills & Expertise section"""

    description: str
    items: Iterable[str]


class AnnotatedItem(BaseSectionContent):
    """Categorized item with annotation. Ex: Open Source Contributions"""

    description: str
    text: str
    annotation: str


# TODO: how to make this typing work(?)
# SectionType: Mapping[str, BaseSectionContent] = {c.__name__: c for c in BaseSectionContent.__subclasses__()}
# SectionTypeName = Literal[tuple(SectionType.keys())]
# SectionTypeClass = Union[tuple(SectionType.values())]

SectionTypeName = Literal["DatedListItems", "DescribeItem", "HighlightItemList", "AnnotatedItem"]
# SectionTypeClass = type[BaseSectionContent]


class SectionDefinition(BaseModel):
    name: str
    type_: SectionTypeName = Field(alias="type")
    contents: Iterable[BaseSectionContent]

    @validator("contents", pre=True)
    def handle_parse_contents(cls, value, values):
        if isinstance(value, list):
            SECTION_TYPES = {c.__name__: c for c in BaseSectionContent.__subclasses__()}
            contents_type = values["type_"]
            Klass = SECTION_TYPES[contents_type]
            return [Klass(**data) for data in value]
        raise ValidationError(f"Invalid value for section contents: {contents_type}")


@dataclass
class Resume:
    """Resume definition"""

    info: Info
    sections: Iterable[SectionDefinition]


@dataclass
class JobAppYaml:
    """Schema for jobapp yaml input"""

    resume: Resume


@dataclass
class TemplateConfig:
    """JSON file defining strings for global search and replace"""

    replace_strings: Optional[Mapping[str, str]] = Field(None)
