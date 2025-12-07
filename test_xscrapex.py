"""
Test script for xScrapex - Twitter/X Scraper

This script demonstrates the basic functionality with mock data
since direct web scraping requires network access.
"""

import sys
from pathlib import Path

# Add the parent directory to the path to import xscrapex
sys.path.insert(0, str(Path(__file__).parent))

from xscrapex import TwitterScraper, Notifier


def test_scraper_initialization():
    """Test TwitterScraper initialization."""
    print("Testing TwitterScraper initialization...")
    scraper = TwitterScraper("testuser")
    assert scraper.username == "testuser"
    assert scraper.seen_tweets == set()
    print("✓ TwitterScraper initialization works")


def test_notifier_initialization():
    """Test Notifier initialization."""
    print("\nTesting Notifier initialization...")
    notifier = Notifier()
    # On non-Windows systems, win10toast won't be available
    assert notifier is not None
    print("✓ Notifier initialization works")


def test_notification():
    """Test notification with mock data."""
    print("\nTesting notification with mock tweet...")
    notifier = Notifier()
    
    mock_tweet = {
        'id': '1234567890',
        'text': 'This is a test tweet to verify notifications work!',
        'timestamp': '2025-12-07T16:30:00+00:00',
        'url': 'https://twitter.com/testuser/status/1234567890'
    }
    
    notifier.notify("testuser", mock_tweet)
    print("✓ Notification test completed (check console output above)")


def test_seen_tweets_management():
    """Test seen tweets tracking."""
    print("\nTesting seen tweets management...")
    scraper = TwitterScraper("testuser2")
    
    # Add some tweet IDs
    scraper.seen_tweets.add("tweet1")
    scraper.seen_tweets.add("tweet2")
    scraper.seen_tweets.add("tweet3")
    
    assert len(scraper.seen_tweets) == 3
    assert "tweet1" in scraper.seen_tweets
    assert "tweet2" in scraper.seen_tweets
    assert "tweet3" in scraper.seen_tweets
    
    # Save and reload
    scraper._save_seen_tweets()
    
    scraper2 = TwitterScraper("testuser2")
    assert len(scraper2.seen_tweets) == 3
    assert "tweet1" in scraper2.seen_tweets
    
    print("✓ Seen tweets tracking works")


def test_argument_parsing():
    """Test command-line argument parsing."""
    print("\nTesting username parsing...")
    
    # Test with @ symbol
    scraper1 = TwitterScraper("@testuser")
    assert scraper1.username == "testuser", "Should strip @ symbol"
    
    # Test without @ symbol
    scraper2 = TwitterScraper("testuser")
    assert scraper2.username == "testuser", "Should work without @ symbol"
    
    print("✓ Username parsing works")


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("xScrapex Test Suite")
    print("="*60)
    
    try:
        test_scraper_initialization()
        test_notifier_initialization()
        test_notification()
        test_seen_tweets_management()
        test_argument_parsing()
        
        print("\n" + "="*60)
        print("All tests passed! ✓")
        print("="*60)
        return 0
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
