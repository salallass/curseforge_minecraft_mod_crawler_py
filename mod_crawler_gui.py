import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
import os
from datetime import datetime
import threading
import shutil
import random
import string
import html

class MinecraftModCrawler:
    def generate_cache_filename(self, mod_name, mod_id=None, extension='html'):
        """Generate a cache filename in format: [random]_[modid]_modname.extension"""
        # Clean the mod name to be filesystem-safe
        safe_name = ''.join(c if c.isalnum() or c in ' -_' else '_' for c in str(mod_name))
        safe_name = safe_name.replace(' ', '_').lower()
        
        # Generate random prefix and include mod ID for better identification
        random_prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        mod_id_part = f"{mod_id}_" if mod_id is not None else ""
        
        return f"{random_prefix}_{mod_id_part}{safe_name}.{extension}"
        
    def ensure_data_directories(self):
        """Ensure all required data directories exist"""
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        os.makedirs(data_dir, exist_ok=True)
        
        # Create descriptions directory for HTML files
        desc_dir = os.path.join(data_dir, "descriptions")
        os.makedirs(desc_dir, exist_ok=True)
        
        return desc_dir
        
    def save_mod_cache(self, mod_data):
        """Save mod data to cache including description HTML and icon"""
        if not mod_data or 'id' not in mod_data:
            return {'html_path': None, 'icon_path': None}
            
        mod_id = mod_data.get('id')
        mod_name = mod_data.get('name', f'mod_{mod_id}')
        cache_data = {
            'html_path': None,
            'icon_path': None
        }
        
        # Ensure data directories exist
        desc_dir = self.ensure_data_directories()
        
        # Save description as HTML
        if 'description' in mod_data:
            try:
                # Generate HTML content with improved styling
                html_content = f"""<!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>{html.escape(mod_data.get('name', 'Mod Description'))}</title>
                    <style>
                        body {{ 
                            font-family: 'Segoe UI', Arial, sans-serif;
                            line-height: 1.8;
                            max-width: 900px;
                            margin: 0 auto;
                            padding: 25px;
                            color: #333;
                            background-color: #f9f9f9;
                        }}
                        .container {{
                            background: white;
                            border-radius: 8px;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                            padding: 30px;
                            margin-top: 20px;
                        }}
                        h1 {{ 
                            color: #2c3e50;
                            border-bottom: 2px solid #eee;
                            padding-bottom: 10px;
                            margin-top: 0;
                        }}
                        .mod-header {{
                            display: flex;
                            align-items: center;
                            margin-bottom: 20px;
                            gap: 20px;
                        }}
                        .mod-icon {{
                            width: 80px;
                            height: 80px;
                            object-fit: contain;
                            border-radius: 8px;
                            border: 1px solid #eee;
                        }}
                        .mod-meta {{ 
                            color: #555;
                            margin: 15px 0;
                            line-height: 1.6;
                        }}
                        .meta-row {{
                            margin: 8px 0;
                        }}
                        .meta-label {{
                            font-weight: bold;
                            color: #2c3e50;
                            display: inline-block;
                            min-width: 100px;
                        }}
                        .description {{
                            margin-top: 25px;
                            line-height: 1.8;
                        }}
                        a {{
                            color: #3498db;
                            text-decoration: none;
                        }}
                        a:hover {{
                            text-decoration: underline;
                        }}
                        .categories {{
                            margin: 15px 0;
                            display: flex;
                            flex-wrap: wrap;
                            gap: 8px;
                        }}
                        .category {{
                            background: #e8f4fd;
                            color: #2c6ecb;
                            padding: 4px 12px;
                            border-radius: 15px;
                            font-size: 0.85em;
                        }}
                        @media (max-width: 768px) {{
                            .mod-header {{
                                flex-direction: column;
                                align-items: flex-start;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="mod-header">
                            <img src="{os.path.basename(self.save_mod_icon(mod_data)) if mod_data.get('logo') else ''}" 
                                 class="mod-icon" 
                                 alt="{html.escape(mod_data.get('name', 'Mod Icon'))}" 
                                 onerror="this.style.display='none'"
                                 id="modIcon">
                            <div>
                                <h1>{html.escape(mod_data.get('name', 'Mod'))}</h1>
                                <div class="mod-meta">
                                    <div class="meta-row">
                                        <span class="meta-label">Author:</span>
                                        {', '.join([html.escape(a.get('name', 'Unknown')) for a in mod_data.get('authors', [{}])])}
                                    </div>
                                    <div class="meta-row">
                                        <span class="meta-label">Downloads:</span>
                                        {mod_data.get('downloadCount', 0):,}
                                    </div>
                                    <div class="meta-row">
                                        <span class="meta-label">Last Updated:</span>
                                        {datetime.fromisoformat(mod_data.get('dateModified', '')).strftime('%Y-%m-%d %H:%M') if mod_data.get('dateModified') else 'N/A'}
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        {f'<div class="categories">' + ''.join([f'<span class="category">{cat.get("name", "")}</span>' for cat in mod_data.get('categories', [])]) + '</div>' if mod_data.get('categories') else ''}
                        
                        <div class="description">
                            {mod_data.get('description', 'No description available.')}
                        </div>
                        
                        <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #eee;">
                            <a href="{mod_data.get('links', {}).get('websiteUrl', '#')}" target="_blank">
                                View on CurseForge ↗
                            </a>
                        </div>
                    </div>
                    
                    <script>
                        // Make sure icon path is relative to the HTML file
                        document.addEventListener('DOMContentLoaded', function() {{
                            const icon = document.getElementById('modIcon');
                            if (icon && icon.src.includes('/')) {{
                                icon.src = icon.src.split('/').pop();
                            }}
                        }});
                    </script>
                </body>
                </html>
                """
                
                # Generate filename and save HTML in data/descriptions
                html_filename = self.generate_cache_filename(mod_name, mod_id, 'html')
                html_path = os.path.join(desc_dir, html_filename)
                
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                cache_data['html_path'] = html_path
                
            except Exception as e:
                self.log_message(f"Error saving mod HTML cache: {e}")
        
        # Save icon if available (still in cache directory)
        if 'logo' in mod_data and mod_data['logo'] and 'url' in mod_data['logo']:
            try:
                icon_url = mod_data['logo']['url']
                icon_ext = os.path.splitext(icon_url)[1].split('?')[0] or '.png'
                icon_filename = self.generate_cache_filename(mod_name, mod_id, icon_ext.lstrip('.'))
                icon_path = os.path.join(self.cache_dir, "icons", icon_filename)
                
                response = requests.get(icon_url, stream=True)
                response.raise_for_status()
                
                with open(icon_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                
                cache_data['icon_path'] = icon_path
                
            except Exception as e:
                self.log_message(f"Error saving mod icon: {e}")
        
        # Update cache size and return paths
        self.update_cache_size_display()
        return cache_data

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CurseForge Minecraft Mod Crawler")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # CurseForge API configuration
        self.api_base = "https://api.curseforge.com/v1"
        self.api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key

        # Create GUI elements
        self.setup_gui()

        # Load existing data
        self.load_existing_data()

    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="CurseForge Minecraft Mod Crawler",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # API Key input
        ttk.Label(main_frame, text="API Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(main_frame, width=50, show="*")
        self.api_key_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        self.api_key_entry.insert(0, self.api_key)

        # Search parameters
        search_frame = ttk.LabelFrame(main_frame, text="Search Parameters", padding="10")
        search_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Game version
        ttk.Label(search_frame, text="Minecraft Version:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.version_var = tk.StringVar(value="1.20.1")
        version_combo = ttk.Combobox(search_frame, textvariable=self.version_var,
                                    values=["1.19.4", "1.20.1", "1.20.2", "1.20.4", "1.21.1"])
        version_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # Mod type
        ttk.Label(search_frame, text="Mod Type:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        self.mod_type_var = tk.StringVar(value="Mod")
        mod_type_combo = ttk.Combobox(search_frame, textvariable=self.mod_type_var,
                                    values=["Mod", "Shader", "Datapack", "Resource Pack", "World", "Modpack"])
        mod_type_combo.grid(row=0, column=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))

        # Mod category
        ttk.Label(search_frame, text="Mod Category:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar(value="All")
        category_combo = ttk.Combobox(search_frame, textvariable=self.category_var,
                                     values=["All", "Adventure", "API", "Cosmetic", "Decoration",
                                            "Food", "Library", "Magic", "Optimization", "Technology"])
        category_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Repeat crawl settings
        ttk.Label(search_frame, text="Repeat Crawl:").grid(row=1, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Number of repeats
        ttk.Label(search_frame, text="Times:").grid(row=1, column=3, sticky=tk.W, pady=5, padx=(10, 0))
        self.repeat_count_var = tk.IntVar(value=1)
        repeat_spin = ttk.Spinbox(search_frame, from_=1, to=100, width=5, textvariable=self.repeat_count_var)
        repeat_spin.grid(row=1, column=4, sticky=tk.W, pady=5, padx=(0, 10))
        
        # Delay between crawls (in minutes)
        ttk.Label(search_frame, text="Delay (min):").grid(row=1, column=5, sticky=tk.W, pady=5, padx=(10, 0))
        self.repeat_delay_var = tk.IntVar(value=5)
        delay_spin = ttk.Spinbox(search_frame, from_=1, to=1440, width=5, textvariable=self.repeat_delay_var)
        delay_spin.grid(row=1, column=6, sticky=tk.W, pady=5, padx=(0, 10))

        # Search term
        ttk.Label(search_frame, text="Search Term (optional):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        # Number of results
        ttk.Label(search_frame, text="Max Results:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.max_results_var = tk.StringVar(value="50")
        max_results_spinbox = ttk.Spinbox(search_frame, from_=10, to=200, increment=10,
                                         textvariable=self.max_results_var, width=10)
        max_results_spinbox.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        # Control buttons
        self.crawl_button = ttk.Button(buttons_frame, text="Start Crawling",
                                      command=self.start_crawling, style="Accent.TButton")
        self.crawl_button.grid(row=0, column=0, padx=(0, 10))

        ttk.Button(buttons_frame, text="Stop", command=self.stop_crawling).grid(row=0, column=1, padx=(0, 10))

        ttk.Button(buttons_frame, text="Clear Output", command=self.clear_output).grid(row=0, column=2, padx=(0, 10))

        ttk.Button(buttons_frame, text="Save Data", command=self.save_data).grid(row=0, column=3, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="Clear Data", command=self.clear_data).grid(row=0, column=4)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=5, column=0, columnspan=2, pady=(5, 0))

        # Output text area
        output_frame = ttk.LabelFrame(main_frame, text="Output Log", padding="10")
        output_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, wrap=tk.WORD)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure output frame
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        # Stats labels
        self.stats_vars = {
            'total_mods': tk.StringVar(value="Total Mods: 0"),
            'total_versions': tk.StringVar(value="Total Versions: 0"),
            'last_updated': tk.StringVar(value="Last Updated: Never"),
            'crawl_time': tk.StringVar(value="Crawl Time: --:--:--"),
            'cache_size': tk.StringVar(value="Cache: 0 B")
        }

        # Arrange stats in a grid
        ttk.Label(stats_frame, textvariable=self.stats_vars['total_mods']).grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        ttk.Label(stats_frame, textvariable=self.stats_vars['total_versions']).grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)
        ttk.Label(stats_frame, textvariable=self.stats_vars['last_updated']).grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
        ttk.Label(stats_frame, textvariable=self.stats_vars['crawl_time'], font=('TkDefaultFont', 9, 'bold')).grid(row=1, column=1, sticky=tk.W, pady=2, padx=5)
        ttk.Label(stats_frame, textvariable=self.stats_vars['cache_size']).grid(row=2, column=0, sticky=tk.W, pady=2, padx=5)

        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data", command=self.load_existing_data)
        file_menu.add_command(label="Save Data", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Initialize data structures
        self.mods_data = []
        self.versions_data = []
        self.crawling = False
        self.crawl_start_time = None
        self.crawl_end_time = None
        self.crawl_duration = None
        self.current_repeat = 0
        self.total_repeats = 1
        self.repeat_timer = None
        
        # Create cache directory structure if it doesn't exist
        self.cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache')
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)
            os.makedirs(os.path.join(self.cache_dir, "icons"), exist_ok=True)
            os.makedirs(os.path.join(self.cache_dir, "media"), exist_ok=True)
            os.makedirs(os.path.join(self.cache_dir, "descriptions"), exist_ok=True)
            self.log_message(f"Created cache directory structure at: {self.cache_dir}")
            
        # Initial cache size update
        self.update_cache_size_display()
        
        # Load existing data if any
        self.load_existing_data()

    def log_message(self, message):
        """Add message to output log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_text.see(tk.END)
        self.root.update()

    def update_stats(self):
        """Update statistics display"""
        self.stats_vars['total_mods'].set(f"Total Mods: {len(self.mods_data)}")
        self.stats_vars['total_versions'].set(f"Total Versions: {len(self.versions_data)}")
        self.stats_vars['last_updated'].set(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")
        
        # Update crawl time if available
        if self.crawl_duration:
            self.stats_vars['crawl_time'].set(f"Crawl Time: {self.format_duration(self.crawl_duration)}")
        elif self.crawl_start_time and self.crawling:
            duration = datetime.now() - self.crawl_start_time
            self.stats_vars['crawl_time'].set(f"Crawling: {self.format_duration(duration)}")
        else:
            self.stats_vars['crawl_time'].set("Crawl Time: --:--:--")
            
        # Update cache size
        self.update_cache_size_display()

    def get_curseforge_headers(self):
        """Get headers for CurseForge API requests"""
        return {
            'Accept': 'application/json',
            'x-api-key': self.api_key_entry.get()
        }

    def get_mod_type_id(self, mod_type):
        """Get the CurseForge class ID for a mod type"""
        mod_types = {
            'Mod': 6,           # Mods
            'Shader': 6552,     # Shaders
            'Datapack': 17,     # Data Packs
            'Resource Pack': 12, # Resource Packs
            'World': 17,        # Worlds
            'Modpack': 4471     # Modpacks
        }
        return mod_types.get(mod_type, 6)  # Default to Mod

    def search_mods(self):
        """Search for mods using CurseForge API"""
        try:
            # Build search parameters
            params = {
                'gameId': 432,  # Minecraft game ID
                'classId': self.get_mod_type_id(self.mod_type_var.get()),
                'sortField': 2,  # Sort by popularity
                'sortOrder': 'desc',
                'pageSize': int(self.max_results_var.get()),
                'index': 0
            }

            # Add version filter if specified
            if self.version_var.get() != "All":
                params['gameVersion'] = self.version_var.get()

            # Add category filter (this would need category ID mapping)
            # For now, we'll use search term for filtering
            if self.search_var.get().strip():
                params['searchFilter'] = self.search_var.get()

            url = f"{self.api_base}/mods/search"
            response = requests.get(url, headers=self.get_curseforge_headers(), params=params)
            response.raise_for_status()

            data = response.json()
            return data.get('data', [])

        except requests.exceptions.RequestException as e:
            self.log_message(f"Error searching mods: {str(e)}")
            return []
        except Exception as e:
            self.log_message(f"Unexpected error: {str(e)}")
            return []

    def get_mod_versions(self, mod_id):
        """Get versions for a specific mod"""
        try:
            url = f"{self.api_base}/mods/{mod_id}/files"
            params = {'pageSize': 100}  # Get more versions

            response = requests.get(url, headers=self.get_curseforge_headers(), params=params)
            response.raise_for_status()

            data = response.json()
            return data.get('data', [])

        except requests.exceptions.RequestException as e:
            self.log_message(f"Error getting versions for mod {mod_id}: {str(e)}")
            return []
        except Exception as e:
            self.log_message(f"Unexpected error getting versions: {str(e)}")
            return []

    def format_duration(self, duration):
        """Format a timedelta as HH:MM:SS"""
        if not duration:
            return "00:00:00"
            
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_cache_size(self):
        """Calculate total size of cache directory in bytes"""
        total_size = 0
        for dirpath, _, filenames in os.walk(self.cache_dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total_size += os.path.getsize(fp)
                except (OSError, AttributeError):
                    pass
        return total_size
        
    def format_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0 B"
        size_names = ("B", "KB", "MB", "GB", "TB")
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
        
    def update_cache_size_display(self):
        """Update the cache size display in the UI"""
        try:
            size_bytes = self.get_cache_size()
            self.stats_vars['cache_size'].set(f"Cache: {self.format_size(size_bytes)}")
        except Exception as e:
            self.log_message(f"Error calculating cache size: {e}")
            self.stats_vars['cache_size'].set("Cache: Error")

    def start_crawling(self):
        """Start the crawling process in a separate thread"""
        if self.crawling:
            messagebox.showwarning("Warning", "Crawling is already in progress!")
            return

        # Validate API key
        if not self.api_key_entry.get().strip() or self.api_key_entry.get() == "YOUR_API_KEY_HERE":
            messagebox.showerror("Error", "Please enter a valid CurseForge API key!")
            return

        self.crawling = True
        self.crawl_start_time = datetime.now()
        self.crawl_end_time = None
        self.crawl_duration = None
        self.crawl_button.config(state=tk.DISABLED, text="Crawling...")
        self.progress_var.set(0)
        
        # Start a timer to update the crawl time display
        def update_timer():
            if self.crawling and self.crawl_start_time:
                duration = datetime.now() - self.crawl_start_time
                self.stats_vars['crawl_time'].set(f"Crawling: {self.format_duration(duration)}")
                self.root.after(1000, update_timer)  # Update every second
        
        self.root.after(1000, update_timer)

        # Start crawling in separate thread
        crawl_thread = threading.Thread(target=self.crawl_mods, daemon=True)
        crawl_thread.start()

    def stop_crawling(self):
        """Stop the crawling process"""
        if self.crawling and self.crawl_start_time:
            self.crawl_end_time = datetime.now()
            self.crawl_duration = self.crawl_end_time - self.crawl_start_time
            self.log_message(f"Crawling stopped after {self.format_duration(self.crawl_duration)}")
        
        # Cancel any pending repeat
        if self.repeat_timer and self.repeat_timer.is_alive():
            self.repeat_timer.cancel()
            self.log_message("Cancelled pending repeat crawls")
        
        self.crawling = False
        self.current_repeat = 0
        self.crawl_button.config(state=tk.NORMAL, text="Start Crawling")
        self.status_var.set("Crawling stopped")
        self.update_stats()  # Update stats to show final crawl time

    def schedule_next_crawl(self):
        """Schedule the next crawl if repeats are configured"""
        self.current_repeat += 1
        
        if self.current_repeat < self.total_repeats:
            delay_minutes = self.repeat_delay_var.get()
            self.log_message(f"Next crawl in {delay_minutes} minutes... (Repeat {self.current_repeat + 1}/{self.total_repeats})")
            
            # Schedule the next crawl
            self.repeat_timer = threading.Timer(
                delay_minutes * 60,  # Convert minutes to seconds
                self.start_crawling_thread
            )
            self.repeat_timer.daemon = True
            self.repeat_timer.start()
        else:
            self.log_message("All crawls completed!")
            self.status_var.set("All crawls completed!")
            self.crawling = False
            self.crawl_button.config(state=tk.NORMAL, text="Start Crawling")

    def start_crawling_thread(self):
        """Wrapper to start crawling in the main thread"""
        if not self.root.winfo_exists():
            return
            
        self.root.after(0, self.crawl_mods)

    def crawl_mods(self):
        """Main crawling function"""
        try:
            if self.current_repeat == 0:
                # First run, initialize
                self.total_repeats = self.repeat_count_var.get()
                self.log_message("=" * 50)
                self.log_message(f"Starting crawl {self.current_repeat + 1}/{self.total_repeats}")
                self.log_message(f"Mod Type: {self.mod_type_var.get()}")
                self.log_message("=" * 50)
            else:
                self.log_message(f"\n{'=' * 50}")
                self.log_message(f"Starting crawl {self.current_repeat + 1}/{self.total_repeats}")
                self.log_message(f"Mod Type: {self.mod_type_var.get()}")
                self.log_message(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.log_message("=" * 50)
                
            self.status_var.set(f"Crawling {self.current_repeat + 1}/{self.total_repeats} - Searching for {self.mod_type_var.get().lower()}s...")

            # Search for mods
            mods = self.search_mods()
            if not mods:
                self.log_message("No mods found!")
                return

            self.log_message(f"Found {len(mods)} mods")
            self.progress_var.set(10)

            total_mods = len(mods)
            processed = 0

            # Process each mod
            for mod in mods:
                if not self.crawling:
                    break

                try:
                    # Extract mod information
                    mod_id = mod.get('id')
                    mod_name = mod.get('name', 'Unknown')
                    
                    # Download and cache mod media
                    icon_url = mod.get('logo', {}).get('url') if mod.get('logo') else None
                    media_data = {}
                    
                    # Download icon in background
                    if icon_url:
                        self.download_icon(mod_id, icon_url)
                    
                    # Download other media in background
                    if 'screenshots' in mod or 'videos' in mod:
                        media_data = self.download_mod_media(mod_id, mod)
                    
                    mod_info = {
                        'id': mod_id,
                        'name': mod_name,
                        'summary': mod.get('summary', ''),
                        'authors': [author.get('name', '') for author in mod.get('authors', [])],
                        'download_count': mod.get('downloadCount', 0),
                        'date_created': mod.get('dateCreated', ''),
                        'date_modified': mod.get('dateModified', ''),
                        'latest_version': mod.get('latestFiles', [{}])[0].get('displayCategories', [''])[0] if mod.get('latestFiles') else '',
                        'mod_loaders': mod.get('modLoaders', []),
                        'game_versions': mod.get('latestFilesIndexes', [{}])[0].get('gameVersion', []) if mod.get('latestFilesIndexes') else [],
                        'icon_url': icon_url,
                        'icon_path': os.path.join('icons', f"{mod_id}.png") if icon_url else None,
                        'media': media_data
                    }

                    self.mods_data.append(mod_info)

                    # Get versions for this mod
                    self.status_var.set(f"Getting versions for {mod.get('name', 'Unknown')}...")
                    self.root.update()

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

                    processed += 1
                    progress = 10 + (processed / total_mods) * 90
                    self.progress_var.set(progress)

                    self.log_message(f"Processed {processed}/{total_mods}: {mod.get('name', 'Unknown')}")

                except Exception as e:
                    self.log_message(f"Error processing mod {mod.get('id', 'unknown')}: {str(e)}")
                    continue

            # Update crawl time
            self.crawl_end_time = datetime.now()
            self.crawl_duration = self.crawl_end_time - self.crawl_start_time
            
            # Update statistics and save
            self.update_stats()
            self.save_data()

            self.log_message("Crawling completed successfully!")
            self.log_message(f"Total crawl time: {self.format_duration(self.crawl_duration)}")
            
            if self.current_repeat < self.total_repeats - 1:
                self.status_var.set(f"Crawl {self.current_repeat + 1}/{self.total_repeats} completed - Preparing next crawl...")
                # Schedule next crawl
                self.schedule_next_crawl()
            else:
                self.status_var.set(f"Completed {self.total_repeats} crawls!")
                self.log_message(f"Completed all {self.total_repeats} crawls!")
                self.crawling = False
                self.crawl_button.config(state=tk.NORMAL, text="Start Crawling")

        except Exception as e:
            self.log_message(f"Critical error during crawling: {str(e)}")
            self.status_var.set("Error occurred")

        finally:
            self.crawling = False
            self.crawl_button.config(state=tk.NORMAL, text="Start Crawling")

    def save_data(self):
        """Save data to JSON files"""
        try:
            # Create data directory if it doesn't exist
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                
            # Prepare metadata
            metadata = {
                'last_updated': datetime.now().isoformat(),
                'total_mods': len(self.mods_data),
                'total_versions': len(self.versions_data),
                'crawl_duration_seconds': self.crawl_duration.total_seconds() if self.crawl_duration else 0,
                'crawl_duration': str(self.crawl_duration) if self.crawl_duration else None,
                'crawl_start': self.crawl_start_time.isoformat() if self.crawl_start_time else None,
                'crawl_end': self.crawl_end_time.isoformat() if self.crawl_end_time else None
            }
            
            # Save mods data with metadata
            mods_file = os.path.join(data_dir, "mods.json")
            mods_data = {
                'metadata': metadata,
                'mods': self.mods_data
            }
            with open(mods_file, 'w', encoding='utf-8') as f:
                json.dump(mods_data, f, indent=2, ensure_ascii=False)

            # Save versions data
            versions_file = os.path.join(data_dir, "versions.json")
            with open(versions_file, 'w', encoding='utf-8') as f:
                json.dump(self.versions_data, f, indent=2, ensure_ascii=False)

            self.log_message(f"Data saved to {mods_file} and {versions_file}")
            messagebox.showinfo("Success", "Data saved successfully!")

        except Exception as e:
            self.log_message(f"Error saving data: {str(e)}")
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    def load_existing_data(self):
        """Load existing data from JSON files"""
        try:
            data_dir = "data"
            mods_file = os.path.join(data_dir, "mods.json")
            versions_file = os.path.join(data_dir, "versions.json")

            if os.path.exists(mods_file):
                with open(mods_file, 'r', encoding='utf-8') as f:
                    mods_data = json.load(f)
                    
                # Handle both old and new format
                if isinstance(mods_data, dict) and 'mods' in mods_data:
                    # New format with metadata
                    self.mods_data = mods_data.get('mods', [])
                    metadata = mods_data.get('metadata', {})
                    
                    # Load crawl time if available
                    if 'crawl_start' in metadata and 'crawl_end' in metadata:
                        try:
                            self.crawl_start_time = datetime.fromisoformat(metadata['crawl_start'])
                            self.crawl_end_time = datetime.fromisoformat(metadata['crawl_end'])
                            if self.crawl_start_time and self.crawl_end_time:
                                self.crawl_duration = self.crawl_end_time - self.crawl_start_time
                                self.log_message(f"Previous crawl took {self.format_duration(self.crawl_duration)}")
                        except (ValueError, TypeError) as e:
                            self.log_message(f"Error parsing crawl time: {e}")
                else:
                    # Old format (list of mods)
                    self.mods_data = mods_data
                    
                self.log_message(f"Loaded {len(self.mods_data)} mods from {mods_file}")

            if os.path.exists(versions_file):
                with open(versions_file, 'r', encoding='utf-8') as f:
                    self.versions_data = json.load(f)
                self.log_message(f"Loaded {len(self.versions_data)} versions from {versions_file}")

            self.update_stats()

        except Exception as e:
            self.log_message(f"Error loading existing data: {str(e)}")

    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
        
    def clear_data(self):
        """Clear all mods and versions data"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all mods and versions data? This will delete all cached media and cannot be undone."):
            self.mods_data = []
            self.versions_data = []
            
            # Clear cache directory but keep the structure
            if os.path.exists(self.cache_dir):
                import shutil
                # Remove all files and directories except the cache directory itself
                for item in os.listdir(self.cache_dir):
                    item_path = os.path.join(self.cache_dir, item)
                    try:
                        if os.path.isfile(item_path):
                            os.unlink(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except Exception as e:
                        self.log_message(f"Error deleting {item_path}: {e}")
                
                # Recreate required directories
                os.makedirs(os.path.join(self.cache_dir, "icons"), exist_ok=True)
                os.makedirs(os.path.join(self.cache_dir, "media"), exist_ok=True)
                
                self.log_message("Cleared all cached data and media")
            
            # Clear data files
            data_dir = "data"
            if os.path.exists(data_dir):
                mods_file = os.path.join(data_dir, "mods.json")
                versions_file = os.path.join(data_dir, "versions.json")
                
                if os.path.exists(mods_file):
                    os.remove(mods_file)
                if os.path.exists(versions_file):
                    os.remove(versions_file)
                
                self.log_message("Cleared mods and versions data")
            
            self.update_stats()
            self.log_message("All data has been cleared")

    def download_media(self, url, file_path):
        """Download and save a media file"""
        try:
            if not url:
                return False
                
            # Skip if already cached
            if os.path.exists(file_path):
                return True
                
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return True
            
        except Exception as e:
            self.log_message(f"Error downloading media from {url}: {str(e)}")
            return False

    def download_icon(self, mod_id, icon_url):
        """Download and cache mod icon"""
        if not icon_url:
            return None
            
        icon_path = os.path.join(self.cache_dir, "icons", f"{mod_id}.png")
        if self.download_media(icon_url, icon_path):
            self.log_message(f"Cached icon for mod ID {mod_id}")
            return icon_path
        return None
        
    def download_mod_media(self, mod_id, mod_data):
        """Download and cache all media for a mod"""
        # Create media directories
        media_base = os.path.join(self.cache_dir, "media", str(mod_id))
        screenshots_dir = os.path.join(media_base, "screenshots")
        videos_dir = os.path.join(media_base, "videos")
        
        os.makedirs(screenshots_dir, exist_ok=True)
        os.makedirs(videos_dir, exist_ok=True)
        
        # Download screenshots
        screenshots = mod_data.get('screenshots', [])
        for i, screenshot in enumerate(screenshots, 1):
            if 'url' in screenshot:
                ext = os.path.splitext(screenshot['url'])[1] or '.png'
                screenshot_path = os.path.join(screenshots_dir, f"{i}{ext}")
                self.download_media(screenshot['url'], screenshot_path)
        
        # Download videos
        videos = mod_data.get('videos', [])
        for i, video in enumerate(videos, 1):
            if 'url' in video:
                ext = os.path.splitext(video['url'])[1] or '.mp4'
                video_path = os.path.join(videos_dir, f"{i}{ext}")
                self.download_media(video['url'], video_path)
        
        # Return paths to the first screenshot and video if available
        first_screenshot = None
        first_video = None
        
        if screenshots and 'url' in screenshots[0]:
            ext = os.path.splitext(screenshots[0]['url'])[1] or '.png'
            first_screenshot = os.path.join("screenshots", f"1{ext}")
            
        if videos and 'url' in videos[0]:
            ext = os.path.splitext(videos[0]['url'])[1] or '.mp4'
            first_video = os.path.join("videos", f"1{ext}")
            
        return {
            'screenshots': [os.path.join("screenshots", f) for f in os.listdir(screenshots_dir)] 
                          if os.path.exists(screenshots_dir) else [],
            'videos': [os.path.join("videos", f) for f in os.listdir(videos_dir)] 
                     if os.path.exists(videos_dir) else [],
            'first_screenshot': first_screenshot,
            'first_video': first_video
        }

    def show_about(self):
        """Show about dialog"""
        about_text = """CurseForge Minecraft Mod Crawler

A tkinter application for crawling Minecraft mods from CurseForge API.

Features:
- Search and crawl Minecraft mods
- Extract mod information and versions
- Save data to JSON files
- User-friendly GUI interface

Note: You need a valid CurseForge API key to use this application.
Get one from: https://console.curseforge.com/"""

        messagebox.showinfo("About", about_text)

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MinecraftModCrawler()
    app.run()
