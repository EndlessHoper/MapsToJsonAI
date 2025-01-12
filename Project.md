# Google Maps Vision Analysis with Groq Llama 3.2 90B

## Project Overview
This project leverages Groq's Llama 3.2 90B Vision (Preview) to analyze screenshots of Google Maps locations. The workflow is as follows:

### Key Components
- **Input**: Google Maps URL provided via command-line interface (CLI)
- **Screenshot Processing**: Capture the left third of the Google Maps page
- **AI Analysis**: 
  - Use Groq's Llama 3.2 90B Vision model
  - Pass the screenshot and a predefined user prompt
  - User prompt is stored in `userprompt.txt`
  - Image changes dynamically based on the input Maps URL

### Technical Stack
- Language: Python
- AI Model: Groq Llama 3.2 90B Vision
- Screenshot Capture: Custom implementation
- Prompt Management: Static user prompt in `userprompt.txt`

### Workflow
1. Accept Google Maps URL as CLI argument
2. Take screenshot of left third of the page
3. Read predefined user prompt from `userprompt.txt`
4. Send screenshot and prompt to Groq API
5. Receive and process AI-generated analysis

## Data Schema
- Venue data is structured using a comprehensive JSON schema defined in `VenueSchema.json`
- Schema includes:
  - Required fields: venue name, description, address, neighborhood, venue type
  - Optional fields: image, rating, tags
  - Detailed drink pricing information
  - Predefined neighborhood and venue type enumerations

### Schema Highlights
- Supports venues in Amsterdam neighborhoods
- Venue types: Drinks, Food, Coffee, Activity
- Flexible structure for AI-generated venue insights
- Enables consistent data extraction and storage

## Postcode to Gebied Utility

### Postcode Mapping Functionality
- **Purpose**: Retrieve the "gebied" (neighborhood/district) for a given Amsterdam postcode
- **Implementation**: `postcode_to_gebied.py`
- **Key Features**:
  - Uses PDOK Locatieserver API for initial address lookup
  - Queries Amsterdam Data API to extract neighborhood information
  - Handles various error scenarios gracefully

### API Integration
- **First API**: PDOK Locatieserver
  - Endpoint: `https://api.pdok.nl/bzk/locatieserver/search/v3_1/suggest`
  - Retrieves address details based on postcode
  - Filters for Amsterdam and Weesp addresses

- **Second API**: Amsterdam Data API
  - Endpoint: `https://api.data.amsterdam.nl/bag/v1.1/nummeraanduiding/`
  - Extracts detailed neighborhood (gebied) information

### Usage
- Interactive command-line interface
- User inputs a postcode
- Returns the corresponding Amsterdam neighborhood/district

### Error Handling
- Comprehensive error checking for:
  - Empty postcodes
  - API connection issues
  - Missing data in API responses

## Prerequisites
- Groq API Key
- Python 3.8+
- Required Python packages (to be listed in `requirements.txt`)