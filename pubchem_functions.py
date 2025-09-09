##pubchem_functions.py
import requests
import logging

# Set up a module-level logger that logs only to a file.
logger = logging.getLogger("pubchem")
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent propagation to the root logger

# Clear existing handlers if any (useful in interactive environments)
if logger.hasHandlers():
    logger.handlers.clear()

file_handler = logging.FileHandler("pfoa_analysis.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def fetch_data(url):
    """Fetch JSON data from the given URL."""
    try:
        logger.info(f"Fetching data from {url}")
        response = requests.get(url)
        response.raise_for_status()
        logger.info("Data fetched successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        return None

def molecular_weight(data):
    """Extract the molecular weight from the provided data."""
    try:
        for prop in data['PC_Compounds'][0]['props']:
            if prop['urn']['label'] == 'Molecular Weight':
                weight = prop['value']['sval']
                logger.info(f"Molecular weight: {weight}")
                return weight
    except (IndexError, KeyError) as e:
        logger.error(f"Error extracting molecular weight: {e}")
    return None

def smiles(data):
    """Extract the SMILES string from the provided data."""
    try:
        for prop in data['PC_Compounds'][0]['props']:
            if prop['urn']['label'] == 'SMILES':
                s = prop['value']['sval']
                logger.info(f"SMILES: {s}")
                return s
    except (IndexError, KeyError) as e:
        logger.error(f"Error extracting SMILES: {e}")
    return None

def hydrogen_bond_donors(data):
    """Extract the hydrogen bond donor count from the provided data."""
    try:
        for prop in data['PC_Compounds'][0]['props']:
            if prop['urn']['label'] == 'Count' and prop['urn'].get('name') == 'Hydrogen Bond Donor':
                donors = prop['value']['ival']
                logger.info(f"Hydrogen bond donors: {donors}")
                return donors
    except (IndexError, KeyError) as e:
        logger.error(f"Error extracting hydrogen bond donors: {e}")
    return None

def hydrogen_bond_acceptors(data):
    """Extract the hydrogen bond acceptor count from the provided data."""
    try:
        for prop in data['PC_Compounds'][0]['props']:
            if prop['urn']['label'] == 'Count' and prop['urn'].get('name') == 'Hydrogen Bond Acceptor':
                acceptors = prop['value']['ival']
                logger.info(f"Hydrogen bond acceptors: {acceptors}")
                return acceptors
    except (IndexError, KeyError) as e:
        logger.error(f"Error extracting hydrogen bond acceptors: {e}")
    return None

def run_analysis(url):
    """Fetch data and extract key properties from the PubChem API."""
    data = fetch_data(url)
    if data:
        results = {
            "molecular_weight": molecular_weight(data),
            "SMILES": smiles(data),
            "hydrogen_bond_donors": hydrogen_bond_donors(data),
            "hydrogen_bond_acceptors": hydrogen_bond_acceptors(data)
        }
        logger.info("Analysis Results: " + str(results))
        return results
    else:
        logger.error("No data fetched. Exiting analysis.")
        return None

