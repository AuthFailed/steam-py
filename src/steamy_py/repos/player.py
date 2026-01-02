"""Player/User API endpoints for Steam API."""

import logging
from typing import List, Optional, Union

from ..exceptions import (
    InvalidSteamIDError,
    PrivateProfileError,
    SteamAPIError,
)
from ..models.player import (
    PlayerSummary,
    Friend,
    PlayerBan,
    PlayerSummariesResponse,
    FriendsListResponse,
    PlayerBansResponse,
    ResolveVanityURLResponse,
)
from .base import BaseAPI


logger = logging.getLogger(__name__)


class PlayerAPI(BaseAPI):
    """Steam Player/User API endpoints."""

    async def get_player_summaries(
        self, steam_ids: Union[str, List[str]]
    ) -> List[PlayerSummary]:
        """Get player summary information for one or more Steam IDs.

        Args:
            steam_ids: Single Steam ID or list of Steam IDs (max 100)

        Returns:
            List of player summaries

        Raises:
            InvalidSteamIDError: If Steam ID format is invalid
            SteamAPIError: On API errors
        """
        if isinstance(steam_ids, str):
            steam_ids = [steam_ids]

        if len(steam_ids) > 100:
            raise ValueError("Maximum 100 Steam IDs allowed per request")

        # Validate Steam IDs
        for steam_id in steam_ids:
            self._validate_steam_id(steam_id)

        steamids_param = ",".join(steam_ids)

        try:
            response_data = await self._request(
                interface="ISteamUser",
                method="GetPlayerSummaries",
                version="v2",
                params={"steamids": steamids_param},
            )

            # Parse the nested response structure
            if "response" not in response_data:
                raise SteamAPIError("Invalid response structure from Steam API")

            response_obj = PlayerSummariesResponse(**response_data["response"])
            return response_obj.players

        except Exception as e:
            logger.error(f"Error getting player summaries: {e}")
            if isinstance(e, SteamAPIError):
                raise
            raise SteamAPIError(f"Failed to get player summaries: {e}")

    async def get_friends_list(
        self, steam_id: str, relationship: str = "friend"
    ) -> List[Friend]:
        """Get friends list for a Steam user.

        Args:
            steam_id: Steam ID of the user
            relationship: Relationship type (default: "friend")

        Returns:
            List of friends

        Raises:
            InvalidSteamIDError: If Steam ID format is invalid
            PrivateProfileError: If profile is private
            PlayerNotFoundError: If player not found
            SteamAPIError: On API errors
        """
        self._validate_steam_id(steam_id)

        try:
            response_data = await self._request(
                interface="ISteamUser",
                method="GetFriendList",
                version="v1",
                params={"steamid": steam_id, "relationship": relationship},
            )

            if "friendslist" not in response_data:
                # This usually means the profile is private
                raise PrivateProfileError(steam_id)

            response_obj = FriendsListResponse(
                friends=response_data["friendslist"].get("friends", [])
            )
            return response_obj.friends

        except PrivateProfileError:
            raise
        except Exception as e:
            logger.error(f"Error getting friends list for {steam_id}: {e}")
            if isinstance(e, SteamAPIError):
                raise
            raise SteamAPIError(f"Failed to get friends list: {e}")

    async def get_player_bans(
        self, steam_ids: Union[str, List[str]]
    ) -> List[PlayerBan]:
        """Get ban information for one or more Steam users.

        Args:
            steam_ids: Single Steam ID or list of Steam IDs (max 100)

        Returns:
            List of player ban information

        Raises:
            InvalidSteamIDError: If Steam ID format is invalid
            SteamAPIError: On API errors
        """
        if isinstance(steam_ids, str):
            steam_ids = [steam_ids]

        if len(steam_ids) > 100:
            raise ValueError("Maximum 100 Steam IDs allowed per request")

        # Validate Steam IDs
        for steam_id in steam_ids:
            self._validate_steam_id(steam_id)

        steamids_param = ",".join(steam_ids)

        try:
            response_data = await self._request(
                interface="ISteamUser",
                method="GetPlayerBans",
                version="v1",
                params={"steamids": steamids_param},
            )

            if "players" not in response_data:
                raise SteamAPIError("Invalid response structure from Steam API")

            response_obj = PlayerBansResponse(players=response_data["players"])
            return response_obj.players

        except Exception as e:
            logger.error(f"Error getting player bans: {e}")
            if isinstance(e, SteamAPIError):
                raise
            raise SteamAPIError(f"Failed to get player bans: {e}")

    async def resolve_vanity_url(
        self, vanity_url: str, url_type: int = 1
    ) -> Optional[str]:
        """Resolve a Steam vanity URL to a Steam ID.

        Args:
            vanity_url: The vanity URL to resolve (just the custom part)
            url_type: URL type (1=individual, 2=group, 3=gameserver)

        Returns:
            Steam ID if successful, None if not found

        Raises:
            SteamAPIError: On API errors
        """
        # Clean the vanity URL (remove full URL parts if provided)
        if "/" in vanity_url:
            vanity_url = vanity_url.split("/")[-1]

        try:
            response_data = await self._request(
                interface="ISteamUser",
                method="ResolveVanityURL",
                version="v1",
                params={"vanityurl": vanity_url, "url_type": url_type},
            )

            if "response" not in response_data:
                raise SteamAPIError("Invalid response structure from Steam API")

            response_obj = ResolveVanityURLResponse(response=response_data["response"])

            if response_obj.response.is_success:
                return response_obj.response.steamid
            else:
                return None

        except Exception as e:
            logger.error(f"Error resolving vanity URL '{vanity_url}': {e}")
            if isinstance(e, SteamAPIError):
                raise
            raise SteamAPIError(f"Failed to resolve vanity URL: {e}")

    def _validate_steam_id(self, steam_id: str) -> None:
        """Validate Steam ID format.

        Args:
            steam_id: Steam ID to validate

        Raises:
            InvalidSteamIDError: If Steam ID format is invalid
        """
        if not steam_id:
            raise InvalidSteamIDError(steam_id, "Steam ID cannot be empty")

        # Steam ID should be a 17-digit number starting with 7656119
        if not steam_id.isdigit():
            raise InvalidSteamIDError(steam_id, "Steam ID must be numeric")

        if len(steam_id) != 17:
            raise InvalidSteamIDError(steam_id, "Steam ID must be 17 digits long")

        if not steam_id.startswith("7656119"):
            raise InvalidSteamIDError(steam_id, "Invalid Steam ID format")

    async def get_player_summary(self, steam_id: str) -> Optional[PlayerSummary]:
        """Get single player summary (convenience method).

        Args:
            steam_id: Steam ID of the player

        Returns:
            Player summary or None if not found

        Raises:
            InvalidSteamIDError: If Steam ID format is invalid
            SteamAPIError: On API errors
        """
        summaries = await self.get_player_summaries(steam_id)
        return summaries[0] if summaries else None
