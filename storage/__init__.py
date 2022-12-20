from storage.models import Organization
from storage.organization_storage import OrganizationStorage
from storage.sqlite_client import SQLiteClient

if __name__ == "__main__":
    sqc = SQLiteClient(file_path="mydb.db", password="123456789")
    org_stg = OrganizationStorage(sqc)
    org = org_stg.select_by_name("standa-novak")
    if not org:
        new_org = Organization(name="standa-novak", active=0)
        org_stg.create(new_org)
    org = org_stg.select_by_name("standa-novak")
    query = [('name', 'standa-novak'), ('active', 0)]
    result = org_stg.select_by_data(query)
    print(result)
