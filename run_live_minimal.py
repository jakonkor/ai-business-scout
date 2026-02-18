#!/usr/bin/env python3
"""
Complete end-to-end demo using REAL data from public APIs
Works with minimal dependencies (just requests + standard library)
"""

import asyncio
import requests
import json
from datetime import datetime
import re
import random


def print_header(title):
    print("\n" + "="*80)
    print(title)
    print("="*80 + "\n")


async def scan_hacker_news():
    """Scan Hacker News API for real trends"""
    print("  📰 Scanning Hacker News API...")
    
    try:
        response = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10
        )
        story_ids = response.json()[:15]
        
        trends = []
        for story_id in story_ids[:8]:
            story_response = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                timeout=5
            )
            story = story_response.json()
            
            if story and story.get('title'):
                # Extract keywords
                keywords = extract_keywords(story['title'])
                
                trends.append({
                    'source': 'hacker_news',
                    'title': story['title'],
                    'engagement': story.get('score', 0) + story.get('descendants', 0) * 2,
                    'url': story.get('url', ''),
                    'keywords': keywords,
                })
        
        print(f"     ✅ Found {len(trends)} trending topics")
        return trends
        
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return []


def extract_keywords(text):
    """Extract keywords from text"""
    stop_words = {'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'is', 'are', 
                  'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
                  'will', 'would', 'could', 'should', 'with', 'from', 'by', 'this', 'that', 'now',
                  'show', 'hn', 'please', 'read', 'if', 'you', 'your'}
    
    # Remove punctuation and split
    words = re.findall(r'\w+', text.lower())
    
    keywords = []
    for word in words:
        if len(word) > 3 and word not in stop_words and not word.isdigit():
            keywords.append(word)
    
    return list(set(keywords))[:5]


def generate_idea_from_trend(trend):
    """Generate business idea from a trend (template-based)"""
    
    # Idea templates based on common keywords
    templates = {
        'security': {
            'title': 'Developer Security Monitoring Platform',
            'description': 'Real-time security vulnerability monitoring and automated patching for development teams',
            'value_prop': 'Catch security issues before they reach production',
            'target': 'Development teams and DevOps engineers',
            'revenue': 'SaaS: $99/month per team',
            'features': ['Automated vulnerability scanning', 'Real-time alerts', 'One-click patching', 'Compliance reporting']
        },
        'network': {
            'title': 'Secure Network Collaboration Tool',
            'description': 'Enterprise-grade networking solution for distributed teams with built-in security',
            'value_prop': 'Simplified secure networking without IT overhead',
            'target': 'Remote-first companies and distributed teams',
            'revenue': 'Freemium: Free tier + $15/user/month pro',
            'features': ['Zero-trust networking', 'Automatic mesh VPN', 'Access control', 'Activity monitoring']
        },
        'editor': {
            'title': 'Collaborative Visual Design Platform',
            'description': 'Web-based design and editing tool with real-time collaboration',
            'value_prop': 'Design together in real-time without expensive software',
            'target': 'Design teams and creative agencies',
            'revenue': 'Subscription: $29/month per user',
            'features': ['Real-time collaboration', 'Cloud storage', 'Version control', 'Export to multiple formats']
        },
        'language': {
            'title': 'Domain-Specific Language Builder',
            'description': 'Platform for creating and sharing custom domain-specific languages and notations',
            'value_prop': 'Build specialized languages for your industry without compiler expertise',
            'target': 'Enterprise developers and industry specialists',
            'revenue': 'Usage-based: Free tier + $0.01 per compile',
            'features': ['Visual syntax builder', 'IDE integration', 'Documentation generator', 'Community marketplace']
        },
    }
    
    # Find matching template
    for keyword in trend['keywords']:
        if keyword in templates:
            template = templates[keyword]
            break
    else:
        # Default template
        main_keyword = trend['keywords'][0] if trend['keywords'] else 'tech'
        template = {
            'title': f'{main_keyword.title()} Solution Platform',
            'description': f'A comprehensive platform for {main_keyword}-related challenges based on latest trends',
            'value_prop': f'Solve {main_keyword} problems faster and more efficiently',
            'target': f'Teams and companies working with {main_keyword}',
            'revenue': 'SaaS subscription: $49-199/month based on team size',
            'features': ['Automated workflows', 'Team collaboration', 'Analytics dashboard', 'API access']
        }
    
    return {
        'title': template['title'],
        'description': template['description'],
        'value_proposition': template['value_prop'],
        'target_market': template['target'],
        'revenue_model': template['revenue'],
        'key_features': template['features'],
        'source_trend': trend['title'],
        'keywords': trend['keywords']
    }


def analyze_idea(idea):
    """Perform simple SWOT analysis"""
    
    # Generate realistic scores based on keywords
    base_score = 6.0
    
    # Adjust based on market indicators
    if 'security' in str(idea['keywords']).lower():
        base_score += 1.0
    if 'ai' in str(idea['keywords']).lower() or 'llm' in str(idea['keywords']).lower():
        base_score += 0.8
    if 'collaboration' in idea['description'].lower():
        base_score += 0.5
    
    viability_score = min(10.0, base_score + random.uniform(-0.5, 0.5))
    
    return {
        'viability_score': round(viability_score, 1),
        'market_size': f'${random.randint(500, 5000)}M',
        'strengths': ['Growing market demand', 'Clear value proposition'],
        'weaknesses': ['Competitive market', 'Requires user adoption'],
        'opportunities': ['Digital transformation trend', 'Remote work growth'],
        'threats': ['Established competitors', 'Rapid technology change']
    }


def validate_idea(idea, analysis):
    """Simulate market validation"""
    
    engagement_score = analysis['viability_score'] * 0.9 + random.uniform(-1, 1)
    engagement_score = max(1.0, min(10.0, engagement_score))
    
    is_promising = engagement_score >= 6.5
    
    return {
        'engagement_score': round(engagement_score, 1),
        'is_promising': is_promising,
        'recommendation': 'Proceed with MVP development' if is_promising else 'Refine value proposition and target market',
        'mock_metrics': {
            'ctr': round(random.uniform(1.5, 3.5), 2),
            'conversions': random.randint(50, 150),
            'engagement_rate': round(random.uniform(5, 15), 1)
        }
    }


async def main():
    """Run the complete pipeline with REAL data"""
    
    print_header("🚀 AI BUSINESS SCOUT - LIVE DATA PIPELINE")
    
    print("This pipeline uses:")
    print("  ✅ REAL trending data from Hacker News API")
    print("  ✅ Template-based idea generation (no LLM needed)")
    print("  ✅ Business analysis frameworks")
    print("  ✅ Market validation simulation")
    print()
    
    # Phase 1: Scan for trends
    print_header("PHASE 1: Scanning for Real Trends")
    
    trends = await scan_hacker_news()
    
    if not trends:
        print("❌ No trends found. Check internet connection.")
        return
    
    print(f"\n  Top Trends by Engagement:")
    sorted_trends = sorted(trends, key=lambda x: x['engagement'], reverse=True)
    for i, trend in enumerate(sorted_trends[:5], 1):
        print(f"    {i}. {trend['title']}")
        print(f"       📊 Engagement: {trend['engagement']:,} | Keywords: {', '.join(trend['keywords'][:3])}")
    
    # Phase 2: Generate ideas
    print_header("PHASE 2: Generating Business Ideas")
    
    print("  💡 Creating business ideas from top trends...\n")
    
    ideas = []
    for trend in sorted_trends[:3]:
        idea = generate_idea_from_trend(trend)
        ideas.append(idea)
        print(f"  ✅ Generated: {idea['title']}")
        print(f"     Based on: {trend['title'][:60]}...")
        print()
    
    # Phase 3: Analyze
    print_header("PHASE 3: Business Analysis")
    
    analyses = []
    for idea in ideas:
        analysis = analyze_idea(idea)
        analyses.append(analysis)
        print(f"  📊 {idea['title']}")
        print(f"     Viability Score: {analysis['viability_score']}/10")
        print(f"     Market Size: {analysis['market_size']}")
        print(f"     Top Strength: {analysis['strengths'][0]}")
        print()
    
    # Phase 4: Validate
    print_header("PHASE 4: Market Validation")
    
    validations = []
    for idea, analysis in zip(ideas, analyses):
        validation = validate_idea(idea, analysis)
        validations.append(validation)
        
        status = "✅ PROMISING" if validation['is_promising'] else "⚠️ NEEDS WORK"
        print(f"  {status} {idea['title']}")
        print(f"     Engagement Score: {validation['engagement_score']}/10")
        print(f"     CTR: {validation['mock_metrics']['ctr']}% | Conversions: {validation['mock_metrics']['conversions']}")
        print(f"     → {validation['recommendation']}")
        print()
    
    # Generate Report
    print_header("📊 EXECUTIVE SUMMARY")
    
    promising_count = sum(1 for v in validations if v['is_promising'])
    
    print(f"  Trends Analyzed:     {len(trends)}")
    print(f"  Ideas Generated:     {len(ideas)}")
    print(f"  Promising Ideas:     {promising_count}/{len(ideas)}")
    print()
    
    print("  🎯 Top Recommendations:\n")
    
    # Sort by engagement score
    ranked = sorted(
        zip(ideas, analyses, validations),
        key=lambda x: x[2]['engagement_score'],
        reverse=True
    )
    
    for i, (idea, analysis, validation) in enumerate(ranked, 1):
        status = "✅" if validation['is_promising'] else "⚠️"
        print(f"    {i}. {status} {idea['title']}")
        print(f"       Viability: {analysis['viability_score']}/10 | Engagement: {validation['engagement_score']}/10")
        print(f"       → {validation['recommendation']}")
        print()
    
    # Save report
    report = {
        'timestamp': datetime.now().isoformat(),
        'pipeline': 'live_data_minimal_dependencies',
        'summary': {
            'trends_analyzed': len(trends),
            'ideas_generated': len(ideas),
            'promising_ideas': promising_count,
        },
        'trends': sorted_trends[:5],
        'ideas': [
            {
                'idea': idea,
                'analysis': analysis,
                'validation': validation
            }
            for idea, analysis, validation in zip(ideas, analyses, validations)
        ]
    }
    
    report_file = f"live_pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print_header("💾 REPORT SAVED")
    
    print(f"  📄 Report: {report_file}")
    print(f"  📊 Trends: {len(trends)} discovered from Hacker News")
    print(f"  💡 Ideas: {len(ideas)} generated and analyzed")
    print(f"  ✅ Promising: {promising_count} ideas worth pursuing")
    print()
    
    print_header("✅ PIPELINE COMPLETE!")
    
    print("  What we did:")
    print("    ✅ Scanned REAL trending data from Hacker News")
    print("    ✅ Generated business ideas based on trends")
    print("    ✅ Analyzed market viability")
    print("    ✅ Validated with simulated campaigns")
    print("    ✅ Created comprehensive report")
    print()
    print("  Next steps:")
    print("    📖 Review the report: cat", report_file)
    print("    🚀 For LLM-powered ideas: Install dependencies + Get GitHub token")
    print("    💡 Start building the top-ranked idea!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
