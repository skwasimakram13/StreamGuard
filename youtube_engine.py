import os
import json
import logging
import asyncio
from typing import Optional, Callable
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

import httplib2
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

from config_manager import ConfigManager

# Scopes needed for YouTube Live Stream moderation
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

config = ConfigManager()

# Setup logging
log_file = os.path.join(config.appdata_dir, "system.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("YouTubeEngine")

class YouTubeEngine:
    def __init__(self):
        self.youtube = None
        self.is_connected = False
        self.quota_exceeded = False
        self.live_chat_id = None
        self.on_status_change: Optional[Callable[[bool, str], None]] = None
        
        # Load existing session if possible
        self._initialize_client()

    def _update_status(self, connected: bool, message: str = ""):
        self.is_connected = connected
        if self.on_status_change:
            self.on_status_change(connected, message)

    def _initialize_client(self):
        """Attempts to initialize the YouTube client from stored credentials."""
        token_json = config.load_token()
        client_secret_json = config.load_client_secret()
        
        if not client_secret_json:
            logger.warning("No client secret found. User needs to provide one.")
            self._update_status(False, "No client secret.")
            return

        creds = None
        if token_json:
            try:
                creds_data = json.loads(token_json)
                creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
            except Exception as e:
                logger.error(f"Error loading token from config: {e}")

        # If there are no (valid) credentials available, we can't initialize fully without user interaction
        if creds and creds.valid:
            self._build_service(creds)
        elif creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                config.save_token(creds.to_json())
                self._build_service(creds)
            except RefreshError as e:
                logger.error(f"Token refresh failed: {e}")
                self._update_status(False, "Token expired. Needs re-auth.")
        else:
            self._update_status(False, "Authentication required.")

    def _build_service(self, creds):
        try:
            self.youtube = build('youtube', 'v3', credentials=creds)
            self._update_status(True, "Connected")
            logger.info("YouTube client successfully built.")
        except Exception as e:
            logger.error(f"Failed to build YouTube client: {e}")
            self._update_status(False, f"Connection error: {e}")

    def authenticate_new_user(self, client_secret_path: str) -> bool:
        """Starts the OAuth flow to get new credentials."""
        try:
            with open(client_secret_path, 'r', encoding='utf-8') as f:
                client_secret_data = f.read()
            
            # Save it securely
            config.save_client_secret(client_secret_data)
            
            flow = InstalledAppFlow.from_client_config(
                json.loads(client_secret_data), SCOPES
            )
            
            # Run local server to catch the redirect
            creds = flow.run_local_server(port=0)
            
            # Save the new token
            config.save_token(creds.to_json())
            
            self._build_service(creds)
            return True
        except Exception as e:
            logger.error(f"Authentication flow failed: {e}")
            self._update_status(False, f"Auth failed: {e}")
            return False

    def logout(self):
        """Clears credentials and disconnects."""
        config.delete_credentials()
        self.youtube = None
        self._update_status(False, "Logged out.")

    # --- Resilient API Calls ---

    @retry(
        retry=retry_if_exception_type((HttpError, httplib2.ServerNotFoundError)),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(5)
    )
    def _execute_api_request(self, request):
        """Executes an API request with exponential backoff for transient errors."""
        try:
            return request.execute()
        except HttpError as e:
            if e.resp.status in [403, 500, 502, 503, 504]:
                logger.warning(f"API Error {e.resp.status}, retrying...")
                if e.resp.status == 403 and "quotaExceeded" in str(e):
                    self.quota_exceeded = True
                    self._update_status(False, "API Quota Exceeded")
                    raise e # Don't retry if it's a quota issue
                raise e # Retry other 5xx/403
            else:
                logger.error(f"Non-retriable API Error: {e}")
                raise e
        except Exception as e:
            logger.error(f"Network error: {e}")
            raise e

    def get_live_chat_id(self) -> Optional[str]:
        """Fetches the live chat ID for the user's active broadcast."""
        if not self.youtube:
            return None
        
        try:
            request = self.youtube.liveBroadcasts().list(
                part="snippet",
                broadcastStatus="active",
                broadcastType="all"
            )
            response = self._execute_api_request(request)
            
            items = response.get("items", [])
            if items:
                self.live_chat_id = items[0]["snippet"]["liveChatId"]
                return self.live_chat_id
            return None
        except Exception as e:
            logger.error(f"Error getting live chat ID: {e}")
            return None

    def get_chat_messages(self, page_token: str = None) -> tuple[list, str]:
        """Fetches recent chat messages. Returns (messages, next_page_token)."""
        if not self.youtube or not self.live_chat_id:
            return [], ""

        try:
            request = self.youtube.liveChatMessages().list(
                liveChatId=self.live_chat_id,
                part="snippet,authorDetails",
                pageToken=page_token
            )
            response = self._execute_api_request(request)
            return response.get("items", []), response.get("nextPageToken", "")
        except Exception as e:
            logger.error(f"Error fetching chat messages: {e}")
            return [], ""

    def delete_message(self, message_id: str) -> bool:
        """Deletes a specific chat message."""
        if not self.youtube:
            return False
            
        try:
            request = self.youtube.liveChatMessages().delete(
                id=message_id
            )
            self._execute_api_request(request)
            logger.info(f"Deleted message: {message_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting message {message_id}: {e}")
            return False

    def send_message(self, message_text: str) -> bool:
        """Sends a message to the active live chat."""
        if not self.youtube or not self.live_chat_id:
            return False
            
        try:
            request = self.youtube.liveChatMessages().insert(
                part="snippet",
                body={
                    "snippet": {
                        "liveChatId": self.live_chat_id,
                        "type": "textMessageEvent",
                        "textMessageDetails": {
                            "messageText": message_text
                        }
                    }
                }
            )
            self._execute_api_request(request)
            logger.info(f"Sent message: {message_text}")
            return True
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    async def heartbeat_loop(self):
        """Background task to check connectivity and quota status."""
        while True:
            if self.youtube:
                try:
                    # Simple call to check if quota is fine and internet is up
                    request = self.youtube.channels().list(part="id", mine=True)
                    # We don't use the retry wrapper here to fail fast on the heartbeat
                    request.execute()
                    self.quota_exceeded = False
                    if not self.is_connected:
                        self._update_status(True, "Connected")
                except HttpError as e:
                    if e.resp.status == 403 and "quotaExceeded" in str(e):
                        self.quota_exceeded = True
                        self._update_status(False, "API Quota Exceeded")
                    elif e.resp.status == 401:
                        self._update_status(False, "Auth Error. Please login again.")
                    else:
                        # Might be a transient 5xx error, we don't necessarily want to mark disconnected immediately
                        logger.warning(f"Heartbeat API error: {e.resp.status}")
                except Exception as e:
                    logger.warning(f"Heartbeat network error: {e}")
                    self._update_status(False, "Network Disconnected")
            
            await asyncio.sleep(60)
