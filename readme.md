# Brickshelf Gallery Downloader

This Python script downloads images from Brickshelf galleries, including all subfolders and paginated content.

## Features

- Recursively processes galleries and subfolders
- Handles paginated content (follows "Next" links)
- Downloads full-size images
- Skips already downloaded images for efficient resuming and updating
- Implements retry logic for improved reliability
- Polite to the server with built-in delays

## Requirements

- Python 3.6+
- Required Python packages:
  - requests
  - beautifulsoup4

## Installation

1. Clone this repository or download the script.
2. Install the required packages:

   pip install requests beautifulsoup4

## Usage

1. Open the script and modify the `base_url` and `start_url` variables to point to the Brickshelf gallery you want to download:

   base_url = "https://brickshelf.com"
   start_url = "/cgi-bin/gallery.cgi?m=yourusername"

2. Optionally, modify the `local_base_path` variable to change where the images will be saved:

   local_base_path = os.path.expanduser("~/Desktop/brickshelf_download")

3. Run the script:

   python brickshelf_downloader.py

## How It Works

1. The script starts at the specified `start_url` and recursively processes all subfolders.
2. For each folder, it finds all image links and downloads the full-size versions.
3. If a folder has multiple pages, the script follows the "Next" links to process all pages.
4. Before downloading an image, the script checks if it already exists locally. If it does, the download is skipped.
5. The script implements retry logic to handle transient network issues.
6. A delay of 1 second is added between requests to be respectful to the server.

## Error Handling

- The script catches and reports errors for individual image downloads and page processing.
- If an error occurs, the script will continue with the next item rather than crashing.

## Resuming Interrupted Downloads

If the script is interrupted, you can simply run it again with the same parameters. It will:
1. Process all folders and subfolders as before.
2. Skip downloading any images that already exist locally.
3. Continue downloading from where it left off.

## Limitations

- The script is designed for personal use and should be used responsibly.
- It may not work if Brickshelf significantly changes its website structure.
- Always respect the website's terms of service and robots.txt file.

## License

This project is licensed under the MIT License - see the [MIT License](https://opensource.org/licenses/MIT) page for details.

## Disclaimer

Use it responsibly and respect the copyright and terms of service of the websites you interact with. The author is not responsible for any misuse of this software or any violations of terms of service of the websites accessed by this script.