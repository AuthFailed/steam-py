from pydantic import BaseModel, Field


class MembershipHistoryEntry(BaseModel):
    family_groupid: str = Field(..., description="Steam family group id")
    rtime_joined: int = Field(..., description="Time of joining this family group")
    rtime_left: int = Field(..., description="Time of leaving this family group")
    role: int = Field(..., description="Role of user in this family group")
    participated: bool = Field(..., description="")


class FamilyGroupStatus(BaseModel):
    family_groupid: str = Field(..., description="Steam family group id")
    is_not_member_of_any_group: bool = Field(
        ..., description="Is current user member of any group?"
    )
    latest_time_joined: int = Field(..., description="Time of joining this family grou")
    latest_joined_family_groupid: str = Field(
        ..., description="Latest joined family group id of user"
    )
    role: int = Field(..., description="Role of user in current family group")
    cooldown_seconds_remaining: int = Field(
        ..., description="Cooldown until next available family group change"
    )
    can_undelete_last_joined_family: bool = Field(..., description="")
    membership_history: list[MembershipHistoryEntry]


class FamilyGroupStatusResponse(BaseModel):
    response: FamilyGroupStatus


class Entry(BaseModel):
    steamid: str
    appid: int
    first_played: int
    latest_played: int
    seconds_played: int


class ResponseData(BaseModel):
    entries: list[Entry]


class SteamResponse(BaseModel):
    response: ResponseData


class SharedLibraryApp(BaseModel):
    appid: int = Field(..., description="Steam app ID")
    owner_steamids: list[str] = Field(
        ..., description="Steam IDs of users who own this app"
    )
    name: str = Field(..., description="App name")
    capsule_filename: str = Field(
        ..., description="Filename for the app's capsule image"
    )
    img_icon_hash: str = Field(..., description="Hash for the app's icon image")
    exclude_reason: int = Field(
        ..., description="Reason for exclusion from family sharing (0 if not excluded)"
    )
    rt_time_acquired: int = Field(
        ..., description="Unix timestamp when app was acquired"
    )
    rt_last_played: int = Field(..., description="Unix timestamp of last play time")
    rt_playtime: int = Field(..., description="Total playtime in seconds")
    app_type: int = Field(..., description="Type of app")
    content_descriptors: list[int] = Field(
        default_factory=list, description="Content descriptor IDs"
    )


class SharedLibraryAppsData(BaseModel):
    apps: list[SharedLibraryApp]


class SharedLibraryAppsResponse(BaseModel):
    response: SharedLibraryAppsData
