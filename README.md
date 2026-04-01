# Contacts Collector

Searches businesses in a U.S. state with Google Places and exports contact data (website, phone, and email when found).

## What it does

- Looks up cities in a state (via City-Data).
- Searches Google Places Text Search for `<city> + <business type>`.
- Avoids duplicate businesses using a saved place ID file.
- Fetches website and phone from Google Places Details API.
- Tries to extract email addresses from business websites (including contact/about pages).
- Exports results to CSV.

## Requirements

- Python 3.10+
- Google Places API key (Text Search + Place Details)
- Google Chrome installed (used by Selenium for email scraping)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

1. Create a `.env` file in the project root:

```env
PLACES_API_KEY=your_google_places_api_key_here
```

2. In `main.py`, set your search values:

```python
STATE = "Input state"
BUSINESS = "Input business type (e.g. 'restaurant', 'plumber', etc.)"
```

## Run

```bash
python main.py
```

## Output files

After running, you will get:

- `{STATE} ids.json` - saved Google Place IDs to prevent duplicate exports in future runs.
- `{STATE} {BUSINESS}.csv` - table with:
  - `City`
  - `Name`
  - `Website`
  - `Phone number`
  - `Email`

## Notes and limitations

- Email scraping depends on each business website; many sites do not expose emails publicly.
- Some records may show placeholders like `Couldn't find website` or `Couldn't find an email`.
- Google API usage may incur costs depending on your quota/billing setup.
- The city list source and site structure can change, which may affect scraping.

## Troubleshooting

- **Missing API key / auth errors**: verify `PLACES_API_KEY` exists in `.env`.
- **No Chrome/Selenium issues**: install/update Chrome and Selenium.
- **Slow runs**: expected for large states because each city and place details request is queried.
- **Empty CSV**: try a broader `BUSINESS` term or a different `STATE`.

