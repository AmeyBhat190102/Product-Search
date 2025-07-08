from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore
from pydantic import SecretStr  # type: ignore


class Settings(BaseSettings):

    # Embedding Model Related Keys
    SENTENCE_TRANSFORMERS_EMBEDDING_MODEL_NAME: str

    # OpenAI Related Keys
    OPENAI_API_KEY: str

    # Langchain Related Keys
    LANGCHAIN_MODEL: str
    LANGCHAIN_TEMP: int
    LANGCHAIN_MAX_TOKENS: int

    # SERP Related Keys
    SERP_API_KEY: SecretStr
    SERP_API_ENDPOINT: str

    # API Related Config
    API_TIMEOUT: int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
