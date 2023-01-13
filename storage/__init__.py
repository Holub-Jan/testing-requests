from storage.models import Organization
from storage.organization_storage import OrganizationStorage
from storage.sqlite_client import SQLiteClient

if __name__ == "__main__":
    sqc = SQLiteClient(file_path="mydb.db", password="123456789")
    org_stg = OrganizationStorage(sqc)
    query = [('name', 'standa-novak')]
    org = org_stg.select_by_query(query)
    if not org:
        new_org = Organization(name="standa-novak", active=0)
        org_stg.create(new_org)
    org = org_stg.select_by_query(query)
    query = [('name', 'standa-novak'), ('active', 0), ('ID', 1)]
    result = org_stg.select_by_query(query)
    print(result)
