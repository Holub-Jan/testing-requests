from pydantic import BaseModel


class TestTable(BaseModel):
    name: str
    num: int


class Organization(BaseModel):
    name: str
    active: int


class Repository(BaseModel):
    name: str
    org_id: int


class Team(BaseModel):
    name: str
    org_id: int


class TeamRepository(BaseModel):
    name: str
    team_id: int
    repo_id: int
    role: str


class User(BaseModel):
    name: str
    team_id: int


class Key(BaseModel):
    name: str
    repo_id: int
    private_key: int
    public_key: int
    read_only: int

