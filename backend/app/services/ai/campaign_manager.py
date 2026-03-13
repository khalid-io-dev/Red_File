from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import json
import uuid

class CampaignStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class Campaign:
    def __init__(self, name: str, targets: List[str], owner_id: int):
        self.id = str(uuid.uuid4())
        self.name = name
        self.targets = targets
        self.owner_id = owner_id
        self.status = CampaignStatus.PENDING
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.results = {}
        self.credentials = []
        self.findings = []
        self.metadata = {
            'total_targets': len(targets),
            'completed_targets': 0,
            'total_tools_run': 0,
            'vulnerabilities_found': 0
        }
    
    def start(self):
        self.status = CampaignStatus.RUNNING
        self.started_at = datetime.now()
    
    def pause(self):
        self.status = CampaignStatus.PAUSED
    
    def resume(self):
        self.status = CampaignStatus.RUNNING
    
    def complete(self):
        self.status = CampaignStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def fail(self, error: str):
        self.status = CampaignStatus.FAILED
        self.metadata['error'] = error
        self.completed_at = datetime.now()
    
    def add_result(self, target: str, result: Dict[str, Any]):
        self.results[target] = result
        self.metadata['completed_targets'] += 1
    
    def add_credential(self, target: str, username: str, password: str, service: str):
        self.credentials.append({
            'target': target,
            'username': username,
            'password': password,
            'service': service,
            'discovered_at': datetime.now().isoformat()
        })
    
    def add_finding(self, target: str, tool: str, severity: str, description: str):
        self.findings.append({
            'target': target,
            'tool': tool,
            'severity': severity,
            'description': description,
            'discovered_at': datetime.now().isoformat()
        })
        
        if severity in ['Critical', 'High']:
            self.metadata['vulnerabilities_found'] += 1
    
    def get_progress(self) -> float:
        if self.metadata['total_targets'] == 0:
            return 0.0
        return (self.metadata['completed_targets'] / self.metadata['total_targets']) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'targets': self.targets,
            'owner_id': self.owner_id,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'progress': self.get_progress(),
            'metadata': self.metadata,
            'credentials_found': len(self.credentials),
            'findings_count': len(self.findings)
        }

class CampaignManager:
    def __init__(self):
        self.campaigns: Dict[str, Campaign] = {}
    
    def create_campaign(self, name: str, targets: List[str], owner_id: int) -> Campaign:
        campaign = Campaign(name, targets, owner_id)
        self.campaigns[campaign.id] = campaign
        return campaign
    
    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        return self.campaigns.get(campaign_id)
    
    def list_campaigns(self, owner_id: Optional[int] = None) -> List[Campaign]:
        if owner_id:
            return [c for c in self.campaigns.values() if c.owner_id == owner_id]
        return list(self.campaigns.values())
    
    def delete_campaign(self, campaign_id: str) -> bool:
        if campaign_id in self.campaigns:
            del self.campaigns[campaign_id]
            return True
        return False
    
    def get_campaign_summary(self, campaign_id: str) -> Dict[str, Any]:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return {'error': 'Campaign not found'}
        
        return {
            **campaign.to_dict(),
            'credentials': campaign.credentials,
            'findings': campaign.findings,
            'results': campaign.results
        }

# Global instance
campaign_manager = CampaignManager()
