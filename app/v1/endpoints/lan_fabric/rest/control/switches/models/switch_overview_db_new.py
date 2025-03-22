from typing import Dict, Optional, List, Any
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship, select, Column, JSON
import json

"""
This simplifies things by using separate tables for Config, Health, Roles,
HW Versions, and SW Versions.  There is no need to link these tables e.g.
through a foreign key in the SwitchOverview table since there is only
a single overview record.
"""

class SwitchConfigBase(SQLModel):
    """
    Base class for SwitchConfig, defining the data fields without the table.

    Attributes:
        in_sync (int): The number of switches that are in sync with the configuration.
        out_of_sync (int): The number of switches that are out of sync with the configuration.
    """
    in_sync: int = Field(default=0)
    out_of_sync: int = Field(default=0)


class SwitchConfigDbModel(SwitchConfigBase, table=True):
    """
    SQLModel table representing the configuration synchronization status of switches.
    """
    id: Optional[int] = Field(default=None, primary_key=True)


class SwitchHealthBase(SQLModel):
    """
    Base class for SwitchHealthDbModel, defining the data fields without the table.

    Attributes:
        Healthy (int): The number of switches with a healthy status.
        Major (int): The number of switches with a major health issue.
        Minor (int): The number of switches with a minor health issue.
    """
    Healthy: int
    Major: int
    Minor: int


class SwitchHealthDbModel(SwitchHealthBase, table=True):
    """
    SQLModel table representing the health status of switches.
    """
    id: Optional[int] = Field(default=None, primary_key=True)


class SwitchRolesBase(SQLModel):
    """
    Base class for SwitchRolesDbModel, defining the data fields without the table.

    Attributes:
        access (int): The number of switches with the access role.
        aggregation (int): The number of switches with the aggregation role.
        border (int): The number of switches with the border role.
        border_gateway (int): The number of switches with the border gateway role.
        border_gateway_spine (int): The number of switches with the border gateway spine role.
        border_gateway_super_spine (int): The number of switches with the border gateway super spine role.
        border_spine (int): The number of switches with the border spine role.
        border_super_spine (int): The number of switches with the border super spine role.
        core_router (int): The number of switches with the core router role.
        edge_router (int): The number of switches with the edge router role.
        leaf (int): The number of switches with the leaf role.
        spine (int): The number of switches with the spine role.
        super_spine (int): The number of switches with the super spine role.
        tor (int): The number of switches with the Top of Rack (TOR) role.
    """
    access: int = Field(default=0)
    aggregation: int = Field(default=0)
    border: int = Field(default=0)
    border_gateway: int = Field(default=0)
    border_gateway_spine: int = Field(default=0)
    border_gateway_super_spine: int = Field(default=0)
    border_spine: int = Field(default=0)
    border_super_spine: int = Field(default=0)
    core_router: int = Field(default=0)
    edge_router: int = Field(default=0)
    leaf: int = Field(default=0)
    spine: int = Field(default=0)
    super_spine: int = Field(default=0)
    tor: int = Field(default=0)


class SwitchRolesDbModel(SwitchRolesBase, table=True):
    """
    SQLModel table representing the roles of switches in the network.

    Attributes:
        id (Optional[int]): The primary key for the table.
        switch_overview_id (Optional[int]): Foreign key linking to the SwitchOverviewDbModel table.
    """
    id: Optional[int] = Field(default=None, primary_key=True)


class SwitchVersionBase(SQLModel):
    """Base class for Switch Versions."""
    version_name: str
    count: int


class SwitchHWVersionsDbModel(SwitchVersionBase, table=True):
    """
    SQLModel table representing the hardware versions of switches.
    Stores each HW version as a separate row.
    """
    id: Optional[int] = Field(default=None, primary_key=True)


class SwitchSWVersionsDbModel(SwitchVersionBase, table=True):
    """
    SQLModel table representing the software versions of switches.
    Stores each SW version as a separate row.
    """
    id: Optional[int] = Field(default=None, primary_key=True)


class SwitchOverviewResponseModel(BaseModel):
    """
    Represents the overall switch overview data.

    Attributes:
        switchConfig (SwitchConfigBase): Configuration synchronization status of the switches.
        switchHealth (SwitchHealthBase): Health status of the switches.
        switchHWVersions (Dict[str, int]): Hardware versions of the switches.
        switchRoles (Dict): Roles of the switches in the network.
        switchSWVersions (Dict[str, int]): Software versions of the switches.
    """
    switchConfig: SwitchConfigBase
    switchHealth: SwitchHealthBase
    switchHWVersions: Dict[str, int]
    switchRoles: Dict[str, int]
    switchSWVersions: Dict[str, int]


class SwitchOverview:
    """
    Class to initialize and/or update the switch overview models using property setters.

    Usage:

    This class is called to add or remove the data associated with one switch from each
    of the switch overview tables.

    switch_overview = SwitchOverview()
    switch_overview.health = "Healthy" # "Healthy", "Major", or "Minor"
    switch_overview.hw_version = "N9K-C93180YC-EX"
    switch_overview.role = "leaf"
    switch_overview.sw_version = "10.2(5)"
    switch_overview.sync = True # True is in_sync, False is out_of_sync

    switch_overview.commit() # Commits the changes to the various database tables
    associated with a the switch overview response.

    # Compile the data from the switch overview database tables into a
    # single response.
    response = switch_overview.response()
    """
    def __init__(self):
        self._health = None
        self._hw_version = None
        self._role = None
        self._sw_version = None
        self._sync = None
        self.response_model = SwitchOverviewResponseModel

        self._init_switch_config = SwitchConfigDbModel(in_sync=0, out_of_sync=0)
        self._init_switch_health = SwitchHealthDbModel(Healthy=0, Major=0, Minor=0)
        self._init_switch_hw_versions = SwitchHWVersionsDbModel(version_name="ignore", count=0)
        self._init_switch_roles = SwitchRolesDbModel(
            access=0,
            aggregation=0,
            border=0,
            border_gateway=0,
            border_gateway_spine=0,
            border_gateway_super_spine=0,
            border_spine=0,
            border_super_spine=0,
            core_router=0,
            edge_router=0,
            leaf=0,
            spine=0,
            super_spine=0,
            tor=0
        )
        self._init_switch_sw_versions = SwitchHWVersionsDbModel(version_name="ignore", count=0)

    
    def initialize_db_tables(self):
        """
        Initializes the switch overview database tables.
        """
        commit = False
        with Session(engine) as session:
            statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.id == 1)
            switch_config_db = session.exec(statement).first()
            if switch_config_db is None:
                switch_config_db = SwitchConfigDbModel(**self._init_switch_config.model_dump())
                session.add(switch_config_db)
                commit = True

            statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.id == 1)
            switch_health_db = session.exec(statement).first()
            if switch_health_db is None:
                switch_health_db = SwitchHealthDbModel(**self._init_switch_health.model_dump())
                session.add(switch_health_db)
                commit = True

            statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.id == 1)
            switch_roles_db = session.exec(statement).first()
            if switch_roles_db is None:
                switch_roles_db = SwitchRolesDbModel(**self._init_switch_roles.model_dump())
                session.add(switch_roles_db)
                commit = True
            
            statement = select(SwitchHWVersionsDbModel)
            switch_hw_versions = session.exec(statement).all()
            if len(switch_hw_versions) == 0:
                switch_hw_db = SwitchHWVersionsDbModel(**self._init_switch_hw_versions.model_dump())
                session.add(switch_hw_db)
                commit = True

            statement = select(SwitchSWVersionsDbModel)
            switch_sw_versions = session.exec(statement).all()
            if len(switch_sw_versions) == 0:
                switch_sw_db = SwitchSWVersionsDbModel(**self._init_switch_sw_versions.model_dump())
                session.add(switch_sw_db)
                commit = True

            # Persist the database tables
            if commit:
                session.commit()


    def update_switch_config(self, session):
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.id == 1)
        switch_config = session.exec(statement).first()
        if self.sync is True:
            switch_config.in_sync += 1
        else:
            switch_config.out_of_sync += 1
        session.add(switch_config)


    def update_switch_health(self, session):
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.id == 1)
        switch_health = session.exec(statement).first()
        if self.health == "Healthy":
            switch_health.Healthy += 1
        elif self.health == "Major":
            switch_health.Major += 1
        elif self.health == "Minor":
            switch_health.Minor += 1
        session.add(switch_health)


    def update_switch_roles(self, session):
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.id == 1)
        switch_roles = session.exec(statement).first()

        if self.role == "access":
            switch_roles.access += 1
        elif self.role == "aggregation":
            switch_roles.aggregation += 1
        elif self.role == "border":
            switch_roles.border += 1
        elif self.role == "border_gateway":
            switch_roles.border_gateway += 1
        elif self.role == "border_gateway_spine":
            switch_roles.border_gateway_spine += 1
        elif self.role == "border_gateway_super_spine":
            switch_roles.border_gateway_super_spine += 1
        elif self.role == "border_spine":
            switch_roles.border_spine += 1
        elif self.role == "border_super_spine":
            switch_roles.border_super_spine += 1
        elif self.role == "core_router":
            switch_roles.core_router += 1
        elif self.role == "edge_router":
            switch_roles.edge_router += 1
        elif self.role == "leaf":
            switch_roles.leaf += 1
        elif self.role == "spine":
            switch_roles.spine += 1
        elif self.role == "super_spine":
            switch_roles.super_spine += 1
        elif self.role == "tor":
            switch_roles.tor += 1
        session.add(switch_roles)


    def update_switch_hw_versions(self, session):
        statement = select(SwitchHWVersionsDbModel)
        switch_hw_versions = session.exec(statement).all()
        if self.hw_version not in [hw.version_name for hw in switch_hw_versions]:
            hw = SwitchHWVersionsDbModel(version_name=self.hw_version, count=1)
            session.add(hw)
        else:
            for hw in switch_hw_versions:
                if hw.version_name == self.hw_version:
                    hw.count += 1
                    session.add(hw)


    def update_switch_sw_versions(self, session):
        statement = select(SwitchSWVersionsDbModel)
        switch_sw_versions = session.exec(statement).all()
        if self.sw_version not in [sw.version_name for sw in switch_sw_versions]:
            sw = SwitchSWVersionsDbModel(version_name=self.sw_version, count=1)
            session.add(sw)
        else:
            for sw in switch_sw_versions:
                if sw.version_name == self.sw_version:
                    sw.count += 1
                    session.add(sw)


    def commit(self):
        """
        Commits the changes to the database.
        """
        if self._health is None:
            raise ValueError("Health status not set.")
        if self._hw_version is None:
            raise ValueError("Hardware version not set.")
        if self._role is None:
            raise ValueError("Role not set.")
        if self._sw_version is None:
            raise ValueError("Software version not set.")
        if self._sync is None:
            raise ValueError("Sync status not set.")

        with Session(engine) as session:
            self.update_switch_config(session)
            self.update_switch_health(session)
            self.update_switch_roles(session)
            self.update_switch_hw_versions(session)
            self.update_switch_sw_versions(session)
            session.commit()


    def response(self) -> Dict[str, Any]:
        """
        Returns the current switch overview data.

        Returns:
            Dict[str, Any]: The current switch overview data.
        """
        session = Session(engine)

        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.id == 1)
        switch_config = session.exec(statement).first()

        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.id == 1)
        switch_health = session.exec(statement).first()

        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.id == 1)
        switch_roles = session.exec(statement).first()

        statement = select(SwitchHWVersionsDbModel)
        switch_hw_versions = session.exec(statement).all()

        statement = select(SwitchSWVersionsDbModel)
        switch_sw_versions = session.exec(statement).all()

        hw_response = {}
        for hw in switch_hw_versions:
            if hw.version_name != "ignore":
                hw_response[hw.version_name] = hw.count

        sw_response = {}
        for sw in switch_sw_versions:
            if sw.version_name != "ignore":
                sw_response[sw.version_name] = sw.count

        response = SwitchOverviewResponseModel(
            switchConfig=switch_config.model_dump(exclude={'id'}),
            switchHealth=switch_health.model_dump(exclude={'id'}),
            switchRoles=switch_roles.model_dump(exclude={'id'}),
            switchHWVersions=hw_response,
            switchSWVersions=sw_response
        )
        return response.model_dump_json(indent=4)

    @property
    def health(self) -> str:
        return self._health
    @health.setter
    def health(self, value: str):
        self._health = value
    
    @property
    def hw_version(self) -> str:
        return self._hw_version
    @hw_version.setter
    def hw_version(self, value: str):
        self._hw_version = value

    @property
    def role(self) -> str:
        return self._role
    @role.setter
    def role(self, value: str):
        self._role = value
    
    @property
    def sw_version(self) -> str:
        return self._sw_version
    @sw_version.setter
    def sw_version(self, value: str):
        self._sw_version = value
    
    @property
    def sync(self) -> bool:
        return self._sync
    @sync.setter
    def sync(self, value: bool):
        self._sync = value


if __name__ == "__main__":
    from sqlmodel import create_engine, Session, select

    DATABASE_URL = "sqlite:///./nexus_dashboard.db"  # Replace with your database URL
    engine = create_engine(DATABASE_URL, echo=True)

    SQLModel.metadata.create_all(engine)

    # Test the SwitchOverview class
    switch_overview = SwitchOverview()
    switch_overview.initialize_db_tables()

    switch_overview.health = "Healthy"
    switch_overview.hw_version = "N9K-C93180YC-EX"
    switch_overview.role = "leaf"
    switch_overview.sw_version = "10.2(5)"
    switch_overview.sync = True
    switch_overview.commit()

    switch_overview.health = "Healthy"
    switch_overview.hw_version = "N9K-9508"
    switch_overview.role = "spine"
    switch_overview.sw_version = "10.3(3)"
    switch_overview.sync = False
    switch_overview.commit()

    print(f"ZZZ: response: {switch_overview.response()}")

