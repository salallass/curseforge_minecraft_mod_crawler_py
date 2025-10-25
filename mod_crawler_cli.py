#!/usr/bin/env python3
"""
CurseForge Minecraft Mod Crawler - Command Line Version
"""

import requests
import json
import os
import argparse
import sys
from datetime import datetime

class ModCrawlerCLI:
    def __init__(self):
        self.api_base = "https://api.curseforge.com/v1"
        self.api_key = "$2a$10$eT.3cqWbb0jqmLAeLiYBwuZdVXGFZAQ0ImT8rJs2vWBu7U0CR43pq"
        self.mods_data = []
        self.versions_data = []

    def load_api_key(self):
        """Load API key from environment or config file"""
        # Try environment variable first
        api_key = os.getenv('CURSEFORGE_API_KEY')
        if api_key:
            self.api_key = api_key
            return

        # Try config file
        config_file = 'config.json'
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.api_key = config.get('api_key')
            except:
                pass

        if not self.api_key:
            print("ERROR: No API key found!")
            print("Set CURSEFORGE_API_KEY environment variable or create config.json")
            sys.exit(1)

    def get_headers(self):
        """Get headers for API requests"""
        return {
            'Accept': 'application/json',
            'x-api-key': self.api_key
        }

    def search_mods(self, game_version="1.20.1", category="All", search_term="", max_results=50):
        """Search for mods"""
        params = {
            'gameId': 432,  # Minecraft
            'sortField': 2,  # Popularity
            'sortOrder': 'desc',
            'pageSize': max_results,
            'index': 0
        }

        if game_version != "All":
            params['gameVersion'] = game_version

        if search_term.strip():
            params['searchFilter'] = search_term

        url = f"{self.api_base}/mods/search"

        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            print(f"Error searching mods: {e}")
            return []

    def get_mod_versions(self, mod_id):
        """Get versions for a mod"""
        url = f"{self.api_base}/mods/{mod_id}/files"
        params = {'pageSize': 100}

        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            print(f"Error getting versions for mod {mod_id}: {e}")
            return []

    def save_data(self, output_dir="data"):
        """Save data to JSON files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save mods
        mods_file = os.path.join(output_dir, "mods.json")
        with open(mods_file, 'w', encoding='utf-8') as f:
            json.dump(self.mods_data, f, indent=2, ensure_ascii=False)

        # Save versions
        versions_file = os.path.join(output_dir, "versions.json")
        with open(versions_file, 'w', encoding='utf-8') as f:
            json.dump(self.versions_data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(self.mods_data)} mods to {mods_file}")
        print(f"Saved {len(self.versions_data)} versions to {versions_file}")

    def crawl(self, game_version="1.20.1", category="All", search_term="", max_results=50):
        """Main crawling function"""
        print(f"Starting crawl - Version: {game_version}, Max results: {max_results}")
        print("=" * 50)

        # Search for mods
        mods = self.search_mods(game_version, category, search_term, max_results)
        if not mods:
            print("No mods found!")
            return

        print(f"Found {len(mods)} mods")

        for i, mod in enumerate(mods, 1):
            print(f"Processing {i}/{len(mods)}: {mod.get('name', 'Unknown')}")

            # Extract mod info
            mod_info = {
                'id': mod.get('id'),
                'name': mod.get('name', 'Unknown'),
                'summary': mod.get('summary', ''),
                'authors': [author.get('name', '') for author in mod.get('authors', [])],
                'download_count': mod.get('downloadCount', 0),
                'date_created': mod.get('dateCreated', ''),
                'date_modified': mod.get('dateModified', ''),
                'mod_loaders': mod.get('modLoaders', []),
                'game_versions': mod.get('latestFilesIndexes', [{}])[0].get('gameVersion', []) if mod.get('latestFilesIndexes') else []
            }
            self.mods_data.append(mod_info)

            # Get versions
            versions = self.get_mod_versions(mod.get('id'))
            for version in versions:
                version_info = {
                    'mod_id': mod.get('id'),
                    'mod_name': mod.get('name', 'Unknown'),
                    'file_id': version.get('id'),
                    'file_name': version.get('fileName', ''),
                    'display_categories': [cat.get('name', '') for cat in version.get('displayCategories', [])],
                    'download_count': version.get('downloadCount', 0),
                    'file_size': version.get('fileLength', 0),
                    'game_versions': version.get('gameVersions', []),
                    'upload_date': version.get('fileDate', ''),
                    'download_url': version.get('downloadUrl', '')
                }
                self.versions_data.append(version_info)

        print("=" * 50)
        print(f"Crawling completed! Found {len(self.mods_data)} mods with {len(self.versions_data)} versions")

        # Save data
        self.save_data()

def main():
    parser = argparse.ArgumentParser(description="CurseForge Minecraft Mod Crawler")
    parser.add_argument('--version', default='1.20.1', help='Minecraft version (default: 1.20.1)')
    parser.add_argument('--search', default='', help='Search term')
    parser.add_argument('--max-results', type=int, default=50, help='Maximum results (default: 50)')
    parser.add_argument('--output', default='data', help='Output directory (default: data)')

    args = parser.parse_args()

    crawler = ModCrawlerCLI()
    crawler.load_api_key()
    crawler.crawl(args.version, "All", args.search, args.max_results)

if __name__ == "__main__":
    main()
