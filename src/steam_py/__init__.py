# Main Steam client
from .steam import Steam

# Core components (for advanced users)
from .client import Client
from .config import Settings

# All exceptions
from .exceptions import (
    SteamAPIError,
    AuthenticationError,
    RateLimitError,
    PlayerNotFoundError,
    GameNotFoundError,
    InvalidSteamIDError,
    InvalidAppIDError,
    PrivateProfileError,
    ServiceUnavailableError,
    ConfigurationError,
    ResponseParsingError,
    NetworkError,
)

# Most commonly used models (for type hints)
from .models import (
    PlayerSummary,
    Friend,
    PlayerBan,
    OwnedGame,
    SteamApp,
    Achievement,
    PriceInfo,
    MarketListing,
    InventoryItem,
    GlobalStat,
    UserStat,
    PlayerCount,
    NewsItem,
)

# API classes (for advanced users who want direct access)
from .repos import PlayerAPI, GameAPI, MarketAPI, StatsAPI, FamilyAPI

__version__ = "1.0.0"

__all__ = [
    # Main client
    "Steam",
    # Core components
    "Client",
    "Settings",
    # Exceptions
    "SteamAPIError",
    "AuthenticationError",
    "RateLimitError",
    "PlayerNotFoundError",
    "GameNotFoundError",
    "InvalidSteamIDError",
    "InvalidAppIDError",
    "PrivateProfileError",
    "ServiceUnavailableError",
    "ConfigurationError",
    "ResponseParsingError",
    "NetworkError",
    # Common models
    "PlayerSummary",
    "Friend",
    "PlayerBan",
    "OwnedGame",
    "SteamApp",
    "Achievement",
    "PriceInfo",
    "MarketListing",
    "InventoryItem",
    "GlobalStat",
    "UserStat",
    "PlayerCount",
    "NewsItem",
    # API classes
    "PlayerAPI",
    "GameAPI",
    "MarketAPI",
    "StatsAPI",
    "FamilyAPI",
    # Version
    "__version__",
]
