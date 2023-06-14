import json
from typing import Any

import redis
from flask import Flask


class Database:
    """A database backend connecting to Redis."""

    initialized = False

    def init(self, app: Flask) -> None:
        """Initializes the Redis backend.

        Args:
            app: A flask application.

        Raises:
            Exception: The backend is already initialized..
        """
        if self.initialized:
            raise Exception("Do not call init() twice")

        config = app.config["db"]

        # DB authentication
        if "password_file" in config:
            with open(config["password_file"]) as f:
                password = f.read()
        else:
            password = None

        # all keys in DB are prefixed by experiment_id
        self.key_prefix = app.config["experiment_id"] + ":"
        self.backend = redis.Redis(
            charset="utf-8", decode_responses=True, password=password, **config["redis_config"]
        )
        self.overwrite_db = config.get("overwrite_db", False)

        print("initialized with config", str(app.config["db"]))
        app.extensions["db"] = self
        self.initialized = True

    def exists(self, key: str) -> bool:
        """Checks if a key exists.

        Args:
            key: The key in string format.

        Returns:
            A bool indicating the key's existence.
        """
        key = self.key_prefix + key
        return bool(self.backend.exists(key))

    def set(self, key: str, value: Any) -> None:
        """Sets a key-value pair in the database.

        Args:
            key: The key in string format.
            value: A JSON-serializable object.

        Raises:
            Exception: The key already exists and overwriting is disabled.
        """
        key = self.key_prefix + key
        if not self.overwrite_db and self.backend.exists(key):
            raise Exception(f"{key} exists in the backend when duplicate keys are not allowed")

        self.backend.set(key, json.dumps(value))

    def get(self, key: str) -> Any:
        """Gets a key-value pair in the database.

        Args:
            key: The key in string format.

        Returns:
            An object decoded from a JSON string.

        Raises:
            Exception: The key does not exist.
        """
        key = self.key_prefix + key
        if not self.backend.exists(key):
            raise Exception(f"{key} does not exist in the backend")

        return json.loads(self.backend.get(key))

    def update(self, key: str, value: dict) -> None:
        """Updates fields of a dictionary in the database.

        Equivalent to set() when the key does not exist.

        Args:
            key: The key in string format.
            value: A dict containing new data.

        Raises:
            Exception: The key exists but its value is not a dictionary.
        """
        if not self.exists(key):
            curr = {}
        else:
            curr = self.get(key)

        if not isinstance(curr, dict):
            raise Exception(f"{key} does not point to a mapping in the db")

        self.set(key, curr | value)
