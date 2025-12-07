# xScrapex

A Twitter/X scraper that monitors a given username and sends notifications for every new tweet. Runs natively on Windows with native toast notifications.

## Features

- 🔍 Monitor any Twitter/X user for new tweets
- 🔔 Windows native notifications for new tweets
- 💾 Persistent storage of seen tweets
- 🎨 Colorful console output
- ⚙️ Configurable polling interval
- 🛡️ No API keys required - uses web scraping

## Requirements

- Python 3.7 or higher
- Windows OS (for native notifications)
- Internet connection

## Installation

1. Clone this repository:
```bash
git clone https://github.com/RiseofRice/xScrapex.git
cd xScrapex
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Monitor a Twitter/X user (default: check every 60 seconds):
```bash
python xscrapex.py username
```

Example:
```bash
python xscrapex.py elonmusk
```

### Advanced Usage

Specify custom polling interval (in seconds):
```bash
python xscrapex.py username --interval 120
```

Or using short form:
```bash
python xscrapex.py username -i 120
```

### Command-Line Options

- `username` - Twitter/X username to monitor (required, without @)
- `--interval` or `-i` - Polling interval in seconds (default: 60)

## How It Works

1. **Initial Load**: On first run, the scraper fetches recent tweets and marks them as "seen" without notifying
2. **Monitoring**: Continuously checks for new tweets at the specified interval
3. **Notification**: When a new tweet is detected:
   - Displays in the console with full details
   - Shows a Windows toast notification (on Windows)
   - Saves the tweet ID to avoid duplicate notifications
4. **Persistence**: Seen tweet IDs are stored in `~/.xscrapex/` directory

## Data Storage

Tweet data is stored locally in:
- Windows: `C:\Users\<YourUsername>\.xscrapex\`
- Format: `<username>_seen.json`

This file contains tweet IDs that have already been seen to prevent duplicate notifications.

## Notes

- **Web Scraping**: This tool uses web scraping via Nitter (privacy-focused Twitter frontend) to avoid requiring Twitter API keys
- **Rate Limiting**: Be respectful with polling intervals. Recommended minimum: 60 seconds
- **Reliability**: Nitter instances may occasionally be unavailable. The tool tries multiple instances automatically
- **Windows Only**: Native notifications work best on Windows 10+. On other platforms, console output is still available

## Troubleshooting

### "No tweets found"
- The Nitter instances might be temporarily unavailable
- Check your internet connection
- Try increasing the polling interval
- The username might be misspelled or the account might be private

### "win10toast not available"
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Console notifications will still work

### High CPU/Memory Usage
- Increase the polling interval with `--interval` option
- The tool uses minimal resources when idle between checks

## Example Output

```
xScrapex - Twitter/X Scraper
Monitoring @elonmusk for new tweets...
Checking every 60 seconds. Press Ctrl+C to stop.

Loading existing tweets...
Found 10 recent tweets (marking as seen)
Started monitoring. Waiting for new tweets...

[2025-12-07 16:35:18] No new tweets. Checking again in 60 seconds...

Found 1 new tweet(s)!

============================================================
New tweet from @elonmusk
Time: 2025-12-07T16:36:00+00:00
Text: This is a new tweet!
URL: https://twitter.com/elonmusk/status/1234567890
============================================================
```

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational purposes only. Please respect Twitter's Terms of Service and use responsibly. The tool uses publicly available data and does not circumvent any access controls.