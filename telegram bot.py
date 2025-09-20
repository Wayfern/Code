import os
import asyncio
import logging
import random
import tempfile
from datetime import datetime, timedelta
from typing import Dict, Any
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
        logger = logging.getLogger(__name__)
        file_storage: Dict[str, Dict[str, Any]] = {}
def generate_mock_stats() -> Dict[str, Any]:
    return {
        "tire_pressure": [round(random.uniform(30, 35), 1) for _ in range(6)],
        "battery_levels": [round(random.uniform(85, 100), 1) for _ in range(4)],
        "water_tank_level": round(random.uniform(40, 95), 1),
        "angle": {"pitch": round(random.uniform(-5, 5), 2),"roll": round(random.uniform(-3, 3), 2)},
        "inside_temperature": round(random.uniform(18, 25), 1),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
#----------------------------------------------------------------------------------------------------------------
# Pasword check
#----------------------------------------------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('authenticated', False):
        context.user_data['awaiting_password'] = True
    await update.message.reply_text("Please enter the password to access this bot:")
    return
    await update.message.reply_text("Use /commands to see all available commands.")
#----------------------------------------------------------------------------------------------------------------
# Demo bus status command
#----------------------------------------------------------------------------------------------------------------
async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('authenticated', False):
    await update.message.reply_text("Access denied. Please use /start to authenticate first.")
    return
        stats = generate_mock_stats()
        total_battery = sum(stats["battery_levels"])
        avg_battery = total_battery / len(stats["battery_levels"])
        stat_message = (
        f"**Bus Statistics**\n"
        f"Tire Pressure (PSI):\n"
        f"   Tire 1: {stats['tire_pressure'][0]} | Tire 2: {stats['tire_pressure'][1]}\n"
        f"   Tire 3: {stats['tire_pressure'][2]} | Tire 4: {stats['tire_pressure'][3]}\n"
        f"   Tire 5: {stats['tire_pressure'][4]} | Tire 6: {stats['tire_pressure'][5]}\n\n"
        f"Battery Levels (%):\n"
        f"   Battery 1: {stats['battery_levels'][0]}% | Battery 2: {stats['battery_levels'][1]}%\n"
        f"   Battery 3: {stats['battery_levels'][2]}% | Battery 4: {stats['battery_levels'][3]}%\n"
        f"   **Total: {total_battery:.1f}% | Average: {avg_battery:.1f}%**\n\n"
        f"Water Tank Level: {stats['water_tank_level']}%\n\n"
        f"Vehicle Angle:\n"
        f"   Pitch: {stats['angle']['pitch']}°\n"
        f"   Roll: {stats['angle']['roll']}°\n\n"
        f"Inside Temperature: {stats['inside_temperature']}°C\n\n"
        f"Last Updated: {stats['timestamp']}")
    await update.message.reply_text(stat_message, parse_mode='Markdown')
#----------------------------------------------------------------------------------------------------------------
# Demo notification system
#----------------------------------------------------------------------------------------------------------------
async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('authenticated', False):
    await update.message.reply_text("Access denied. Please use /start to authenticate first.")
    return
    await update.message.reply_text("Notification scheduled for 5 seconds...")
    await asyncio.sleep(5)
        notification_messages = [
        "**Notice!** Motion detected outside the vehicle!",
        "**Alert!** Unauthorized movement detected near bus perimeter!",
        "**Warning!** External motion sensor triggered - possible intrusion!",
        "**Security Alert!** Activity detected around vehicle exterior!",
        "**Motion Detected!** Movement registered by perimeter sensors!",
        "**Attention!** Suspicious activity detected outside bus!",
        "**Proximity Alert!** Object or person detected near vehicle!",
        "**Sensor Triggered!** External motion detection system activated!",
        "**Perimeter Breach!** Movement detected in restricted zone!",
        "**Activity Alert!** Motion sensors indicate external presence!"]
        selected_message = random.choice(notification_messages)
    await update.message.reply_text(selected_message, parse_mode='Markdown')
#----------------------------------------------------------------------------------------------------------------
# Demo file upload system (holds files temporarily in the chat history)
#----------------------------------------------------------------------------------------------------------------
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('authenticated', False):
    await update.message.reply_text("Access denied. Please use /start to authenticate first.")
    return
    if not context.args:
    await update.message.reply_text("Please provide an ID: `/upload <ID>`", parse_mode='Markdown')
    return
        file_id = " ".join(context.args)
        context.user_data['pending_upload'] = file_id
    await update.message.reply_text(
        f"Ready to receive file with ID: `{file_id}`\n"
        f"Please send the file now...",
        parse_mode='Markdown')
async def handle_file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'pending_upload' not in context.user_data:
    return
        file_id = context.user_data['pending_upload']
        file_obj = None
        file_name = None
        file_type = None
    if update.message.document:
        file_obj = update.message.document
        file_name = file_obj.file_name
        file_type = "document"
    elif update.message.photo:
        file_obj = update.message.photo[-1]
        file_name = f"photo_{file_id}.jpg"
        file_type = "photo"
    elif update.message.video:
        file_obj = update.message.video
        file_name = f"video_{file_id}.mp4"
        file_type = "video"
    elif update.message.audio:
        file_obj = update.message.audio
        file_name = f"audio_{file_id}.mp3"
        file_type = "audio"
    else:
    await update.message.reply_text("Unsupported file type!")
    return
        file_storage[file_id] = {
        'file_obj': file_obj,
        'file_name': file_name,
        'file_type': file_type,
        'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'file_size': getattr(file_obj, 'file_size', 0)}
    del context.user_data['pending_upload']
    await update.message.reply_text(
        f"File uploaded successfully!\n"
        f"**ID:** `{file_id}`\n"
        f"**Name:** {file_name}\n"
        f"**Size:** {file_storage[file_id]['file_size']} bytes\n"
        f"**Uploaded:** {file_storage[file_id]['upload_time']}",
        parse_mode='Markdown')
#----------------------------------------------------------------------------------------------------------------
# Demo file get system (once again just pulls from the chat history)
#----------------------------------------------------------------------------------------------------------------
async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('authenticated', False):
    await update.message.reply_text("Access denied. Please use /start to authenticate first.")
    return
    if not context.args:
    await update.message.reply_text("Please provide an ID: `/get <ID>`", parse_mode='Markdown')
    return
        file_id = " ".join(context.args)
    if file_id not in file_storage:
    await update.message.reply_text(f"No file found with ID: `{file_id}`", parse_mode='Markdown')
    return
        stored_file = file_storage[file_id]
    await update.message.reply_text(
        f"Sending file: `{stored_file['file_name']}`\n"
        f"Uploaded: {stored_file['upload_time']}",
        parse_mode='Markdown')
    try:
    if stored_file['file_type'] == 'document':
    await update.message.reply_document(stored_file['file_obj'].file_id)
    elif stored_file['file_type'] == 'photo':
    await update.message.reply_photo(stored_file['file_obj'].file_id)
    elif stored_file['file_type'] == 'video':
    await update.message.reply_video(stored_file['file_obj'].file_id)
    elif stored_file['file_type'] == 'audio':
    await update.message.reply_audio(stored_file['file_obj'].file_id)
    except Exception as e:
    await update.message.reply_text(f"Error sending file: {str(e)}")
#----------------------------------------------------------------------------------------------------------------
# Demo pi sleep/wake system (used to toggle the pi from a super low power mode where it only runs this)
#----------------------------------------------------------------------------------------------------------------
#----< Wake >----
async def wake(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('authenticated', False):
    await update.message.reply_text("Access denied. Please use /start to authenticate first.")
    return
    await update.message.reply_text("Sending wake signal...")
    await asyncio.sleep(1)
    await update.message.reply_text("Pi is now awake.")
#----< Sleep >----
async def sleep(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('authenticated', False):
    await update.message.reply_text("Access denied. Please use /start to authenticate first.")
    return
    await update.message.reply_text("Sending sleep signal...")
    await asyncio.sleep(1)
    await update.message.reply_text("Pi is now sleeping.")
#----------------------------------------------------------------------------------------------------------------
# Demo communication to the pi
#----------------------------------------------------------------------------------------------------------------
async def pi_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('authenticated', False):
    await update.message.reply_text("Access denied. Please use /start to authenticate first.")
    return
    if not context.args:
    await update.message.reply_text("Please provide a command: `/pi <command>`\nAvailable commands: `terminal`", parse_mode='Markdown')
    return
        command = context.args[0].lower()
    if command == "terminal":
        context.user_data['pi_mode'] = 'terminal'
        remaining_args = " ".join(context.args[1:]) if len(context.args) > 1 else ""
    if remaining_args:
    await execute_terminal_command(update, remaining_args)
    else:
    await update.message.reply_text("**Pi Terminal Mode**\nSend terminal commands directly. Type `exit` to leave terminal mode.", parse_mode='Markdown')
    else:
    await update.message.reply_text("Unknown command. Available commands: `terminal`", parse_mode='Markdown')
    async def execute_terminal_command(update: Update, command: str) -> None:
        mock_responses = {
        "ls": "Documents  Downloads  Pictures  Desktop  test.txt  config.py",
        "pwd": "/home/pi",
        "whoami": "pi",
        "date": datetime.now().strftime("%a %b %d %H:%M:%S UTC %Y"),
        "uname -a": "Linux raspberrypi 5.15.84-v8+ #1613 SMP PREEMPT Thu Jan 5 12:01:26 GMT 2023 aarch64 GNU/Linux",
        "df -h": "Filesystem      Size  Used Avail Use% Mounted on\n/dev/root        15G  4.2G   10G  30% /",
        "free -h": "               total        used        free      shared  buff/cache   available\nMem:           3.7Gi       456Mi       2.8Gi        37Mi       512Mi       3.1Gi",
        "uptime": "12:34:56 up 2 days, 14:23,  1 user,  load average: 0.15, 0.20, 0.18",
        "vcgencmd measure_temp": "temp=42.8'C",
        "vcgencmd get_throttled": "throttled=0x0",
        "ps aux --sort=-%cpu | head -5": "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\nroot         1  0.2  0.8  27384  8192 ?        Ss   10:32   0:02 /sbin/init\npi        1234  1.5  2.1  45632 12288 ?        S    10:33   0:15 python3 bot.py\nroot       456  0.8  0.5  12345  4096 ?        S    10:32   0:01 systemd",
        "iostat": "avg-cpu:  %user   %nice %system %iowait  %steal   %idle\n           2.15    0.00    1.82    0.45    0.00   95.58"}
    if command.lower() == "all":
        all_stats = f"""**System Status**
        **----System Information----**
        {mock_responses['uname -a']}
        **-------Current Time-------**
        {mock_responses['date']}
        **-------System Uptime------**
        {mock_responses['uptime']}
        **-------Memory Usage-------**
        {mock_responses['free -h']}
        **--------Disk Usage--------**
        {mock_responses['df -h']}
        **------CPU Temperature-----**
        {mock_responses['vcgencmd measure_temp']}
        **-----Throttling Status----**
        {mock_responses['vcgencmd get_throttled']}
        **-----Top CPU Processes----**
        {mock_responses['ps aux --sort=-%cpu | head -5']}
        **-------CPU Statistics-----**
        {mock_responses['iostat']}"""
    await update.message.reply_text(all_stats, parse_mode='Markdown')
    return
    if command.lower() in mock_responses:
        response = mock_responses[command.lower()]
    elif command.lower().startswith("cat "):
        filename = command[4:]
    if filename == "test.txt":
        response = "dam"
    else:
        response = f"cat: {filename}: No such file or directory"
    else:
        response = f"Command '{command}' executed successfully"
    await update.message.reply_text(f"```\npi@raspberrypi:~$ {command}\n{response}\n```", parse_mode='Markdown')
    if 'pi_mode' not in context.user_data:
    return
        user_input = update.message.text.strip()
    if context.user_data['pi_mode'] == 'terminal':
    if user_input.lower() == 'exit':
    del context.user_data['pi_mode']
    await update.message.reply_text("Exited terminal mode.")
    return
    await execute_terminal_command(update, user_input)
    return
#----------------------------------------------------------------------------------------------------------------
# Command list
#----------------------------------------------------------------------------------------------------------------
async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('authenticated', False):
    await update.message.reply_text("Access denied. Please use /start to authenticate first.")
    return
        commands_text = (
        "**Commands**\n\n"
        "`/stat` - Display current bus stats\n"
        "`/notify` - Test notification system\n"
        "`/upload <ID>` - Upload a file with specified ID\n"
        "`/get <ID>` - Retrieve a stored file by ID\n"
        "`/wake` - Wake up the Pi\n"
        "`/sleep` - Put the Pi to sleep\n"
        "`/pi <command>` - Interact with Raspberry Pi\n"
        "`/pi terminal` - Access Pi terminal\n\n"
        "`/commands` - Show this help message\n\n"
        "-------------------")
    await update.message.reply_text(commands_text, parse_mode='Markdown')
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.warning(f'Update {update} caused error {context.error}')
#----------------------------------------------------------------------------------------------------------------
async def handle_pi_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'awaiting_password' in context.user_data:
        password = update.message.text.strip()
        correct_password = os.getenv('PASSWORD')
    if not correct_password:
    await update.message.reply_text("Password not configured. Contact administrator.")
    return
    if password == correct_password:
        context.user_data['authenticated'] = True
    del context.user_data['awaiting_password']
    await update.message.reply_text("Access granted")
    else:
    await update.message.reply_text("Incorrect password your stupid....")
    return
    if not context.user_data.get('authenticated', False):
    await update.message.reply_text("No")
    return
#----------------------------------------------------------------------------------------------------------------
def main() -> None:
         token = os.getenv('TOKEN')
         password = os.getenv('PASSWORD')
    if not token:
        logger.error("TOKEN environment variable not set")
    print("Error: Please set the TOKEN environment variable")
    print("   Example: export TOKEN='token_here (im not putting it here)'")
    return
    if not password:
        logger.error("PASSWORD environment variable not set!")
    print("Error: Please set the PASSWORD environment variable")
    print("   Example: export PASSWORD='password_here (im not putting it here)'")
    return
        application = Application.builder().token(token).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("stat", stat))
        application.add_handler(CommandHandler("notify", notify))
        application.add_handler(CommandHandler("upload", upload))
        application.add_handler(CommandHandler("get", get_file))
        application.add_handler(CommandHandler("wake", wake))
        application.add_handler(CommandHandler("sleep", sleep))
        application.add_handler(CommandHandler("pi", pi_command))
        application.add_handler(CommandHandler("commands", commands))
        application.add_handler(MessageHandler(
        filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO, 
        handle_file_upload))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_pi_navigation))
        application.add_error_handler(error_handler)
    print("starting...")
    print("running. Press Ctrl+C to stop.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    if __name__ == '__main__':
        main()