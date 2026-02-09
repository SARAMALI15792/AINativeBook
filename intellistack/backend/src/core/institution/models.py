"""Institution management models for multi-tenancy support."""

from datetime import datetime, date
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared.database import Base

if TYPE_CHECKING:
    from src.core.auth.models import User


class InstitutionType(str, Enum):
    """Institution type classification."""

    UNIVERSITY = "university"
    COLLEGE = "college"
    BOOTCAMP = "bootcamp"
    CORPORATE = "corporate"
    SELF_PACED = "self_paced"


class Institution(Base):
    """
    Organization using IntelliStack (FR-039).

    Supports multi-tenancy with custom branding and settings.
    """

    __tablename__ = "institutions"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    institution_type: Mapped[InstitutionType] = mapped_column(
        String(50), nullable=False, default=InstitutionType.UNIVERSITY
    )
    domain: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, unique=True
    )  # Email domain for auto-assignment

    # Branding
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    primary_color: Mapped[str] = mapped_column(String(7), default="#2e8555")
    secondary_color: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)
    custom_css: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Settings
    settings: Mapped[dict] = mapped_column(
        JSONB, default=dict
    )  # Custom configuration per institution
    welcome_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Webhook for event notifications (FR-039)
    webhook_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    webhook_secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Quotas (if negotiated)
    simulation_quota_hours: Mapped[int] = mapped_column(Integer, default=25)  # Per student
    max_students: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    trial_ends_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    cohorts: Mapped[list["Cohort"]] = relationship("Cohort", back_populates="institution")
    members: Mapped[list["InstitutionMember"]] = relationship(
        "InstitutionMember", back_populates="institution"
    )


class InstitutionMember(Base):
    """
    User-Institution association with role.

    Supports users belonging to multiple institutions.
    """

    __tablename__ = "institution_members"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    institution_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("institutions.id"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # admin, instructor, student

    # Timestamps
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    left_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    institution: Mapped["Institution"] = relationship(
        "Institution", back_populates="members"
    )
    user: Mapped["User"] = relationship("User")


class Cohort(Base):
    """
    Learning cohort within an institution.

    Groups students for synchronized learning experience.
    """

    __tablename__ = "cohorts"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    institution_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("institutions.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Schedule
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Enrollment
    enrollment_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_enrollment_open: Mapped[bool] = mapped_column(Boolean, default=True)

    # Settings
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Metadata
    created_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    institution: Mapped["Institution"] = relationship("Institution", back_populates="cohorts")
    enrollments: Mapped[list["CohortEnrollment"]] = relationship(
        "CohortEnrollment", back_populates="cohort"
    )
    instructors: Mapped[list["CohortInstructor"]] = relationship(
        "CohortInstructor", back_populates="cohort"
    )
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])


class CohortEnrollment(Base):
    """
    Student enrollment in a cohort.

    Tracks enrollment status and progress.
    """

    __tablename__ = "cohort_enrollments"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    cohort_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("cohorts.id"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, index=True
    )

    # Enrollment details
    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    enrolled_by: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=True
    )  # Admin who enrolled
    dropped_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    cohort: Mapped["Cohort"] = relationship("Cohort", back_populates="enrollments")
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    enrolled_by_user: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[enrolled_by]
    )


class CohortInstructor(Base):
    """
    Instructor assignment to cohort.

    Supports multiple instructors per cohort.
    """

    __tablename__ = "cohort_instructors"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    cohort_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("cohorts.id"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, index=True
    )

    # Assignment details
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    assigned_by: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=True
    )

    # Relationships
    cohort: Mapped["Cohort"] = relationship("Cohort", back_populates="instructors")
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
