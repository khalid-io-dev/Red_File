from typing import List, Dict

class CVEPredictor:
    def __init__(self):
        self.cve_db = {
            "apache": {"2.4.49": ["CVE-2021-41773"]},
            "wordpress": {"5.8": ["CVE-2021-39200"]},
            "mysql": {"5.7": ["CVE-2021-2471"]},
        }
    
    def predict_cves(self, tech: str, version: str) -> List[Dict]:
        results = []
        for key, versions in self.cve_db.items():
            if key in tech.lower():
                for ver, cves in versions.items():
                    if ver in version:
                        for cve in cves:
                            results.append({
                                "cve_id": cve,
                                "tech": tech,
                                "version": version,
                                "severity": "high"
                            })
        return results
    
    def predict_exploit_success(self, target: Dict, exploit: str) -> Dict:
        success = 0.5
        if target.get("waf"): success *= 0.4
        if target.get("ids"): success *= 0.5
        return {"exploit": exploit, "probability": success}

cve_predictor = CVEPredictor()
