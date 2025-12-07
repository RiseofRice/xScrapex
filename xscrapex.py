"""
xScrapex - Twitter/X Scraper
Monitor a Twitter/X username and get notified of new tweets.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
import sys
from datetime import datetime
from pathlib import Path
from colorama import init, Fore, Style

# Constants
NOTIFICATION_MESSAGE_MAX_LENGTH = 200
DEFAULT_POLLING_INTERVAL = 60


class TwitterScraper:
    """Scraper for monitoring Twitter/X user tweets."""
    
    def __init__(self, username, data_dir=None):
        """
        Initialize the Twitter scraper.
        
        Args:
            username: Twitter/X username to monitor (without @)
            data_dir: Directory to store seen tweets data
        """
        self.username = username.lstrip('@')
        self.data_dir = data_dir or Path.home() / '.xscrapex'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.seen_file = self.data_dir / f'{self.username}_seen.json'
        self.seen_tweets = self._load_seen_tweets()
        
        # User agent to avoid blocks
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def _load_seen_tweets(self):
        """Load previously seen tweet IDs from file."""
        if self.seen_file.exists():
            try:
                with open(self.seen_file, 'r') as f:
                    return set(json.load(f))
            except Exception as e:
                print(f"Warning: Could not load seen tweets: {e}")
                return set()
        return set()
    
    def _save_seen_tweets(self):
        """Save seen tweet IDs to file."""
        try:
            with open(self.seen_file, 'w') as f:
                json.dump(list(self.seen_tweets), f)
        except Exception as e:
            print(f"Warning: Could not save seen tweets: {e}")
    
    def get_tweets(self):
        """
        Fetch recent tweets from the user.
        
        Returns:
            List of tweet dictionaries with 'id', 'text', and 'timestamp'
        """
        # Note: Direct scraping from Twitter/X is challenging due to their anti-bot measures.
        # This uses a simplified approach via nitter (privacy-focused Twitter frontend)
        # Alternative: Use official Twitter API with authentication
        
        tweets = []
        
        # Try multiple nitter instances (updated December 2024)
        # Note: Nitter instance availability changes frequently
        # For updated lists, see: https://status.d420.de/
        nitter_instances = [
            f'https://nitter.net/{self.username}',
            f'https://nitter.poast.org/{self.username}',
            f'https://nitter.privacydev.net/{self.username}',
            f'https://nitter.pussthecat.org/{self.username}',
            f'https://nitter.woodland.cafe/{self.username}',
            f'https://nitter.1d4.us/{self.username}',
            f'https://nitter.kavin.rocks/{self.username}',
            f'https://nitter.unixfox.eu/{self.username}',
            f'https://nitter.moomoo.me/{self.username}',
            f'https://nitter.fdn.fr/{self.username}',
            f'https://nitter.it/{self.username}',
            f'https://nitter.dark.fail/{self.username}',
        ]
        
        last_error = None
        
        for instance_url in nitter_instances:
            try:
                response = requests.get(instance_url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    tweets = self._parse_nitter_page(response.text)
                    if tweets:
                        break
            except requests.exceptions.Timeout:
                last_error = f"Timeout connecting to {instance_url}"
                continue
            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection error for {instance_url}: {type(e).__name__}"
                continue
            except Exception as e:
                last_error = f"Failed to fetch from {instance_url}: {e}"
                continue
        
        if not tweets and last_error:
            print(f"Warning: All Nitter instances failed. Last error: {last_error}")
            print("Note: Nitter instances may be temporarily unavailable. This is normal.")
            print("The scraper will keep trying on the next check.")
        
        return tweets
    
    def _parse_nitter_page(self, html_content):
        """Parse tweets from Nitter HTML page."""
        tweets = []
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find tweet containers in Nitter
            tweet_items = soup.find_all('div', class_='timeline-item')
            
            for item in tweet_items[:10]:  # Get up to 10 recent tweets
                try:
                    # Extract tweet link (contains ID)
                    link = item.find('a', class_='tweet-link')
                    if not link:
                        continue
                    
                    tweet_url = link.get('href', '')
                    # Extract tweet ID from URL
                    tweet_id = tweet_url.split('/')[-1].split('#')[0]
                    
                    # Extract tweet text
                    tweet_content = item.find('div', class_='tweet-content')
                    tweet_text = tweet_content.get_text(strip=True) if tweet_content else ''
                    
                    # Extract timestamp
                    tweet_date = item.find('span', class_='tweet-date')
                    timestamp = tweet_date.get('title', '') if tweet_date else datetime.now().isoformat()
                    
                    if tweet_id and tweet_text:
                        tweets.append({
                            'id': tweet_id,
                            'text': tweet_text,
                            'timestamp': timestamp,
                            'url': f'https://twitter.com/{self.username}/status/{tweet_id}'
                        })
                except Exception as e:
                    print(f"Error parsing tweet item: {e}")
                    continue
            
        except Exception as e:
            print(f"Error parsing page: {e}")
        
        return tweets
    
    def check_new_tweets(self):
        """
        Check for new tweets and return them.
        
        Returns:
            List of new tweet dictionaries
        """
        current_tweets = self.get_tweets()
        new_tweets = []
        
        for tweet in current_tweets:
            if tweet['id'] not in self.seen_tweets:
                new_tweets.append(tweet)
                self.seen_tweets.add(tweet['id'])
        
        if new_tweets:
            self._save_seen_tweets()
        
        return new_tweets


class Notifier:
    """Handle notifications for new tweets."""
    
    def __init__(self):
        """Initialize the notifier."""
        self.use_win10toast = False
        
        # Try to import win10toast for Windows notifications
        if sys.platform == 'win32':
            try:
                from win10toast import ToastNotifier
                self.toaster = ToastNotifier()
                self.use_win10toast = True
            except ImportError:
                print("Note: win10toast not available. Install with: pip install win10toast")
                self.toaster = None
        else:
            self.toaster = None
    
    def notify(self, username, tweet):
        """
        Send a notification about a new tweet.
        
        Args:
            username: Twitter username
            tweet: Tweet dictionary with 'text', 'url', etc.
        """
        title = f"New tweet from @{username}"
        message = tweet['text'][:NOTIFICATION_MESSAGE_MAX_LENGTH]  # Limit message length
        
        # Print to console
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"Time: {tweet.get('timestamp', 'Unknown')}")
        print(f"Text: {message}")
        print(f"URL: {tweet.get('url', 'N/A')}")
        print(f"{'='*60}\n")
        
        # Windows native notification
        if self.use_win10toast and self.toaster:
            try:
                self.toaster.show_toast(
                    title,
                    message,
                    duration=10,
                    threaded=True
                )
            except Exception as e:
                print(f"Failed to show Windows notification: {e}")


def monitor_user(username, interval=DEFAULT_POLLING_INTERVAL):
    """
    Monitor a Twitter/X user for new tweets.
    
    Args:
        username: Twitter username to monitor
        interval: Polling interval in seconds (default: 60)
    """
    init()  # Initialize colorama for Windows
    
    scraper = TwitterScraper(username)
    notifier = Notifier()
    
    print(f"{Fore.CYAN}xScrapex - Twitter/X Scraper{Style.RESET_ALL}")
    print(f"Monitoring @{username} for new tweets...")
    print(f"Checking every {interval} seconds. Press Ctrl+C to stop.\n")
    
    # Initial load - mark existing tweets as seen without notifying
    print(f"{Fore.YELLOW}Loading existing tweets...{Style.RESET_ALL}")
    initial_tweets = scraper.get_tweets()
    if initial_tweets:
        print(f"Found {len(initial_tweets)} recent tweets (marking as seen)")
        for tweet in initial_tweets:
            scraper.seen_tweets.add(tweet['id'])
        scraper._save_seen_tweets()
    else:
        print("No tweets found or unable to fetch. Will keep trying...")
    
    print(f"{Fore.GREEN}Started monitoring. Waiting for new tweets...{Style.RESET_ALL}\n")
    
    try:
        while True:
            new_tweets = scraper.check_new_tweets()
            
            if new_tweets:
                print(f"{Fore.GREEN}Found {len(new_tweets)} new tweet(s)!{Style.RESET_ALL}")
                for tweet in new_tweets:
                    notifier.notify(username, tweet)
            else:
                # Status update every check
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{current_time}] No new tweets. Checking again in {interval} seconds...")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Stopping monitor...{Style.RESET_ALL}")
        print(f"Seen tweets saved to: {scraper.seen_file}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='xScrapex - Monitor Twitter/X users for new tweets',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python xscrapex.py elonmusk
  python xscrapex.py elonmusk --interval 120
        """
    )
    
    parser.add_argument(
        'username',
        help='Twitter/X username to monitor (without @)'
    )
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=DEFAULT_POLLING_INTERVAL,
        help=f'Polling interval in seconds (default: {DEFAULT_POLLING_INTERVAL})'
    )
    
    args = parser.parse_args()
    
    monitor_user(args.username, args.interval)
