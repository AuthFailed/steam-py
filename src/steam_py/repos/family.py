"""Steam Family API endpoints."""

import logging
from typing import Optional, Dict, Any

from ..exceptions import SteamAPIError, AuthenticationError
from .base import BaseAPI


logger = logging.getLogger(__name__)


class FamilyAPI(BaseAPI):
    """Steam Family API endpoints.

    Note: These endpoints require access_token authentication, not api_key.
    """

    async def get_family_group(
        self,
        family_group_id: Optional[int] = None,
        send_running_apps: bool = False,
    ) -> Dict[str, Any]:
        """Get family group information.

        Args:
            family_group_id: Specific family group ID to fetch
            send_running_apps: Whether to include running app information

        Returns:
            Family group data

        Raises:
            AuthenticationError: If access token is not provided
            SteamAPIError: On API errors
        """
        params = {}
        if family_group_id is not None:
            params["family_group_id"] = str(family_group_id)
        if send_running_apps:
            params["send_running_apps"] = "1"

        try:
            response_data = await self._request(
                interface="IFamilyGroupsService",
                method="GetFamilyGroup",
                version="v1",
                params=params,
                auth_type="access_token",
            )
            return response_data
        except ValueError as e:
            if "Access token is required" in str(e):
                raise AuthenticationError(
                    "Access token is required for Family API endpoints"
                )
            raise
        except Exception as e:
            logger.error(f"Error getting family group: {e}")
            raise SteamAPIError(f"Failed to get family group: {e}")

    async def get_family_group_for_user(
        self, steamid: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get the family group for the authenticated user or specified user.

        Args:
            steamid: Steam ID of user (for support/admin accounts only).
                    If omitted, gets family group for the authenticated user.

        Returns:
            Family group data for the user

        Raises:
            AuthenticationError: If access token is not provided
            SteamAPIError: On API errors
        """
        params = {}
        if steamid is not None:
            params["steamid"] = str(steamid)

        try:
            response_data = await self._request(
                interface="IFamilyGroupsService",
                method="GetFamilyGroupForUser",
                version="v1",
                params=params,
                auth_type="access_token",
            )
            return response_data
        except ValueError as e:
            if "Access token is required" in str(e):
                raise AuthenticationError(
                    "Access token is required for Family API endpoints"
                )
            raise
        except Exception as e:
            logger.error(f"Error getting family group for user: {e}")
            raise SteamAPIError(f"Failed to get family group for user: {e}")

    async def get_playtime_summary(
        self, family_groupid: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get playtime summary for family group.

        Args:
            family_groupid: Family group ID (optional)

        Returns:
            Playtime summary data

        Raises:
            AuthenticationError: If access token is not provided
            SteamAPIError: On API errors
        """
        params = {}
        if family_groupid is not None:
            params["family_groupid"] = str(family_groupid)

        try:
            response_data = await self._request(
                interface="IFamilyGroupsService",
                method="GetPlaytimeSummary",
                version="v1",
                params=params,
                auth_type="access_token",
                http_method="POST",
            )
            return response_data
        except ValueError as e:
            if "Access token is required" in str(e):
                raise AuthenticationError(
                    "Access token is required for Family API endpoints"
                )
            raise
        except Exception as e:
            logger.error(f"Error getting playtime summary: {e}")
            raise SteamAPIError(f"Failed to get playtime summary: {e}")

    # POST request examples
    async def create_family_invite(
        self, steamid: str, family_groupid: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create a family group invitation (POST request example).

        Args:
            steamid: Steam ID of user to invite
            family_groupid: Family group ID (optional)

        Returns:
            Invitation response data

        Raises:
            AuthenticationError: If access token is not provided
            SteamAPIError: On API errors
        """
        params = {"steamid": str(steamid)}
        if family_groupid is not None:
            params["family_groupid"] = str(family_groupid)

        try:
            response_data = await self._post_request(
                interface="IFamilyGroupsService",
                method="CreateFamilyInvite",
                version="v1",
                params=params,
                auth_type="access_token",
            )
            return response_data
        except ValueError as e:
            if "Access token is required" in str(e):
                raise AuthenticationError(
                    "Access token is required for Family API endpoints"
                )
            raise
        except Exception as e:
            logger.error(f"Error creating family invite: {e}")
            raise SteamAPIError(f"Failed to create family invite: {e}")

    async def respond_to_family_invite(
        self, family_groupid: int, accept: bool = True
    ) -> Dict[str, Any]:
        """Respond to a family group invitation (POST request example).

        Args:
            family_groupid: Family group ID
            accept: Whether to accept or decline the invitation

        Returns:
            Response data

        Raises:
            AuthenticationError: If access token is not provided
            SteamAPIError: On API errors
        """
        params = {
            "family_groupid": str(family_groupid),
            "accept": "1" if accept else "0",
        }

        try:
            response_data = await self._post_request(
                interface="IFamilyGroupsService",
                method="RespondToFamilyInvite",
                version="v1",
                params=params,
                auth_type="access_token",
            )
            return response_data
        except ValueError as e:
            if "Access token is required" in str(e):
                raise AuthenticationError(
                    "Access token is required for Family API endpoints"
                )
            raise
        except Exception as e:
            logger.error(f"Error responding to family invite: {e}")
            raise SteamAPIError(f"Failed to respond to family invite: {e}")

    async def modify_family_settings(
        self, family_groupid: int, settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Modify family group settings (PUT request example).

        Args:
            family_groupid: Family group ID
            settings: Settings to update

        Returns:
            Updated settings data

        Raises:
            AuthenticationError: If access token is not provided
            SteamAPIError: On API errors
        """
        params = {"family_groupid": str(family_groupid)}
        params.update(settings)

        try:
            response_data = await self._put_request(
                interface="IFamilyGroupsService",
                method="ModifyFamilySettings",
                version="v1",
                params=params,
                auth_type="access_token",
            )
            return response_data
        except ValueError as e:
            if "Access token is required" in str(e):
                raise AuthenticationError(
                    "Access token is required for Family API endpoints"
                )
            raise
        except Exception as e:
            logger.error(f"Error modifying family settings: {e}")
            raise SteamAPIError(f"Failed to modify family settings: {e}")

    async def remove_family_member(
        self, family_groupid: int, steamid: str
    ) -> Dict[str, Any]:
        """Remove a member from family group (DELETE request example).

        Args:
            family_groupid: Family group ID
            steamid: Steam ID of member to remove

        Returns:
            Removal response data

        Raises:
            AuthenticationError: If access token is not provided
            SteamAPIError: On API errors
        """
        params = {"family_groupid": str(family_groupid), "steamid": str(steamid)}

        try:
            response_data = await self._delete_request(
                interface="IFamilyGroupsService",
                method="RemoveFamilyMember",
                version="v1",
                params=params,
                auth_type="access_token",
            )
            return response_data
        except ValueError as e:
            if "Access token is required" in str(e):
                raise AuthenticationError(
                    "Access token is required for Family API endpoints"
                )
            raise
        except Exception as e:
            logger.error(f"Error removing family member: {e}")
            raise SteamAPIError(f"Failed to remove family member: {e}")
