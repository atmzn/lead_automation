import sys
import json

def infer_industry(company_name: str) -> str:
    """Einfache Branchenerkennung per Keyword"""
    keywords = {
        "media": "Medien",
        "tech": "IT",
        "software": "IT",
        "consulting": "Beratung",
        "health": "Gesundheit",
        "finance": "Finanzen"
    }
    name = company_name.lower()
    for key, branch in keywords.items():
        if key in name:
            return branch
    return "Allgemein"

def estimate_size(email: str) -> str:
    """Firmengröße grob schätzen basierend auf der E-Mail-Domain"""
    domain = email.split('@')[-1]
    free_providers = ["gmail.com", "web.de", "hotmail.com", "gmx.de", "outlook.com"]
    if domain in free_providers:
        return "1-5"
    return "51-200"  # Annahme: geschäftliche Domain

def lead_score(email: str) -> int:
    """Scoring anhand der Domain-Qualität"""
    domain = email.split('@')[-1]
    free_providers = ["gmail.com", "web.de", "hotmail.com", "gmx.de", "outlook.com"]
    if domain in free_providers:
        return 30  # Geringes Vertrauen
    elif domain.endswith(".org") or domain.endswith(".edu"):
        return 60  # Mittelmäßig
    else:
        return 85  # Firmenadresse

def enrich_lead(data: dict) -> dict:
    """Lead-Daten anreichern"""
    enriched = data.copy()
    company = data.get("company", "")
    email = data.get("email", "")

    enriched["industry"] = infer_industry(company)
    enriched["company_size"] = estimate_size(email)
    enriched["score"] = lead_score(email)

    return enriched

def main():
    raw_input = sys.stdin.read()
    try:
        data = json.loads(raw_input)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)

    result = enrich_lead(data)
    print(json.dumps(result))

if __name__ == "__main__":
    main()
