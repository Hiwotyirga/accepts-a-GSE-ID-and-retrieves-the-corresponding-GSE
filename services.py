import requests
import re
from typing import Union, Dict, Optional
from config import NCBI_API_KEY

def fetch_gse_entry(gse_id: str, api_key: Optional[str] = NCBI_API_KEY) -> Union[str, Dict[str, str]]:
   
    if not gse_id or not isinstance(gse_id, str):
        return {"error": "invalid_input", "message": "GSE ID must be a non-empty string"}
        
    if not re.match(r'^GSE\d+$', gse_id):
        return {"error": "invalid_id", "message": f"Invalid GSE ID format: {gse_id}"}
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    headers = {"User-Agent": "GSE_Fetcher/1.0"}
    
    search_params = {
            "db": "gds",
            "term": f"{gse_id}[Accession]",
            "api_key": api_key,
            "retmode": "json"
        }
        
    search_response = requests.get(
            f"{base_url}esearch.fcgi",
            params=search_params,
            headers=headers,
            timeout=15
        )
    search_response.raise_for_status()
    search_data = search_response.json()
        
    id_list = search_data.get("esearchresult", {}).get("idlist", [])
    if not id_list:
            return {"error": "not_found", "message": f"{gse_id} not found in GEO database"}
            
    uid = id_list[0]

    summary_params = {
                "db": "gds",
                "id": uid,
                "retmode": "json",
                "api_key": api_key
            }
    summary_response = requests.get(
                f"{base_url}esummary.fcgi",
                params=summary_params,
                headers=headers,
                timeout=15
            )
    summary_response.raise_for_status()
    summary_data = summary_response.json()
    return summary_data

                    
    

    
# # test
# result = fetch_gse_entry("GSE13507")
# import json
# print(json.dumps(result, indent=2))  
