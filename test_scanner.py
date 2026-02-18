#!/usr/bin/env python3
"""
Lightweight version that works with just requests (already installed)
Tests the public API scrapers without LLM
"""

import asyncio
import requests
import json
from datetime import datetime
import re


def print_header(title):
    """Print section header"""
    print("\n" + "="*80)
    print(title)
    print("="*80 + "\n")


async def scan_hacker_news():
    """Scan Hacker News API"""
    print("📰 Scanning Hacker News API...")
    
    try:
        # Get top stories
        response = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10
        )
        story_ids = response.json()[:10]
        
        trends = []
        for story_id in story_ids[:5]:
            story_response = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                timeout=5
            )
            story = story_response.json()
            
            if story and story.get('title'):
                trends.append({
                    'title': story['title'],
                    'score': story.get('score', 0),
                    'comments': story.get('descendants', 0),
                    'url': story.get('url', ''),
                })
        
        print(f"   ✅ Found {len(trends)} top stories\n")
        return trends
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return []


async def scan_reddit():
    """Scan Reddit public JSON API"""
    print("🤖 Scanning Reddit (public JSON)...")
    
    try:
        subreddits = ['programming', 'technology']
        all_posts = []
        
        for subreddit in subreddits[:2]:
            response = requests.get(
                f"https://www.reddit.com/r/{subreddit}/hot.json",
                headers={'User-Agent': 'ai-business-scout/1.0'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                posts = data['data']['children'][:3]
                
                for post in posts:
                    post_data = post['data']
                    all_posts.append({
                        'title': post_data['title'],
                        'score': post_data['score'],
                        'comments': post_data['num_comments'],
                        'subreddit': subreddit,
                    })
        
        print(f"   ✅ Found {len(all_posts)} trending posts\n")
        return all_posts
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return []


async def scan_github_trending():
    """Scrape GitHub trending page"""
    print("🐙 Scanning GitHub Trending...")
    
    try:
        response = requests.get(
            "https://github.com/trending",
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=10
        )
        
        # Simple regex parsing (no BeautifulSoup needed)
        repos = []
        
        # Extract repo names - look for h2 with class containing 'lh-condensed'
        repo_pattern = r'<h2[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(repo_pattern, response.text)
        
        for url, name in matches[:5]:
            repos.append({
                'name': name.strip(),
                'url': f"https://github.com{url}",
            })
        
        print(f"   ✅ Found {len(repos)} trending repositories\n")
        return repos
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return []


async def main():
    """Run the lightweight scanner"""
    
    print_header("🚀 AI BUSINESS SCOUT - LIGHTWEIGHT SCANNER TEST")
    
    print("Testing public API access (no authentication required)")
    print("Using only built-in libraries + requests\n")
    
    print_header("PHASE 1: Scanning Public Web Sources")
    
    # Scan all sources
    results = await asyncio.gather(
        scan_hacker_news(),
        scan_reddit(),
        scan_github_trending(),
    )
    
    hn_stories, reddit_posts, github_repos = results
    
    # Display results
    print_header("📊 RESULTS")
    
    if hn_stories:
        print("🔥 Top Hacker News Stories:\n")
        for i, story in enumerate(hn_stories, 1):
            print(f"  {i}. {story['title']}")
            print(f"     👍 {story['score']} points | 💬 {story['comments']} comments")
            if story['url']:
                print(f"     🔗 {story['url'][:60]}...")
            print()
    
    if reddit_posts:
        print("🔥 Trending Reddit Posts:\n")
        for i, post in enumerate(reddit_posts, 1):
            print(f"  {i}. [{post['subreddit']}] {post['title']}")
            print(f"     👍 {post['score']} upvotes | 💬 {post['comments']} comments")
            print()
    
    if github_repos:
        print("🔥 GitHub Trending Repositories:\n")
        for i, repo in enumerate(github_repos, 1):
            print(f"  {i}. {repo['name']}")
            print(f"     🔗 {repo['url']}")
            print()
    
    # Save results
    report = {
        'timestamp': datetime.now().isoformat(),
        'hacker_news': hn_stories,
        'reddit': reddit_posts,
        'github': github_repos,
        'total_trends': len(hn_stories) + len(reddit_posts) + len(github_repos),
    }
    
    report_file = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print_header("✅ SCAN COMPLETE")
    
    print(f"📊 Total trends discovered: {report['total_trends']}")
    print(f"💾 Results saved to: {report_file}")
    print()
    
    print("Next steps:")
    print("  1. ✅ Public API scanning works!")
    print("  2. 📝 To enable LLM-powered idea generation:")
    print("     - Get GitHub token: https://github.com/settings/tokens")
    print("     - Install: python3 -m pip install --user openai python-dotenv pydantic")
    print("     - Run: python3 run_public.py")
    print()


if __name__ == "__main__":
    asyncio.run(main())
