import logging

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

load_dotenv()


class Settings(BaseSettings):
    env: str = "local"

    agent_id: str = "agent"
    agent_name: str = "Agent"

    litellm_base_url: str = Field(default=...)
    litellm_key: str = Field(default=...)
    llm_model: str = Field(default=...)
    braintrust_api_key: str = Field(default=...)

    log_level: str = "INFO"
    debug_level: int = 2

    model_config = SettingsConfigDict(
        frozen=True,
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )
