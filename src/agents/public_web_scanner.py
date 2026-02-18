"""
Public Web Scanner Agent - Uses free public APIs
No authentication required for most sources
"""

import asyncio
from typing import List, Dict, Any
from datetime import datetime
import uuid
import requests
from bs4 import BeautifulSoup

from ..models import Trend, TrendSource


class PublicWebScanner:
    """
    Scanner that uses publicly available data sources:
    - Hacker News API (free, no auth)
    - Reddit JSON API (public, no auth)
    - Google Trends (via pytrends)
    - NewsAPI (optional, free tier)
    """
    
    def __init__(self, news_api_key: str = None):
        self.news_api_key = news_api_key
        self.trends: List[Trend] = []
    
    async def scan_all_sources(self) -> List[Trend]:
        """Scan all public sources for trends."""
        print("🔍 Public Web Scanner: Starting scan...")
        
        tasks = [
            self._scan_hacker_news(),
            self._scan_reddit_public(),
            self._scan_github_trending(),
        ]
        
        if self.news_api_key:
            tasks.append(self._scan_news_api())
        
        # Run all scans concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten results
        all_trends = []
        for result in results:
            if isinstance(result, list):
                all_trends.extend(result)
            elif isinstance(result, Exception):
                print(f"⚠️  Error during scan: {result}")
        
        self.trends = all_trends
        print(f"✅ Public Web Scanner: Found {len(all_trends)} trends")
        
        return all_trends
    
    async def _scan_hacker_news(self) -> List[Trend]:
        """Scan Hacker News front page and top stories."""
        print("  📰 Scanning Hacker News...")
        
        try:
            # Get top stories
            response = requests.get(
                "https://hacker-news.firebaseio.com/v0/topstories.json",
                timeout=10
            )
            story_ids = response.json()[:10]  # Top 10 stories
            
            trends = []
            keywords_map = {}
            
            for story_id in story_ids[:5]:  # Process first 5
                story_response = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    timeout=5
                )
                story = story_response.json()
                
                if story and story.get('title'):
                    # Extract keywords from title
                    title = story['title']
                    keywords = self._extract_keywords(title)
                    
                    # Group by keywords
                    for kw in keywords:
                        if kw not in keywords_map:
                            keywords_map[kw] = []
                        keywords_map[kw].append({
                            'title': title,
                            'score': story.get('score', 0),
                            'comments': story.get('descendants', 0)
                        })
            
            # Create trends from keyword groups
            for keyword, stories in keywords_map.items():
                if len(stories) >= 1:  # At least 1 story
                    total_engagement = sum(s['score'] + s['comments'] for s in stories)
                    
                    trends.append(Trend(
                        id=str(uuid.uuid4()),
                        source=TrendSource.NEWS,
                        title=f"{keyword.title()} Trending on HN",
                        description=f"Multiple Hacker News stories discussing {keyword}: {stories[0]['title'][:100]}...",
                        sentiment=0.7,
                        engagement=total_engagement,
                        keywords=[keyword] + self._extract_keywords(' '.join(s['title'] for s in stories)),
                    ))
            
            return trends[:3]  # Return top 3 trends
            
        except Exception as e:
            print(f"  ❌ Error scanning Hacker News: {e}")
            return []
    
    async def _scan_reddit_public(self) -> List[Trend]:
        """Scan Reddit public JSON API (no auth required)."""
        print("  🤖 Scanning Reddit (public)...")
        
        try:
            # Scan multiple tech subreddits
            subreddits = ['programming', 'technology', 'startups', 'entrepreneur']
            trends = []
            
            for subreddit in subreddits[:2]:  # First 2 to avoid rate limits
                response = requests.get(
                    f"https://www.reddit.com/r/{subreddit}/hot.json",
                    headers={'User-Agent': 'ai-business-scout/1.0'},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data['data']['children'][:5]
                    
                    for post in posts:
                        post_data = post['data']
                        
                        trends.append(Trend(
                            id=str(uuid.uuid4()),
                            source=TrendSource.REDDIT,
                            title=post_data['title'],
                            description=post_data.get('selftext', '')[:200],
                            sentiment=0.6,
                            engagement=post_data['score'] + post_data['num_comments'],
                            keywords=self._extract_keywords(post_data['title']),
                        ))
            
            return trends[:5]  # Return top 5
            
        except Exception as e:
            print(f"  ❌ Error scanning Reddit: {e}")
            return []
    
    async def _scan_github_trending(self) -> List[Trend]:
        """Scrape GitHub trending page."""
        print("  🐙 Scanning GitHub Trending...")
        
        try:
            response = requests.get(
                "https://github.com/trending",
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            repos = soup.find_all('article', class_='Box-row')[:5]
            
            trends = []
            for repo in repos:
                title_elem = repo.find('h2')
                if title_elem:
                    repo_name = title_elem.text.strip().replace('\n', '').replace(' ', '')
                    
                    desc_elem = repo.find('p', class_='col-9')
                    description = desc_elem.text.strip() if desc_elem else ""
                    
                    # Get stars
                    stars_elem = repo.find('svg', {'aria-label': 'star'})
                    stars = 0
                    if stars_elem and stars_elem.parent:
                        stars_text = stars_elem.parent.text.strip()
                        try:
                            stars = int(stars_text.replace(',', ''))
                        except:
                            pass
                    
                    trends.append(Trend(
                        id=str(uuid.uuid4()),
                        source=TrendSource.GOOGLE_TRENDS,
                        title=f"GitHub: {repo_name}",
                        description=description[:200],
                        sentiment=0.8,
                        engagement=stars,
                        keywords=self._extract_keywords(repo_name + " " + description),
                    ))
            
            return trends
            
        except Exception as e:
            print(f"  ❌ Error scanning GitHub: {e}")
            return []
    
    async def _scan_news_api(self) -> List[Trend]:
        """Scan NewsAPI (optional, requires free API key)."""
        print("  📰 Scanning NewsAPI...")
        
        if not self.news_api_key:
            return []
        
        try:
            response = requests.get(
                "https://newsapi.org/v2/top-headlines",
                params={
                    'apiKey': self.news_api_key,
                    'category': 'technology',
                    'language': 'en',
                    'pageSize': 10,
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                trends = []
                for article in articles[:5]:
                    trends.append(Trend(
                        id=str(uuid.uuid4()),
                        source=TrendSource.NEWS,
                        title=article['title'],
                        description=article.get('description', '')[:200],
                        sentiment=0.7,
                        engagement=1000,  # NewsAPI doesn't provide engagement
                        keywords=self._extract_keywords(article['title']),
                    ))
                
                return trends
            
        except Exception as e:
            print(f"  ❌ Error scanning NewsAPI: {e}")
        
        return []
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text (simple version)."""
        # Remove common words
        stop_words = {'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'with', 'from', 'by', 'this', 'that', 'these', 'those'}
        
        words = text.lower().split()
        keywords = []
        
        for word in words:
            # Clean word
            word = ''.join(c for c in word if c.isalnum())
            if len(word) > 3 and word not in stop_words:
                keywords.append(word)
        
        # Return unique keywords
        return list(set(keywords))[:5]
    
    def get_top_trends(self, limit: int = 10) -> List[Trend]:
        """Get top trends sorted by engagement."""
        sorted_trends = sorted(self.trends, key=lambda t: t.engagement, reverse=True)
        return sorted_trends[:limit]


async def main():
    """Test the Public Web Scanner"""
    scanner = PublicWebScanner()
    trends = await scanner.scan_all_sources()
    
    print("\n" + "="*60)
    print("Top Trends from Public Sources:")
    print("="*60)
    
    for trend in scanner.get_top_trends(5):
        print(f"\n📍 {trend.title}")
        print(f"   Source: {trend.source.value}")
        print(f"   Engagement: {trend.engagement:,}")
        print(f"   Keywords: {', '.join(trend.keywords[:5])}")
        print(f"   {trend.description[:100]}...")


if __name__ == "__main__":
    asyncio.run(main())
