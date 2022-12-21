from pydantic import BaseModel


class TableModel(BaseModel):
    id_: int = -1
    name: str


class Organization(TableModel):
    active: int


class Repository(TableModel):
    org_id: int


class Team(TableModel):
    org_id: int


class TeamRepository(TableModel):
    team_id: int
    repo_id: int
    role: str


class User(TableModel):
    team_id: int


class Key(TableModel):
    repo_id: int
    private_key: str
    public_key: str
    read_only: int

