# CurseForge Minecraft Mod Crawler

A Python Tkinter GUI application for crawling Minecraft mods from the CurseForge API and storing them in JSON files.

## Features

- **User-Friendly GUI**: Easy-to-use tkinter interface
- **CurseForge API Integration**: Automatically fetches mod data from CurseForge
- **Data Export**: Saves mods and versions to structured JSON files
- **Progress Tracking**: Real-time progress updates and logging
- **Error Handling**: Robust error handling and user feedback
- **Statistics Display**: Shows crawling statistics and results

## Setup

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Get CurseForge API Key**:
   - Visit [CurseForge Console](https://console.curseforge.com/)
   - Create an account and generate an API key
   - Replace `YOUR_API_KEY_HERE` in the application with your actual API key

4. **Run the application**:
   ```bash
   python mod_crawler_gui.py
   ```

## Usage

1. **Enter API Key**: Input your CurseForge API key in the API Key field
2. **Configure Search**:
   - Select Minecraft version (e.g., 1.20.1)
   - Choose mod category or leave as "All"
   - Enter search term (optional)
   - Set maximum number of results
3. **Start Crawling**: Click "Start Crawling" to begin
4. **Monitor Progress**: Watch the progress bar and output log
5. **Save Results**: Data is automatically saved to `data/mods.json` and `data/versions.json`

## Output Files

The application creates a `data/` directory with two JSON files:

- **`mods.json`**: Contains mod information including:
  - Mod ID, name, summary
  - Authors and download counts
  - Creation and modification dates
  - Latest version and supported loaders

- **`versions.json`**: Contains version information including:
  - File IDs and names
  - Game version compatibility
  - Download URLs and file sizes
  - Upload dates and download counts

## API Key Setup

To get a CurseForge API key:

1. Go to https://console.curseforge.com/
2. Sign in with your CurseForge account
3. Navigate to "API Keys" section
4. Create a new API key for your application
5. Copy the key and paste it in the application

**Note**: Keep your API key secure and never commit it to version control.

## Troubleshooting

- **"No mods found"**: Check your API key and internet connection
- **API errors**: Verify your API key is valid and has proper permissions
- **Empty results**: Try adjusting search parameters or removing filters

## License

This project is open source. Feel free to modify and distribute.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
