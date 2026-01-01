#!/usr/bin/env python3
"""
Automatically fetch publications from Google Scholar and update the website.
This script:
1. Fetches publications from your Google Scholar profile
2. Updates _bibliography/papers.bib with new publications
3. Generates news announcements for new papers
4. Updates publication metadata
"""

import os
import sys
import yaml
from datetime import datetime
from pathlib import Path

try:
    from scholarly import scholarly, ProxyGenerator
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.bwriter import BibTexWriter
    from bibtexparser.bibdatabase import BibDatabase
except ImportError:
    print("Error: Required packages not installed. Install with:")
    print("pip install scholarly bibtexparser pyyaml")
    sys.exit(1)


class ScholarSyncManager:
    """Manages synchronization between Google Scholar and Jekyll site"""
    
    def __init__(self, scholar_id):
        self.scholar_id = scholar_id
        self.root_dir = Path(__file__).parent.parent
        self.bib_file = self.root_dir / '_bibliography' / 'papers.bib'
        self.news_dir = self.root_dir / '_news'
        self.data_dir = self.root_dir / '_data'
        self.data_file = self.data_dir / 'publications.yml'
        
        # Ensure directories exist
        self.news_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        (self.root_dir / '_bibliography').mkdir(exist_ok=True)
        
        # Setup scholarly with proxy to avoid blocks
        try:
            pg = ProxyGenerator()
            pg.FreeProxies()
            scholarly.use_proxy(pg)
        except Exception as e:
            print(f"Warning: Could not setup proxy: {e}. Continuing without proxy...")
    
    def fetch_publications(self):
        """Fetch all publications from Google Scholar"""
        print(f"Fetching publications for Scholar ID: {self.scholar_id}")
        
        try:
            author = scholarly.search_author_id(self.scholar_id)
            author_filled = scholarly.fill(author, sections=['publications'])
            
            publications = []
            for pub in author_filled['publications']:
                try:
                    pub_filled = scholarly.fill(pub)
                    publications.append(pub_filled)
                    print(f"  ✓ Fetched: {pub_filled['bib']['title']}")
                except Exception as e:
                    print(f"  ✗ Error fetching publication: {e}")
                    continue
            
            print(f"\nSuccessfully fetched {len(publications)} publications")
            return publications
            
        except Exception as e:
            print(f"Error fetching publications: {e}")
            return []
    
    def convert_to_bibtex(self, publications):
        """Convert scholarly publications to BibTeX format"""
        bibtex_entries = []
        
        for pub in publications:
            bib = pub['bib']
            
            # Generate citation key
            first_author = bib.get('author', ['Unknown'])[0].split()[-1].lower()
            year = bib.get('pub_year', 'unknown')
            title_word = bib.get('title', 'untitled').split()[0].lower()
            cite_key = f"{first_author}{year}{title_word}"
            
            # Determine publication type
            pub_type = self._determine_pub_type(bib)
            
            # Build BibTeX entry
            entry = f"@{pub_type}{{{cite_key},\n"
            entry += f"  title={{{bib.get('title', 'Untitled')}}},\n"
            
            # Authors
            if 'author' in bib:
                authors = ' and '.join(bib['author'])
                entry += f"  author={{{authors}}},\n"
            
            # Venue
            if 'venue' in bib:
                if pub_type == 'article':
                    entry += f"  journal={{{bib['venue']}}},\n"
                else:
                    entry += f"  booktitle={{{bib['venue']}}},\n"
            
            # Year
            if 'pub_year' in bib:
                entry += f"  year={{{bib['pub_year']}}},\n"
            
            # Additional fields
            if 'citation' in bib:
                entry += f"  publisher={{{bib.get('citation', 'Unknown')}}},\n"
            
            # Add custom fields for website
            num_citations = pub.get('num_citations', 0)
            entry += f"  google_scholar_id={{{pub.get('author_pub_id', '')}}},\n"
            entry += f"  abbr={{{self._get_venue_abbr(bib.get('venue', ''))}}},\n"
            
            # Mark high-impact papers as selected
            if num_citations > 20:
                entry += f"  selected={{true}},\n"
            
            entry += "}\n"
            bibtex_entries.append(entry)
        
        return "\n".join(bibtex_entries)
    
    def _determine_pub_type(self, bib):
        """Determine publication type from bib data"""
        venue = bib.get('venue', '').lower()
        
        if any(word in venue for word in ['journal', 'transactions', 'letters']):
            return 'article'
        elif any(word in venue for word in ['conference', 'proceedings', 'workshop', 'symposium']):
            return 'inproceedings'
        else:
            return 'article'  # Default
    
    def _get_venue_abbr(self, venue):
        """Get abbreviated venue name"""
        abbr_map = {
            'International Conference on Distributed Computing Systems': 'ICDCS',
            'International Conference on Distributed Computing and Networking': 'ICDCN',
            'IEEE Network Operations and Management Symposium': 'NOMS',
            'International Conference on Mobile and Ubiquitous Systems': 'MobiQuitous',
            'Journal of Network and Systems Management': 'JNSM',
        }
        
        for full_name, abbr in abbr_map.items():
            if full_name.lower() in venue.lower():
                return abbr
        
        # Try to create abbreviation from first letters
        words = [w for w in venue.split() if len(w) > 3 and w[0].isupper()]
        if words:
            return ''.join([w[0] for w in words[:3]])
        
        return ''
    
    def update_bibliography(self, bibtex_content):
        """Update the bibliography file"""
        print("\nUpdating bibliography file...")
        
        # Read existing bib file
        existing_entries = {}
        if self.bib_file.exists():
            with open(self.bib_file, 'r') as f:
                parser = BibTexParser(common_strings=True)
                existing_db = bibtexparser.load(f, parser=parser)
                existing_entries = {entry['ID']: entry for entry in existing_db.entries}
        
        # Parse new entries
        parser = BibTexParser(common_strings=True)
        new_db = bibtexparser.loads(bibtex_content, parser=parser)
        
        # Merge (prefer existing entries to preserve manual edits)
        for entry in new_db.entries:
            if entry['ID'] not in existing_entries:
                existing_entries[entry['ID']] = entry
                print(f"  ✓ Added new publication: {entry.get('title', 'Untitled')}")
        
        # Write back
        final_db = BibDatabase()
        final_db.entries = list(existing_entries.values())
        
        writer = BibTexWriter()
        writer.indent = '  '
        
        with open(self.bib_file, 'w') as f:
            f.write("---\n---\n\n")  # Jekyll front matter
            f.write('@string{aps = {American Physical Society,}}\n\n')
            f.write(writer.write(final_db))
        
        print(f"✓ Bibliography updated: {len(final_db.entries)} total publications")
    
    def generate_news_announcements(self, publications):
        """Generate news announcements for recent publications"""
        print("\nGenerating news announcements...")
        
        # Clear existing auto-generated announcements
        self.news_dir.mkdir(exist_ok=True)
        for file in self.news_dir.glob('auto_*.md'):
            file.unlink()
        
        # Sort publications by year (most recent first)
        pubs_by_year = {}
        for pub in publications:
            year = pub['bib'].get('pub_year', 'unknown')
            if year not in pubs_by_year:
                pubs_by_year[year] = []
            pubs_by_year[year].append(pub)
        
        # Generate announcements for recent publications (last 2 years)
        current_year = datetime.now().year
        announcement_count = 0
        
        for year in sorted(pubs_by_year.keys(), reverse=True):
            if isinstance(year, str) or year < current_year - 2:
                continue
            
            for idx, pub in enumerate(pubs_by_year[year]):
                bib = pub['bib']
                title = bib.get('title', 'Untitled')
                venue = bib.get('venue', 'Unknown Venue')
                
                # Create announcement file
                file_name = f"auto_pub_{year}_{idx+1}.md"
                file_path = self.news_dir / file_name
                
                # Determine announcement date (use publication year)
                date_str = f"{year}-01-01"
                
                content = f"""---
layout: post
date: {date_str}
inline: true
related_posts: false
---

Our paper titled "{title}" has been published in {venue}.
"""
                
                with open(file_path, 'w') as f:
                    f.write(content)
                
                announcement_count += 1
                print(f"  ✓ Created announcement: {file_name}")
        
        print(f"✓ Generated {announcement_count} news announcements")
    
    def update_publications_data(self, publications):
        """Update publications metadata file"""
        print("\nUpdating publications metadata...")
        
        pub_data = {
            'last_updated': datetime.now().isoformat(),
            'total_publications': len(publications),
            'total_citations': sum(pub.get('num_citations', 0) for pub in publications),
            'h_index': self._calculate_h_index(publications),
            'recent_publications': []
        }
        
        # Add recent publications (last 3 years)
        current_year = datetime.now().year
        for pub in publications:
            year = pub['bib'].get('pub_year')
            if isinstance(year, int) and year >= current_year - 3:
                pub_data['recent_publications'].append({
                    'title': pub['bib'].get('title'),
                    'year': year,
                    'citations': pub.get('num_citations', 0),
                    'venue': pub['bib'].get('venue', '')
                })
        
        # Write YAML file
        with open(self.data_file, 'w') as f:
            yaml.dump(pub_data, f, default_flow_style=False, sort_keys=False)
        
        print(f"✓ Metadata updated: {pub_data['total_publications']} pubs, {pub_data['total_citations']} citations, h-index: {pub_data['h_index']}")
    
    def _calculate_h_index(self, publications):
        """Calculate h-index from publications"""
        citations = sorted([pub.get('num_citations', 0) for pub in publications], reverse=True)
        h_index = 0
        for i, c in enumerate(citations, 1):
            if c >= i:
                h_index = i
            else:
                break
        return h_index
    
    def sync(self):
        """Main sync function"""
        print("=" * 60)
        print("Google Scholar Publication Sync")
        print("=" * 60)
        
        # Fetch publications
        publications = self.fetch_publications()
        
        if not publications:
            print("\n⚠ No publications found. Exiting.")
            return
        
        # Convert to BibTeX
        bibtex_content = self.convert_to_bibtex(publications)
        
        # Update files
        self.update_bibliography(bibtex_content)
        self.generate_news_announcements(publications)
        self.update_publications_data(publications)
        
        print("\n" + "=" * 60)
        print("✓ Sync completed successfully!")
        print("=" * 60)


def main():
    # Get Scholar ID from environment or use default
    scholar_id = os.environ.get('SCHOLAR_ID', 'wq36gfgAAAAJ')
    
    manager = ScholarSyncManager(scholar_id)
    manager.sync()


if __name__ == '__main__':
    main()
