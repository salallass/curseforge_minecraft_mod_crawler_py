#!/usr/bin/env python3
"""
CurseForge Minecraft Mod Crawler Launcher
"""

import sys
import os
from mod_crawler_gui import MinecraftModCrawler

def main():
    """Main entry point"""
    try:
        print("Starting CurseForge Minecraft Mod Crawler...")
        print("Make sure you have a valid API key configured in the application.")
        print("Check README.md for setup instructions.")
        print()

        app = MinecraftModCrawler()
        app.run()

    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
