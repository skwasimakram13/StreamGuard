import flet as ft
import asyncio
import subprocess

from flet.controls.material.icons import Icons
from config_manager import ConfigManager
from youtube_engine import YouTubeEngine
from database import DatabaseManager
from sentiment import SentimentEngine
from version import __version__
import logging

logger = logging.getLogger(__name__)

config = ConfigManager()
yt_engine = YouTubeEngine()
db = DatabaseManager()
sentiment = SentimentEngine()

async def main(page: ft.Page):
    page.title = "StreamGuard"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.GREY_900
    page.padding = 20
    page.window.width = 1150
    page.window.height = 850

    # ─── App State ───────────────────────────────────────────────────────────
    banned_words: set[str] = set(config.get_setting("banned_words", []))
    auto_mod_enabled: bool = config.get_setting("auto_mod", False)
    chat_fetching_enabled: bool = config.get_setting("chat_fetching_enabled", True)
    poll_frequency: int = config.get_setting("poll_frequency", 5)
    next_page_token: str = ""

    # Bot State
    alerts_bot_enabled: bool = config.get_setting("alerts_bot_enabled", False)
    alerts_interval: int = config.get_setting("alerts_interval", 5)
    alert_messages: list[str] = config.get_setting("alert_messages", [
        "The stream is starting soon, stay tuned!",
        "We are giving away a special prize, don't miss it!",
        "Only 10 minutes left for the giveaway, get ready!"
    ])

    engagement_bot_enabled: bool = config.get_setting("engagement_bot_enabled", False)
    engagement_interval: int = config.get_setting("engagement_interval", 5)
    reminder_messages: list[str] = config.get_setting("reminder_messages", [
        "Don't forget to LIKE and SHARE the stream if you're enjoying it!",
        "SUBSCRIBE for more awesome content!",
        "We're almost at 100 likes, let's go!"
    ])

    custom_commands_enabled: bool = config.get_setting("custom_commands_enabled", False)
    custom_commands: dict[str, str] = config.get_setting("custom_commands", {
        "!discord": "Join our community here: https://discord.gg/yourlink",
        "!specs": "CPU: Ryzen 9, GPU: RTX 4090"
    })
    
    gemini_api_key: str = config.get_setting("gemini_api_key", "")
    sentiment.configure(gemini_api_key)
    vibe_batch: list[str] = []

    # ─── Toast Helper ────────────────────────────────────────────────────────
    def show_toast(message: str, is_error: bool = False):
        color = ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700
        sb = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color,
            open=True,
        )
        page.overlay.append(sb)
        page.update()

    async def save_settings():
        config.set_setting("banned_words", list(banned_words))
        config.set_setting("auto_mod", auto_mod_enabled)
        config.set_setting("chat_fetching_enabled", chat_fetching_enabled)
        config.set_setting("poll_frequency", poll_frequency)
        
        config.set_setting("alerts_bot_enabled", alerts_bot_enabled)
        config.set_setting("alerts_interval", alerts_interval)
        config.set_setting("alert_messages", alert_messages)
        
        config.set_setting("engagement_bot_enabled", engagement_bot_enabled)
        config.set_setting("engagement_interval", engagement_interval)
        config.set_setting("reminder_messages", reminder_messages)
        
        config.set_setting("custom_commands_enabled", custom_commands_enabled)
        config.set_setting("custom_commands", custom_commands)
        config.set_setting("gemini_api_key", gemini_api_key)

    # ─── Status Indicator ────────────────────────────────────────────────────
    status_dot = ft.Icon(icon=Icons.CIRCLE, color=ft.Colors.RED_400, size=18)
    status_label = ft.Text("Disconnected", size=15, weight=ft.FontWeight.BOLD,
                           color=ft.Colors.WHITE)

    def update_status_ui(connected: bool, message: str):
        status_dot.color = ft.Colors.GREEN_400 if connected else ft.Colors.RED_400
        status_label.value = message or ("Connected" if connected else "Disconnected")
        page.update()

    yt_engine.on_status_change = update_status_ui

    # ─── Native File Dialog (Windows PowerShell) ─────────────────────────────
    # ft.FilePicker is NOT used here — it is unsupported in flet build windows
    # (throws "Unknown control: FilePicker"). Instead we call PowerShell's
    # System.Windows.Forms.OpenFileDialog directly from a thread executor.

    def _open_file_dialog_sync() -> str:
        """Spawn a native Windows OpenFileDialog via PowerShell. Returns the
        selected file path, or an empty string if the user cancelled."""
        ps_script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$dlg = New-Object System.Windows.Forms.OpenFileDialog; "
            "$dlg.Title = 'Select your client_secret.json'; "
            "$dlg.Filter = 'JSON Files (*.json)|*.json|All Files (*.*)|*.*'; "
            "$dlg.FilterIndex = 1; "
            "$dlg.Multiselect = $false; "
            "if ($dlg.ShowDialog() -eq 'OK') { Write-Output $dlg.FileName }"
        )
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=120,
                creationflags=subprocess.CREATE_NO_WINDOW,  # hide the PowerShell console window
            )
            return result.stdout.strip()
        except Exception as exc:
            logger.error("File dialog subprocess failed: %s", exc)
            return ""

    async def handle_pick_secret(_):
        loop = asyncio.get_running_loop()
        file_path = await loop.run_in_executor(None, _open_file_dialog_sync)
        if not file_path:
            return  # User cancelled
        success = await loop.run_in_executor(
            None, yt_engine.authenticate_new_user, file_path
        )
        if success:
            show_toast("Successfully authenticated! 🎉")
            await show_dashboard()
        else:
            show_toast("Authentication failed. Check your client_secret.json.", is_error=True)

    # ─── Setup Wizard View ───────────────────────────────────────────────────
    setup_view = ft.Column(
        controls=[
            ft.Container(height=40),
            ft.Icon(icon=Icons.SHIELD, color=ft.Colors.BLUE_400, size=64),
            ft.Container(height=16),
            ft.Text("Welcome to StreamGuard V2", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text("Bring Your Own Key (BYOK) Architecture", size=15, color=ft.Colors.GREY_400),
            ft.Divider(height=40, color=ft.Colors.GREY_700),
            ft.Text("Step 1: Download your OAuth 2.0 Client Secret JSON from Google Cloud Console.", size=15, color=ft.Colors.GREY_300),
            ft.Text("Step 2: Select the file below to securely authenticate.", size=15, color=ft.Colors.GREY_300),
            ft.Container(height=16),
            ft.FilledButton("Select client_secret.json", icon=Icons.UPLOAD_FILE, on_click=handle_pick_secret),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ─── Dashboard – Chat Feed ───────────────────────────────────────────────
    chat_list = ft.ListView(expand=True, spacing=8, auto_scroll=True)
    highlights_list = ft.ListView(expand=True, spacing=8, auto_scroll=True)

    async def delete_msg(e):
        msg_id = e.control.data
        ok = await asyncio.get_running_loop().run_in_executor(None, yt_engine.delete_message, msg_id)
        show_toast("Message deleted." if ok else "Failed to delete.", is_error=not ok)

    def make_message_card(item: dict) -> ft.Card:
        msg_id = item["id"]
        author = item["authorDetails"]["displayName"]
        text = item["snippet"]["displayMessage"]
        msg_type = item["snippet"]["type"]
        
        is_highlight = msg_type in ["superChatEvent", "newSponsorEvent", "memberMilestoneChatEvent"]
        
        # Superchats get amber border, regular chat gets grey
        border = ft.Border.all(2, ft.Colors.AMBER_400) if is_highlight else None
        
        return ft.Card(
            content=ft.Container(
                padding=10, bgcolor=ft.Colors.GREY_800,
                border=border,
                border_radius=8,
                content=ft.Row([
                    ft.Column([
                        ft.Row([
                            ft.Icon(Icons.STAR, color=ft.Colors.AMBER_400, size=16) if is_highlight else ft.Container(),
                            ft.Text(author, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200 if not is_highlight else ft.Colors.AMBER_200),
                        ]),
                        ft.Text(text, selectable=True, color=ft.Colors.GREY_200),
                    ], expand=True),
                    ft.IconButton(icon=Icons.DELETE, icon_color=ft.Colors.RED_400, data=msg_id, on_click=delete_msg),
                ])
            )
        )

    # ─── Moderation Tab ──────────────────────────────────────────────────────
    banned_words_field = ft.TextField(
        label="Banned Words (comma separated)", multiline=True, min_lines=3,
        value=", ".join(banned_words), expand=True, color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREY_800, border_color=ft.Colors.GREY_600,
    )

    async def update_banned_list(_):
        nonlocal banned_words
        banned_words = set(w.strip() for w in banned_words_field.value.split(",") if w.strip())
        await save_settings()
        show_toast("Banned list updated.")

    def toggle_master(e):
        nonlocal chat_fetching_enabled; chat_fetching_enabled = e.control.value; asyncio.create_task(save_settings())

    def toggle_automod(e):
        nonlocal auto_mod_enabled; auto_mod_enabled = e.control.value; asyncio.create_task(save_settings())

    def change_sensitivity(e):
        nonlocal poll_frequency; poll_frequency = max(2, int(e.control.value)); asyncio.create_task(save_settings())

    moderation_view = ft.Row(
        controls=[
            ft.Column([
                ft.Text("Live Chat Feed", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Container(content=chat_list, expand=True, border=ft.Border.all(1, ft.Colors.GREY_700), border_radius=10, padding=10, bgcolor=ft.Colors.GREY_800),
            ], expand=4),
            ft.VerticalDivider(width=10, color=ft.Colors.TRANSPARENT),
            ft.Column([
                ft.Text("Highlights", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400),
                ft.Container(content=highlights_list, expand=True, border=ft.Border.all(1, ft.Colors.AMBER_700), border_radius=10, padding=10, bgcolor=ft.Colors.GREY_900),
            ], expand=2),
            ft.VerticalDivider(width=10, color=ft.Colors.TRANSPARENT),
            ft.Column([
                ft.Text("Moderation Controls", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Card(content=ft.Container(padding=15, bgcolor=ft.Colors.GREY_800, content=ft.Column([
                    ft.Switch(label="Master Switch: Enable Chat API & Bots", value=chat_fetching_enabled, on_change=toggle_master, active_color=ft.Colors.GREEN_400),
                    ft.Divider(),
                    ft.Switch(label="Enable Auto-Mod", value=auto_mod_enabled, on_change=toggle_automod, active_color=ft.Colors.BLUE_400),
                    ft.Text("Polling Frequency (seconds)", color=ft.Colors.GREY_300),
                    ft.Slider(min=2, max=30, divisions=28, value=poll_frequency, label="{value}s", on_change=change_sensitivity, active_color=ft.Colors.BLUE_400),
                ]))),
                ft.Container(height=10),
                ft.Card(content=ft.Container(padding=15, bgcolor=ft.Colors.GREY_800, content=ft.Column([
                    ft.Text("Banned List Manager", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    banned_words_field,
                    ft.FilledButton("Update List", on_click=update_banned_list),
                ])), expand=True),
            ], expand=2),
        ], expand=True
    )

    # ─── Loyalty Tab ─────────────────────────────────────────────────────────
    loyalty_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    def refresh_loyalty():
        loyalty_list.controls.clear()
        viewers = db.get_top_viewers(50)
        for v in viewers:
            def toggle_vip(e, author_id=v['author_id']):
                db.toggle_vip(author_id, e.control.value)
                show_toast("VIP status updated")
            
            loyalty_list.controls.append(
                ft.Card(content=ft.ListTile(
                    leading=ft.Icon(Icons.PERSON, color=ft.Colors.BLUE_400),
                    title=ft.Text(f"{v['display_name']} ({v['message_count']} msgs)", weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"First seen: {v['first_seen'][:10]}"),
                    trailing=ft.Switch(label="VIP", value=v['is_vip'], on_change=toggle_vip, active_color=ft.Colors.AMBER_400)
                ))
            )
        if not viewers:
            loyalty_list.controls.append(ft.Text("No viewers recorded yet. Start reading chat!", color=ft.Colors.GREY_400))
        page.update()

    loyalty_view = ft.Column([
        ft.Row([
            ft.Text("Top Chatters & Regulars", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.IconButton(icon=Icons.REFRESH, on_click=lambda _: refresh_loyalty())
        ]),
        ft.Container(content=loyalty_list, expand=True, bgcolor=ft.Colors.GREY_800, padding=10, border_radius=10)
    ], expand=True)

    # ─── Bots Tab ────────────────────────────────────────────────────────────
    
    def make_bot_card(title, desc, controls):
        return ft.Card(content=ft.Container(padding=15, bgcolor=ft.Colors.GREY_800, content=ft.Column([
            ft.Text(title, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=18),
            ft.Text(desc, color=ft.Colors.GREY_400, size=12),
            ft.Divider(color=ft.Colors.GREY_700),
            *controls
        ])))

    # Alerts Bot UI
    def toggle_alerts(e):
        nonlocal alerts_bot_enabled; alerts_bot_enabled = e.control.value; asyncio.create_task(save_settings())
    def change_alerts_int(e):
        nonlocal alerts_interval; alerts_interval = max(1, int(e.control.value)); asyncio.create_task(save_settings())
    async def save_alerts(_):
        nonlocal alert_messages; alert_messages = [l.strip() for l in alerts_field.value.split('\n') if l.strip()]
        await save_settings(); show_toast("Alert messages saved.")

    alerts_field = ft.TextField(value="\n".join(alert_messages), multiline=True, min_lines=4, max_lines=4, expand=True, bgcolor=ft.Colors.GREY_900)
    alerts_card = make_bot_card("Time-based Alerts Bot", "Sends promotional or informational alerts on a timer.", [
        ft.Switch(label="Enable Alerts Bot", value=alerts_bot_enabled, on_change=toggle_alerts, active_color=ft.Colors.BLUE_400),
        ft.Text("Interval (minutes)", color=ft.Colors.GREY_300),
        ft.Slider(min=1, max=60, divisions=59, value=alerts_interval, label="{value}m", on_change=change_alerts_int, active_color=ft.Colors.BLUE_400),
        ft.Text("Messages (one per line)", color=ft.Colors.GREY_300),
        ft.Row([alerts_field]),
        ft.FilledButton("Save Messages", on_click=save_alerts)
    ])

    # Engagement Bot UI
    def toggle_eng(e):
        nonlocal engagement_bot_enabled; engagement_bot_enabled = e.control.value; asyncio.create_task(save_settings())
    def change_eng_int(e):
        nonlocal engagement_interval; engagement_interval = max(1, int(e.control.value)); asyncio.create_task(save_settings())
    async def save_eng(_):
        nonlocal reminder_messages; reminder_messages = [l.strip() for l in eng_field.value.split('\n') if l.strip()]
        await save_settings(); show_toast("Engagement messages saved.")

    eng_field = ft.TextField(value="\n".join(reminder_messages), multiline=True, min_lines=4, max_lines=4, expand=True, bgcolor=ft.Colors.GREY_900)
    eng_card = make_bot_card("Viewer Engagement Bot", "Sends engagement reminders (like/subscribe) on a timer.", [
        ft.Switch(label="Enable Engagement Bot", value=engagement_bot_enabled, on_change=toggle_eng, active_color=ft.Colors.BLUE_400),
        ft.Text("Interval (minutes)", color=ft.Colors.GREY_300),
        ft.Slider(min=1, max=60, divisions=59, value=engagement_interval, label="{value}m", on_change=change_eng_int, active_color=ft.Colors.BLUE_400),
        ft.Text("Messages (one per line)", color=ft.Colors.GREY_300),
        ft.Row([eng_field]),
        ft.FilledButton("Save Messages", on_click=save_eng)
    ])

    # Custom Commands UI
    def toggle_cmd(e):
        nonlocal custom_commands_enabled; custom_commands_enabled = e.control.value; asyncio.create_task(save_settings())
    async def save_cmd(_):
        nonlocal custom_commands
        lines = cmd_field.value.split('\n')
        new_dict = {}
        for l in lines:
            if '|' in l:
                q, a = l.split('|', 1)
                new_dict[q.strip().lower()] = a.strip()
        custom_commands = new_dict
        await save_settings(); show_toast("Commands saved.")
        
    cmd_initial = "\n".join([f"{q} | {a}" for q, a in custom_commands.items()])
    cmd_field = ft.TextField(value=cmd_initial, multiline=True, min_lines=4, max_lines=4, expand=True, bgcolor=ft.Colors.GREY_900)
    cmd_card = make_bot_card("Custom Commands Bot", "Define !commands. Format: !command | Response", [
        ft.Switch(label="Enable Commands Bot", value=custom_commands_enabled, on_change=toggle_cmd, active_color=ft.Colors.BLUE_400),
        ft.Text("Commands (one per line)", color=ft.Colors.GREY_300),
        ft.Row([cmd_field]),
        ft.FilledButton("Save Commands", on_click=save_cmd)
    ])

    # AI Vibe Meter
    async def save_gemini(_):
        nonlocal gemini_api_key
        gemini_api_key = gemini_field.value.strip()
        sentiment.configure(gemini_api_key)
        await save_settings()
        show_toast("API Key saved.")

    gemini_field = ft.TextField(value=gemini_api_key, label="Gemini API Key", password=True, can_reveal_password=True, expand=True, bgcolor=ft.Colors.GREY_900)
    vibe_display = ft.Text("💬", size=48)
    vibe_card = make_bot_card("AI Vibe Meter", "Analyzes chat sentiment every 15s (Requires Gemini Key)", [
        ft.Row([gemini_field]),
        ft.FilledButton("Save Key", on_click=save_gemini),
        ft.Divider(),
        ft.Row([ft.Text("Current Chat Vibe:", size=24, weight=ft.FontWeight.BOLD), vibe_display], alignment=ft.MainAxisAlignment.CENTER)
    ])

    bots_view = ft.Row([
        ft.Column([alerts_card, eng_card], expand=1, scroll=ft.ScrollMode.AUTO),
        ft.Column([cmd_card, vibe_card], expand=1, scroll=ft.ScrollMode.AUTO)
    ], expand=True)

    # ─── Dashboard Navigation ──────────────────────────────────────────────
    dashboard_content = ft.Container(content=moderation_view, padding=ft.Padding(top=10, left=0, right=0, bottom=0), expand=True)

    def switch_tab(e):
        val = list(e.control.selected)[0]
        if val == "moderation":
            dashboard_content.content = moderation_view
        elif val == "bots":
            dashboard_content.content = bots_view
        elif val == "loyalty":
            refresh_loyalty()
            dashboard_content.content = loyalty_view
        page.update()

    tab_selector = ft.SegmentedButton(
        selected=["moderation"],
        on_change=switch_tab,
        segments=[
            ft.Segment(value="moderation", label=ft.Text("Moderation"), icon=Icons.SHIELD),
            ft.Segment(value="bots", label=ft.Text("Bots"), icon=Icons.SMART_TOY),
            ft.Segment(value="loyalty", label=ft.Text("Loyalty"), icon=Icons.PEOPLE),
        ]
    )

    dashboard_tabs = ft.Column([
        tab_selector,
        dashboard_content
    ], expand=True)

    # ─── Shared Header ───────────────────────────────────────────────────────
    async def logout_clicked(_):
        yt_engine.logout()
        show_toast("Logged out.")
        await show_setup()

    header = ft.Row(
        controls=[
            ft.Row([
                ft.Icon(icon=Icons.SHIELD, color=ft.Colors.BLUE_400, size=28),
                ft.Text("StreamGuard", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(f"v{__version__}", size=12, color=ft.Colors.GREY_500),
            ]),
            ft.Row([
                status_dot, ft.Container(width=6), status_label, ft.Container(width=20),
                ft.TextButton("Logout", on_click=logout_clicked),
            ]),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    main_container = ft.Column(controls=[header, ft.Divider(color=ft.Colors.GREY_700)], expand=True)

    # ─── Background Loops ────────────────────────────────────────────────────
    async def alerts_bot_loop():
        idx = 0
        while True:
            for _ in range(alerts_interval * 12):
                await asyncio.sleep(5)
            if chat_fetching_enabled and alerts_bot_enabled and yt_engine.is_connected and yt_engine.live_chat_id and alert_messages:
                msg = alert_messages[idx % len(alert_messages)]
                await asyncio.get_running_loop().run_in_executor(None, yt_engine.send_message, msg)
                idx += 1

    async def engagement_bot_loop():
        idx = 0
        while True:
            for _ in range(engagement_interval * 12):
                await asyncio.sleep(5)
            if chat_fetching_enabled and engagement_bot_enabled and yt_engine.is_connected and yt_engine.live_chat_id and reminder_messages:
                msg = reminder_messages[idx % len(reminder_messages)]
                await asyncio.get_running_loop().run_in_executor(None, yt_engine.send_message, msg)
                idx += 1

    async def sentiment_loop():
        while True:
            await asyncio.sleep(15)
            if chat_fetching_enabled and gemini_api_key and vibe_batch and yt_engine.is_connected:
                vibe = await sentiment.analyze_vibe(vibe_batch)
                vibe_display.value = vibe
                page.update()
                vibe_batch.clear()

    async def poll_chat():
        nonlocal next_page_token
        # Track which message IDs have already triggered a command reply
        replied_ids: set[str] = set()
        loop = asyncio.get_running_loop()
        while True:
            if chat_fetching_enabled and yt_engine.is_connected and yt_engine.live_chat_id:
                try:
                    msgs, next_token = yt_engine.get_chat_messages(next_page_token)
                    if next_token:
                        next_page_token = next_token
                        
                    new_cards = []
                    new_highlights = []
                    
                    for msg in msgs:
                        msg_id = msg["id"]
                        text = msg["snippet"]["displayMessage"]
                        text_lower = text.lower()
                        author_id = msg["authorDetails"]["channelId"]
                        author_name = msg["authorDetails"]["displayName"]
                        msg_type = msg["snippet"]["type"]
                        
                        # 1. Database Tracking
                        db.record_message(author_id, author_name)
                        
                        # 2. Add to Vibe Batch (cap at 50)
                        vibe_batch.append(text)
                        if len(vibe_batch) > 50:
                            vibe_batch.pop(0)
                        
                        # 3. Custom Commands Check (use set to avoid duplicate replies)
                        if custom_commands_enabled and msg_id not in replied_ids:
                            for cmd, response in custom_commands.items():
                                if text_lower.startswith(cmd.lower()):
                                    loop.run_in_executor(None, yt_engine.send_message, response)
                                    replied_ids.add(msg_id)
                                    # Trim replied_ids to prevent unbounded growth
                                    if len(replied_ids) > 500:
                                        replied_ids.clear()
                                    break
                        
                        # 4. Auto Mod Check
                        if auto_mod_enabled and any(w.lower() in text_lower for w in banned_words):
                            ok = await loop.run_in_executor(None, yt_engine.delete_message, msg_id)
                            if ok:
                                show_toast("⚠ Auto-deleted banned message.", is_error=True)
                            continue  # Don't add deleted message to UI
                            
                        # 5. Add to UI
                        card = make_message_card(msg)
                        new_cards.append(card)
                        
                        # 6. Highlights panel
                        if msg_type in ["superChatEvent", "newSponsorEvent", "memberMilestoneChatEvent"]:
                            new_highlights.append(make_message_card(msg))
                            
                    if new_cards:
                        chat_list.controls.extend(new_cards)
                        if len(chat_list.controls) > 100:
                            chat_list.controls = chat_list.controls[-100:]
                            
                    if new_highlights:
                        highlights_list.controls.extend(new_highlights)
                        if len(highlights_list.controls) > 50:
                            highlights_list.controls = highlights_list.controls[-50:]
                            
                    if new_cards or new_highlights:
                        page.update()
                except Exception:
                    logger.exception("Error in poll_chat loop")
            await asyncio.sleep(poll_frequency)

    # ─── Navigation ──────────────────────────────────────────────────────────
    async def show_dashboard():
        main_container.controls = [header, ft.Divider(color=ft.Colors.GREY_700), dashboard_tabs]
        page.update()
        chat_list.controls.clear()
        highlights_list.controls.clear()
        loop = asyncio.get_running_loop()
        chat_id = await loop.run_in_executor(None, yt_engine.get_live_chat_id)
        if chat_id:
            show_toast("Connected to live chat!")
            asyncio.create_task(poll_chat())
            asyncio.create_task(alerts_bot_loop())
            asyncio.create_task(engagement_bot_loop())
            asyncio.create_task(sentiment_loop())
        else:
            show_toast("No active live stream found.", is_error=True)

    async def show_setup():
        main_container.controls = [header, ft.Divider(color=ft.Colors.GREY_700), setup_view]
        page.update()

    # ─── Bootstrap ───────────────────────────────────────────────────────────
    page.add(main_container)
    asyncio.create_task(yt_engine.heartbeat_loop())

    if config.has_credentials() and yt_engine.is_connected:
        await show_dashboard()
    else:
        await show_setup()

if __name__ == "__main__":
    ft.app(main)
