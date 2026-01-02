"""Base model classes for Steam API responses."""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class SteamModel(BaseModel):
    """Base class for all Steam API response models."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        populate_by_name=True,
    )


class SteamResponse(SteamModel):
    """Base response wrapper for Steam API responses."""

    success: bool = True
    message: Optional[str] = None


class PaginatedResponse(SteamModel):
    """Base for paginated API responses."""

    total: Optional[int] = None
    has_more: bool = False
    next_cursor: Optional[str] = None


class ErrorResponse(SteamModel):
    """Steam API error response model."""

    success: bool = False
    error: Optional[str] = None
    error_code: Optional[int] = None
    error_msg: Optional[str] = None
