"""Player/User related data models for Steam API."""

from datetime import datetime
from enum import IntEnum
from typing import List, Optional
from pydantic import Field

from .base import SteamModel, SteamResponse


class PersonaState(IntEnum):
    """Steam persona state enumeration."""

    OFFLINE = 0
    ONLINE = 1
    BUSY = 2
    AWAY = 3
    SNOOZE = 4
    LOOKING_TO_TRADE = 5
    LOOKING_TO_PLAY = 6


class CommunityVisibilityState(IntEnum):
    """Steam community visibility state."""

    PRIVATE = 1
    FRIENDS_ONLY = 2
    PUBLIC = 3


class PlayerSummary(SteamModel):
    """Steam player summary information."""

    steamid: str = Field(description="Steam ID of the player")
    personaname: str = Field(description="Player's display name")
    profileurl: str = Field(description="URL to player's Steam profile")
    avatar: str = Field(description="32x32 pixel avatar URL")
    avatarmedium: str = Field(description="64x64 pixel avatar URL")
    avatarfull: str = Field(description="184x184 pixel avatar URL")

    personastate: PersonaState = Field(description="Current online status")
    communityvisibilitystate: CommunityVisibilityState = Field(
        description="Profile visibility"
    )
    profilestate: Optional[int] = Field(default=None, description="Profile setup state")

    lastlogoff: Optional[int] = Field(
        default=None, description="Last logoff time (Unix timestamp)"
    )
    commentpermission: Optional[int] = Field(
        default=None, description="Comment permission setting"
    )

    realname: Optional[str] = Field(
        default=None, description="Player's real name (if public)"
    )
    primaryclanid: Optional[str] = Field(
        default=None, description="Primary clan/group ID"
    )
    timecreated: Optional[int] = Field(
        default=None, description="Account creation time (Unix timestamp)"
    )

    gameid: Optional[str] = Field(default=None, description="Currently playing game ID")
    gameserverip: Optional[str] = Field(
        default=None, description="Game server IP if in-game"
    )
    gameextrainfo: Optional[str] = Field(
        default=None, description="Rich presence game info"
    )

    cityid: Optional[int] = Field(default=None, description="City ID")
    loccountrycode: Optional[str] = Field(default=None, description="Country code")
    locstatecode: Optional[str] = Field(default=None, description="State code")
    loccityid: Optional[int] = Field(default=None, description="City ID")

    @property
    def is_online(self) -> bool:
        """Check if player is currently online."""
        return self.personastate != PersonaState.OFFLINE

    @property
    def is_in_game(self) -> bool:
        """Check if player is currently in a game."""
        return self.gameid is not None

    @property
    def is_public(self) -> bool:
        """Check if profile is public."""
        return self.communityvisibilitystate == CommunityVisibilityState.PUBLIC


class Friend(SteamModel):
    """Steam friend information."""

    steamid: str = Field(description="Steam ID of the friend")
    relationship: str = Field(description="Relationship type (usually 'friend')")
    friend_since: Optional[int] = Field(
        default=None, description="Unix timestamp when friendship started"
    )

    @property
    def friend_since_datetime(self) -> Optional[datetime]:
        """Get friendship start date as datetime object."""
        return datetime.fromtimestamp(self.friend_since) if self.friend_since else None


class PlayerBan(SteamModel):
    """Steam player ban information."""

    steamid: str = Field(description="Steam ID of the player")
    community_banned: bool = Field(description="Community ban status")
    vac_banned: bool = Field(description="VAC ban status")
    number_of_vac_bans: int = Field(description="Number of VAC bans")
    days_since_last_ban: int = Field(description="Days since last ban")
    number_of_game_bans: int = Field(description="Number of game bans")
    economy_ban: str = Field(description="Economy ban status")

    @property
    def is_banned(self) -> bool:
        """Check if player has any active bans."""
        return self.community_banned or self.vac_banned or self.number_of_game_bans > 0

    @property
    def has_economy_ban(self) -> bool:
        """Check if player has economy restrictions."""
        return self.economy_ban != "none"


class VanityURLResolution(SteamModel):
    """Vanity URL resolution result."""

    steamid: Optional[str] = Field(default=None, description="Resolved Steam ID")
    success: int = Field(description="Success code (1 = success)")

    @property
    def is_success(self) -> bool:
        """Check if resolution was successful."""
        return self.success == 1


# Response wrapper models
class PlayerSummariesResponse(SteamResponse):
    """Response wrapper for GetPlayerSummaries."""

    players: List[PlayerSummary] = Field(description="List of player summaries")


class FriendsListResponse(SteamResponse):
    """Response wrapper for GetFriendList."""

    friends: List[Friend] = Field(default_factory=list, description="List of friends")


class PlayerBansResponse(SteamResponse):
    """Response wrapper for GetPlayerBans."""

    players: List[PlayerBan] = Field(description="List of player ban information")


class ResolveVanityURLResponse(SteamResponse):
    """Response wrapper for ResolveVanityURL."""

    response: VanityURLResolution = Field(description="Vanity URL resolution result")
