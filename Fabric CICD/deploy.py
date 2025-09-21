from pathlib import Path
import argparse, yaml, fnmatch
from azure.identity import ClientSecretCredential
from fabric_cicd import FabricWorkspace, publish_all_items

SUPPORTED_EXTS = {".tmdl", ".json", ".yml", ".yaml", ".sql"}

def main():
    ap = argparse.ArgumentParser(description="Deploy to Microsoft Fabric (SemanticModel -> Report)")
    ap.add_argument("--client_id", required=True)
    ap.add_argument("--client_secret", required=True)
    ap.add_argument("--tenant_id", required=True)
    ap.add_argument("--workspace_id", required=True)
    ap.add_argument("--repo_subdir", required=True)  # WS_DD_HealthSafety | WS_GDH | WS_UC_CSRDManagement
    ap.add_argument("--env", required=True, choices=["DEV", "ACC", "PROD"])
    a = ap.parse_args()
    
    print("CLIENT_ID (first 5):", a.client_id[:5])
    print("TENANT_ID (first 5):", a.tenant_id[:5])
    print("CLIENT_SECRET    (first 5):", a.client_secret[:5])

    cred = ClientSecretCredential(client_id=a.client_id, client_secret=a.client_secret, tenant_id=a.tenant_id)

    repo_root = Path(__file__).resolve().parent.parent
    repo_dir  = (repo_root / a.repo_subdir).resolve()
    param_path = repo_root / "parameter.yml"   

    # 1) Semantic Models 
    ws = FabricWorkspace(
        workspace_id=a.workspace_id,
        repository_directory=str(repo_dir),
        item_type_in_scope=["SemanticModel"],
        environment=a.env,
        token_credential=cred,
    )
    publish_all_items(ws)

    # 2) Reports
    ws = FabricWorkspace(
        workspace_id=a.workspace_id,
        repository_directory=str(repo_dir),
        item_type_in_scope=["Report"],
        environment=a.env,
        token_credential=cred,
    )
    publish_all_items(ws)

if __name__ == "__main__":
    main()
