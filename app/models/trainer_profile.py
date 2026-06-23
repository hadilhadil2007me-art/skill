import uuid
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base


class TrainerProfile(Base):
    __tablename__ = "trainer_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    skill_id = Column(
        Integer, ForeignKey("skills.id", ondelete="SET NULL"), nullable=True
    )
    city = Column(String, index=True, nullable=False)
    experience_years = Column(Integer, default=0, nullable=False)
    bio = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="trainer_profile")
    skill = relationship("Skill", back_populates="trainer_profiles")
