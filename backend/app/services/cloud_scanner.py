import boto3
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.compute import ComputeManagementClient
from google.cloud import storage, compute_v1
from typing import List, Dict
import os

class CloudScanner:
    """Scan cloud infrastructure for security issues"""
    
    def __init__(self):
        self.aws_session = None
        self.azure_credential = None
        self.gcp_project = os.getenv('GCP_PROJECT_ID')
    
    # ===== AWS SCANNING =====
    
    async def scan_aws_s3(self, region: str = 'us-east-1') -> List[Dict]:
        """Scan AWS S3 buckets for misconfigurations"""
        findings = []
        try:
            s3 = boto3.client('s3', region_name=region)
            buckets = s3.list_buckets()['Buckets']
            
            for bucket in buckets:
                bucket_name = bucket['Name']
                
                # Check public access
                try:
                    acl = s3.get_bucket_acl(Bucket=bucket_name)
                    for grant in acl['Grants']:
                        if grant['Grantee'].get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                            findings.append({
                                "resource": bucket_name,
                                "type": "S3 Bucket",
                                "severity": "Critical",
                                "issue": "Publicly accessible bucket",
                                "description": f"Bucket {bucket_name} is publicly accessible"
                            })
                except:
                    pass
                
                # Check encryption
                try:
                    encryption = s3.get_bucket_encryption(Bucket=bucket_name)
                except:
                    findings.append({
                        "resource": bucket_name,
                        "type": "S3 Bucket",
                        "severity": "High",
                        "issue": "Encryption not enabled",
                        "description": f"Bucket {bucket_name} does not have encryption enabled"
                    })
                
                # Check versioning
                try:
                    versioning = s3.get_bucket_versioning(Bucket=bucket_name)
                    if versioning.get('Status') != 'Enabled':
                        findings.append({
                            "resource": bucket_name,
                            "type": "S3 Bucket",
                            "severity": "Medium",
                            "issue": "Versioning not enabled",
                            "description": f"Bucket {bucket_name} does not have versioning enabled"
                        })
                except:
                    pass
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def scan_aws_iam(self) -> List[Dict]:
        """Scan AWS IAM for security issues"""
        findings = []
        try:
            iam = boto3.client('iam')
            
            # Check for users without MFA
            users = iam.list_users()['Users']
            for user in users:
                username = user['UserName']
                mfa_devices = iam.list_mfa_devices(UserName=username)['MFADevices']
                
                if not mfa_devices:
                    findings.append({
                        "resource": username,
                        "type": "IAM User",
                        "severity": "High",
                        "issue": "MFA not enabled",
                        "description": f"User {username} does not have MFA enabled"
                    })
            
            # Check for overly permissive policies
            policies = iam.list_policies(Scope='Local')['Policies']
            for policy in policies:
                policy_arn = policy['Arn']
                version = iam.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
                policy_doc = iam.get_policy_version(PolicyArn=policy_arn, VersionId=version)
                
                # Check for wildcard permissions
                for statement in policy_doc['PolicyVersion']['Document'].get('Statement', []):
                    if statement.get('Effect') == 'Allow' and statement.get('Action') == '*':
                        findings.append({
                            "resource": policy['PolicyName'],
                            "type": "IAM Policy",
                            "severity": "Critical",
                            "issue": "Wildcard permissions",
                            "description": f"Policy {policy['PolicyName']} grants wildcard permissions"
                        })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def scan_aws_ec2(self, region: str = 'us-east-1') -> List[Dict]:
        """Scan AWS EC2 instances"""
        findings = []
        try:
            ec2 = boto3.client('ec2', region_name=region)
            instances = ec2.describe_instances()
            
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    
                    # Check for public IP
                    if instance.get('PublicIpAddress'):
                        findings.append({
                            "resource": instance_id,
                            "type": "EC2 Instance",
                            "severity": "Medium",
                            "issue": "Public IP assigned",
                            "description": f"Instance {instance_id} has public IP {instance['PublicIpAddress']}"
                        })
                    
                    # Check for unencrypted volumes
                    for bdm in instance.get('BlockDeviceMappings', []):
                        volume_id = bdm['Ebs']['VolumeId']
                        volume = ec2.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]
                        
                        if not volume.get('Encrypted'):
                            findings.append({
                                "resource": volume_id,
                                "type": "EBS Volume",
                                "severity": "High",
                                "issue": "Unencrypted volume",
                                "description": f"Volume {volume_id} is not encrypted"
                            })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def scan_aws_security_groups(self, region: str = 'us-east-1') -> List[Dict]:
        """Scan AWS security groups"""
        findings = []
        try:
            ec2 = boto3.client('ec2', region_name=region)
            sgs = ec2.describe_security_groups()['SecurityGroups']
            
            for sg in sgs:
                sg_id = sg['GroupId']
                
                # Check for overly permissive rules
                for rule in sg.get('IpPermissions', []):
                    for ip_range in rule.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            findings.append({
                                "resource": sg_id,
                                "type": "Security Group",
                                "severity": "Critical",
                                "issue": "Open to internet",
                                "description": f"Security group {sg_id} allows access from 0.0.0.0/0 on port {rule.get('FromPort', 'all')}"
                            })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    # ===== AZURE SCANNING =====
    
    async def scan_azure_storage(self) -> List[Dict]:
        """Scan Azure storage accounts"""
        findings = []
        try:
            subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
            credential = DefaultAzureCredential()
            storage_client = StorageManagementClient(credential, subscription_id)
            
            accounts = storage_client.storage_accounts.list()
            for account in accounts:
                # Check for public access
                if account.allow_blob_public_access:
                    findings.append({
                        "resource": account.name,
                        "type": "Storage Account",
                        "severity": "High",
                        "issue": "Public blob access enabled",
                        "description": f"Storage account {account.name} allows public blob access"
                    })
                
                # Check for HTTPS only
                if not account.enable_https_traffic_only:
                    findings.append({
                        "resource": account.name,
                        "type": "Storage Account",
                        "severity": "Medium",
                        "issue": "HTTPS not enforced",
                        "description": f"Storage account {account.name} does not enforce HTTPS"
                    })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def scan_azure_vms(self) -> List[Dict]:
        """Scan Azure virtual machines"""
        findings = []
        try:
            subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
            credential = DefaultAzureCredential()
            compute_client = ComputeManagementClient(credential, subscription_id)
            
            vms = compute_client.virtual_machines.list_all()
            for vm in vms:
                # Check for unencrypted disks
                if vm.storage_profile.os_disk.encryption_settings is None:
                    findings.append({
                        "resource": vm.name,
                        "type": "Virtual Machine",
                        "severity": "High",
                        "issue": "Disk encryption not enabled",
                        "description": f"VM {vm.name} does not have disk encryption enabled"
                    })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    # ===== GCP SCANNING =====
    
    async def scan_gcp_storage(self) -> List[Dict]:
        """Scan GCP storage buckets"""
        findings = []
        try:
            storage_client = storage.Client(project=self.gcp_project)
            buckets = storage_client.list_buckets()
            
            for bucket in buckets:
                # Check for public access
                policy = bucket.get_iam_policy()
                for binding in policy.bindings:
                    if 'allUsers' in binding['members'] or 'allAuthenticatedUsers' in binding['members']:
                        findings.append({
                            "resource": bucket.name,
                            "type": "GCS Bucket",
                            "severity": "Critical",
                            "issue": "Publicly accessible bucket",
                            "description": f"Bucket {bucket.name} is publicly accessible"
                        })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def scan_gcp_compute(self) -> List[Dict]:
        """Scan GCP compute instances"""
        findings = []
        try:
            compute_client = compute_v1.InstancesClient()
            
            # List all instances across all zones
            for zone in ['us-central1-a', 'us-east1-b']:  # Add more zones as needed
                request = compute_v1.ListInstancesRequest(
                    project=self.gcp_project,
                    zone=zone
                )
                instances = compute_client.list(request=request)
                
                for instance in instances:
                    # Check for external IP
                    for interface in instance.network_interfaces:
                        if interface.access_configs:
                            findings.append({
                                "resource": instance.name,
                                "type": "Compute Instance",
                                "severity": "Medium",
                                "issue": "External IP assigned",
                                "description": f"Instance {instance.name} has external IP"
                            })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings

    # ===== MAIN SCAN METHODS =====

    async def scan_aws(self, access_key: str, secret_key: str, region: str = 'us-east-1') -> Dict:
        """Full AWS security scan"""
        import os
        # Set credentials for boto3
        os.environ['AWS_ACCESS_KEY_ID'] = access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = secret_key

        findings = []
        findings.extend(await self.scan_aws_s3(region))
        findings.extend(await self.scan_aws_iam())
        findings.extend(await self.scan_aws_ec2(region))
        findings.extend(await self.scan_aws_security_groups(region))

        return {
            "provider": "aws",
            "region": region,
            "findings": findings,
            "total_findings": len(findings),
            "critical": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'Critical']),
            "high": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'High']),
            "medium": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'Medium']),
            "low": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'Low'])
        }

    async def scan_azure(self, subscription_id: str, tenant_id: str, client_id: str, client_secret: str) -> Dict:
        """Full Azure security scan"""
        import os
        os.environ['AZURE_SUBSCRIPTION_ID'] = subscription_id
        os.environ['AZURE_TENANT_ID'] = tenant_id
        os.environ['AZURE_CLIENT_ID'] = client_id
        os.environ['AZURE_CLIENT_SECRET'] = client_secret

        findings = []
        findings.extend(await self.scan_azure_storage())
        findings.extend(await self.scan_azure_vms())

        return {
            "provider": "azure",
            "subscription_id": subscription_id,
            "findings": findings,
            "total_findings": len(findings),
            "critical": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'Critical']),
            "high": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'High']),
            "medium": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'Medium']),
            "low": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'Low'])
        }

    async def scan_gcp(self, project_id: str, credentials_json: str) -> Dict:
        """Full GCP security scan"""
        import os
        os.environ['GCP_PROJECT_ID'] = project_id

        findings = []
        findings.extend(await self.scan_gcp_storage())
        findings.extend(await self.scan_gcp_compute())

        return {
            "provider": "gcp",
            "project_id": project_id,
            "findings": findings,
            "total_findings": len(findings),
            "critical": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'Critical']),
            "high": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'High']),
            "medium": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'Medium']),
            "low": len([f for f in findings if isinstance(f, dict) and f.get('severity') == 'Low'])
        }

# Singleton instance
cloud_scanner = CloudScanner()
