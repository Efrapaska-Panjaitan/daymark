from sqlalchemy import CheckConstraint , Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

class Task(Base):
    __tablename__ = "tasks"
    
    __table_args__ = (
        CheckConstraint(
            "status IN ('Todo', 'In Progress', 'Done')",
            name="ck_tasks_status_allowed",
        ),
    )
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        autoincrement = True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable = False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable = False,
        server_default = "",
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable = False,
        server_default = "Todo",
    )