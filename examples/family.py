import asyncio

from steamy_py import Steam


async def main():
    """The example shows obtaining a family group of user,
    authorized by access_token of that user."""
    async with Steam(access_token="YOUR_ACCESS_TOKEN") as steam:
        family = await steam.family.get_family_group_for_user()
        family_groupid = family.response.family_groupid
        print(f"Family Group ID: {family_groupid}")

        shared_library_apps = await steam.family.get_shared_library_apps(
            family_groupid=family_groupid,
            include_free=False,
            include_non_games=False,
        )
        print(f"Shared apps: {len(shared_library_apps.response.apps)}")


if __name__ == "__main__":
    asyncio.run(main())
