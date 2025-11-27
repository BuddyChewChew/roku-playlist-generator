import requests
import json
import gzip
import logging
from io import BytesIO

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# --- Updated Global Variables ---
def generate_roku_playlist(sort="chno"):
    """Generates M3U playlist for Roku."""
    
    # Updated URL pointing to the GZIP file on GitHub
    ROKU_URL = "https://github.com/matthuisman/i.mjh.nz/raw/refs/heads/master/Roku/.channels.json.gz"  
    EPG_URL = "https://github.com/matthuisman/i.mjh.nz/raw/master/Roku/all.xml"
    
    # --- Data Fetching and Parsing ---

    roku_data = None
    try:
        logging.info(f"Fetching GZIP URL: {ROKU_URL}")
        response = requests.get(ROKU_URL, stream=True)
        response.raise_for_status()  # Check for bad status codes (4xx or 5xx)

        # 1. Read the binary content
        compressed_file = BytesIO(response.content)
        
        # 2. Decompress the content using the gzip library
        with gzip.GzipFile(fileobj=compressed_file, mode='rb') as f:
            decompressed_data = f.read()
        
        # 3. Decode the bytes to a string and parse as JSON
        json_string = decompressed_data.decode('utf-8')
        roku_data = json.loads(json_string)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching URL {ROKU_URL}: {e}")
        logging.error("Failed to fetch or parse Roku data due to request error.")
        return
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON from URL {ROKU_URL}: {e}")
        logging.error("Failed to fetch or parse Roku data due to JSON error.")
        return
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.error("Failed to fetch or parse Roku data.")
        return

    if not roku_data:
        logging.error("No Roku data loaded after fetching.")
        return
    
    logging.info(f"Successfully fetched and parsed {len(roku_data)} channels.")
    
    # --- Playlist Generation Logic (Placeholder) ---
    
    # Assume the rest of your original script processes roku_data and writes 
    # the output to 'roku.m3u'
    
    output_lines = ["#EXTM3U"]
    
    # Example processing loop (replace with your actual logic)
    for channel in roku_data:
        try:
            name = channel.get("name", "Unknown Channel")
            url = channel.get("stream_url", "")
            tvg_id = channel.get("tvg_id", "")
            tvg_name = channel.get("tvg_name", name)
            
            if url:
                header = f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}",{name}'
                output_lines.append(header)
                output_lines.append(url)
        except Exception as e:
            logging.warning(f"Skipping channel due to error: {e}")


    # --- File Writing ---
    
    try:
        with open("roku.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines) + "\n")
        logging.info("Successfully wrote playlist to roku.m3u")
    except IOError as e:
        logging.error(f"Error writing to roku.m3u: {e}")


# --- Execution ---
if __name__ == "__main__":
    generate_roku_playlist()
