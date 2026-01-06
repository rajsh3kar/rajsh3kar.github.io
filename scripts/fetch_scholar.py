#!/usr/bin/env python3
"""
Fetch publications from Google Scholar and save to JSON for Astro site.
Auto-generates publication data that can be imported in Astro components.
"""

import os
import json
from datetime import datetime

try:
    from scholarly import scholarly
except ImportError:
    print("Error: scholarly package not installed")
    print("Install with: pip install scholarly")
    exit(1)

def fetch_publications(scholar_id):
    """Fetch all publications for a given Google Scholar ID."""
    print(f"Fetching publications for Scholar ID: {scholar_id}")
    
    try:
        # Get author profile
        search_query = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(search_query)
        
        publications = []
        
        for pub in author['publications']:
            try:
                # Fill publication details
                filled_pub = scholarly.fill(pub)
                
                # Extract key information
                pub_data = {
                    'title': filled_pub['bib'].get('title', 'Untitled'),
                    'authors': filled_pub['bib'].get('author', ''),
                    'venue': filled_pub['bib'].get('venue', ''),
                    'year': filled_pub['bib'].get('pub_year', ''),
                    'citations': filled_pub.get('num_citations', 0),
                    'url': filled_pub.get('pub_url', ''),
                    'abstract': filled_pub['bib'].get('abstract', '')
                }
                
                publications.append(pub_data)
                print(f"  ✓ Fetched: {pub_data['title'][:60]}...")
            except Exception as e:
                print(f"  ⚠ Skipped publication due to error: {e}")
                continue
        
        # Sort by year (most recent first), then by citations
        publications.sort(key=lambda x: (int(x.get('year', 0) or 0), x.get('citations', 0)), reverse=True)
        
        return {
            'last_updated': datetime.now().isoformat(),
            'scholar_id': scholar_id,
            'total_publications': len(publications),
            'publications': publications
        }
        
    except Exception as e:
        print(f"❌ Error fetching publications: {e}")
        return None

def main():
    scholar_id = os.environ.get('SCHOLAR_ID', 'wq36gfgAAAAJ')
    
    print("=" * 60)
    print("Google Scholar Publication Fetcher")
    print("=" * 60)
    
    # Fetch publications
    data = fetch_publications(scholar_id)
    
    if data:
        # Create output directory if it doesn't exist
        os.makedirs('src/data', exist_ok=True)
        
        # Save to JSON
        output_file = 'src/data/publications.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Successfully saved {len(data['publications'])} publications to {output_file}")
        print(f"📊 Total citations across all publications: {sum(p['citations'] for p in data['publications'])}")
    else:
        print("\n❌ Failed to fetch publications")
        exit(1)

if __name__ == '__main__':
    main()

        print("\n❌ Failed to fetch publications")
        exit(1)

if __name__ == '__main__':
    main()
