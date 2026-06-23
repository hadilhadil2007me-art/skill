import enum
import uuid
from sqlalchemy import Boolean, Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TRAINER = "trainer"
    TRAINEE = "trainee"


class AccountStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default=UserRole.TRAINEE.value, nullable=False)
    phone = Column(String, nullable=True)
    wilaya = Column(String, nullable=True)
    profession = Column(String, nullable=True)
    account_status = Column(
        String, default=AccountStatus.PENDING.value, nullable=False
    )
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_code = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    # A trainer user has one trainer profile
    trainer_profile = relationship(
        "TrainerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # Trainees submit requests
    sent_requests = relationship(
        "TrainingRequest",
        foreign_keys="[TrainingRequest.trainee_id]",
        back_populates="trainee",
        cascade="all, delete-orphan",
    )

    # Trainers receive requests
    received_requests = relationship(
        "TrainingRequest",
        foreign_keys="[TrainingRequest.trainer_id]",
        back_populates="trainer",
        cascade="all, delete-orphan",
    )

    # Trainees write reviews
    reviews_given = relationship(
        "Review",
        foreign_keys="[Review.trainee_id]",
        back_populates="trainee",
        cascade="all, delete-orphan",
    )

    # Trainers receive reviews
    reviews_received = relationship(
        "Review",
        foreign_keys="[Review.trainer_id]",
        back_populates="trainer",
        cascade="all, delete-orphan",
    )
