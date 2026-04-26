import os
import json
import threading
import logging
from cryptography.fernet import Fernet
import keyring

# Setup basic logging for the config manager (can be overridden by main logging config)
logger = logging.getLogger("ConfigManager")

class ConfigManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConfigManager, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        self.app_name = "StreamGuard"
        self.appdata_dir = os.path.join(os.environ.get('APPDATA', ''), self.app_name)
        
        # Ensure the directory exists
        if not os.path.exists(self.appdata_dir):
            os.makedirs(self.appdata_dir)
            logger.info(f"Created AppData directory at: {self.appdata_dir}")

        self.settings_file = os.path.join(self.appdata_dir, "settings.json")
        self.token_file = os.path.join(self.appdata_dir, "token.enc")
        self.client_secret_file = os.path.join(self.appdata_dir, "client_secret.enc")
        
        self.fernet = self._get_or_create_fernet()

    def _get_or_create_fernet(self) -> Fernet:
        """Retrieves or creates the encryption key from the Windows Credential Manager."""
        key = keyring.get_password(self.app_name, "encryption_key")
        if not key:
            key = Fernet.generate_key().decode('utf-8')
            keyring.set_password(self.app_name, "encryption_key", key)
            logger.info("Generated new encryption key and stored in keyring.")
        
        return Fernet(key.encode('utf-8'))

    def _encrypt_data(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode('utf-8'))

    def _decrypt_data(self, data: bytes) -> str:
        return self.fernet.decrypt(data).decode('utf-8')

    # --- Thread-safe Setting Methods ---

    def get_setting(self, key: str, default=None):
        with self._lock:
            settings = self._load_settings()
            return settings.get(key, default)

    def set_setting(self, key: str, value):
        with self._lock:
            settings = self._load_settings()
            settings[key] = value
            self._save_settings(settings)

    def _load_settings(self) -> dict:
        if not os.path.exists(self.settings_file):
            return {}
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            return {}

    def _save_settings(self, settings: dict):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving settings: {e}")

    # --- Thread-safe Encrypted Credential Methods ---

    def save_client_secret(self, secret_json: str):
        """Encrypts and saves the client secret JSON string."""
        with self._lock:
            encrypted = self._encrypt_data(secret_json)
            with open(self.client_secret_file, 'wb') as f:
                f.write(encrypted)
            logger.info("Client secret encrypted and saved.")

    def load_client_secret(self) -> str:
        """Loads and decrypts the client secret JSON string. Returns None if not found."""
        with self._lock:
            if not os.path.exists(self.client_secret_file):
                return None
            try:
                with open(self.client_secret_file, 'rb') as f:
                    encrypted = f.read()
                return self._decrypt_data(encrypted)
            except Exception as e:
                logger.error(f"Error loading client secret: {e}")
                return None

    def save_token(self, token_json: str):
        """Encrypts and saves the OAuth token JSON string."""
        with self._lock:
            encrypted = self._encrypt_data(token_json)
            with open(self.token_file, 'wb') as f:
                f.write(encrypted)
            logger.info("OAuth token encrypted and saved.")

    def load_token(self) -> str:
        """Loads and decrypts the OAuth token JSON string. Returns None if not found."""
        with self._lock:
            if not os.path.exists(self.token_file):
                return None
            try:
                with open(self.token_file, 'rb') as f:
                    encrypted = f.read()
                return self._decrypt_data(encrypted)
            except Exception as e:
                logger.error(f"Error loading token: {e}")
                return None

    def has_credentials(self) -> bool:
        """Check if we have the client secret at least."""
        return os.path.exists(self.client_secret_file)

    def delete_credentials(self):
        """Deletes the encrypted credential files and keyring entry."""
        with self._lock:
            if os.path.exists(self.client_secret_file):
                os.remove(self.client_secret_file)
            if os.path.exists(self.token_file):
                os.remove(self.token_file)
            
            try:
                keyring.delete_password(self.app_name, "encryption_key")
            except keyring.errors.PasswordDeleteError:
                pass # It's okay if it doesn't exist
            
            logger.info("Credentials and encryption key deleted.")
