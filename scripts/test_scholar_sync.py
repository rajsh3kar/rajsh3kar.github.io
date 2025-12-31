#!/usr/bin/env python3
"""
Quick test script to verify Google Scholar sync is working.
This is a simplified version that just fetches and displays your publications.
"""

import os
import sys

try:
    from scholarly import scholarly
except ImportError:
    print("❌ Error: 'scholarly' package not installed")
    print("\nInstall it with:")
    print("  pip install scholarly")
    sys.exit(1)

def test_scholar_fetch(scholar_id):
    """Test fetching publications from Google Scholar"""
    
    print("=" * 60)
    print("Testing Google Scholar Connection")
    print("=" * 60)
    print(f"Scholar ID: {scholar_id}\n")
    
    try:
        # Fetch author profile
        print("📡 Fetching author profile...")
        author = scholarly.search_author_id(scholar_id)
        
        print(f"✓ Found: {author.get('name', 'Unknown')}")
        print(f"  Affiliation: {author.get('affiliation', 'N/A')}")
        print(f"  Email: {author.get('email_domain', 'N/A')}")
        
        # Fill with publications
        print("\n📚 Fetching publications...")
        author_filled = scholarly.fill(author, sections=['publications'])
        
        publications = author_filled.get('publications', [])
        print(f"✓ Found {len(publications)} publications\n")
        
        # Display publications
        print("Publications List:")
        print("-" * 60)
        
        for i, pub in enumerate(publications[:10], 1):  # Show first 10
            bib = pub.get('bib', {})
            title = bib.get('title', 'Untitled')
            year = bib.get('pub_year', 'N/A')
            venue = bib.get('venue', 'N/A')
            citations = pub.get('num_citations', 0)
            
            print(f"{i}. {title}")
            print(f"   Year: {year} | Venue: {venue} | Citations: {citations}")
            print()
        
        if len(publications) > 10:
            print(f"... and {len(publications) - 10} more publications\n")
        
        # Calculate metrics
        total_citations = sum(p.get('num_citations', 0) for p in publications)
        
        # Calculate h-index
        citations_list = sorted([p.get('num_citations', 0) for p in publications], reverse=True)
        h_index = 0
        for i, c in enumerate(citations_list, 1):
            if c >= i:
                h_index = i
            else:
                break
        
        print("=" * 60)
        print("Summary Statistics")
        print("=" * 60)
        print(f"Total Publications: {len(publications)}")
        print(f"Total Citations: {total_citations}")
        print(f"H-Index: {h_index}")
        print("=" * 60)
        
        print("\n✓ Test completed successfully!")
        print("\nNext steps:")
        print("1. Run the full sync: python scripts/fetch_scholar_publications.py")
        print("2. Enable GitHub Actions for automatic daily updates")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify the Scholar ID is correct")
        print("3. Try again in a few minutes (rate limiting)")
        return False

if __name__ == '__main__':
    scholar_id = os.environ.get('SCHOLAR_ID', 'wq36gfgAAAAJ')
    test_scholar_fetch(scholar_id)
