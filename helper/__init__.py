from container.org_helper import OrganizationHelper
from storage import SQLiteClient

if __name__ == "__main__":
    sqc = SQLiteClient(file_path="mydb.db", password="123456789")
    org_help = OrganizationHelper(sqc)
    org_row = org_help.get_or_create('standa-novak')
    print(org_row)
