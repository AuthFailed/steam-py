import asyncio

from steamy_py import Steam


async def main():
    """The example shows obtaining a family group of user,
    authorized by access_token of that user."""
    async with Steam(api_key="YOUR_API_KEY", access_token="YOUR_ACCESS_TOKEN") as steam:
        family = await steam.family.get_family_group_for_user()

        shared_library_apps = await steam.family.get_shared_library_apps(
            family_group_id=family.response.family_groupid,
            steamid="YOUR_STEAMID",
        )

        users = []
        for app in shared_library_apps.response.apps:
            for steamid in app.owner_steamids:
                if steamid not in users:
                    users.append(steamid)
            print(f"Game: {app.name}. Owners: {app.owner_steamids}")

        print(f"Family group games: {len(shared_library_apps.response.apps)}")
        print(f"Number of family group members: {len(users)}")

        family_users = await steam.player.get_player_summaries(steam_ids=users)
        for index, user in enumerate(family_users):
            print(f"{index}. {user.steamid} - {user.personaname}")


if __name__ == "__main__":
    asyncio.run(main())
