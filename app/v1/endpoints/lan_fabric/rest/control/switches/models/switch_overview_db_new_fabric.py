# TODO: If SQLModel is ever fixed, remove the mypy directive below.
# https://github.com/fastapi/sqlmodel/discussions/732
# mypy: disable-error-code=call-arg
from typing import Dict, Optional

from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

DATABASE_URL = "sqlite:///./nexus_dashboard.db"  # Replace with your database URL
engine = create_engine(DATABASE_URL, echo=False)


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

    fabric: Optional[str] = Field(default=None, primary_key=True)


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

    fabric: Optional[str] = Field(default=None, primary_key=True)


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

    fabric: Optional[str] = Field(default=None, primary_key=True)


class SwitchVersionBase(SQLModel):
    """Base class for Switch Versions."""

    version_name: str
    count: int


class SwitchHWVersionsDbModel(SwitchVersionBase, table=True):
    """
    SQLModel table representing the hardware versions of switches.
    Stores each HW version as a separate row.
    """

    fabric: Optional[str] = Field(default=None, primary_key=True)


class SwitchSWVersionsDbModel(SwitchVersionBase, table=True):
    """
    SQLModel table representing the software versions of switches.
    Stores each SW version as a separate row.
    """

    fabric: Optional[str] = Field(default=None, primary_key=True)


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
            tor=0,
        )
        self._init_switch_sw_versions = SwitchHWVersionsDbModel(version_name="ignore", count=0)

        self.switch_roles = {
            "access",
            "aggregation",
            "border",
            "border_gateway",
            "border_gateway_spine",
            "border_gateway_super_spine",
            "border_spine",
            "border_super_spine",
            "core_router",
            "edge_router",
            "leaf",
            "spine",
            "super_spine",
            "tor",
        }

        self.switch_health_status = {"Healthy", "Major", "Minor"}

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
        """
        Update the switch configuration synchronization status,
        incrementing the in_sync or out_of_sync count based on self.sync.

        Add the updated switch configuration to the session.
        """
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.id == 1)
        switch_config = session.exec(statement).first()
        if self.sync is True:
            switch_config.in_sync += 1
        else:
            switch_config.out_of_sync += 1
        session.add(switch_config)

    def update_switch_health(self, session):
        """
        Update the switch health status, incrementing the Healthy, Major, or Minor count
        based on self.health.

        Add the updated switch health to the session.
        """
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.id == 1)
        switch_health = session.exec(statement).first()

        for status in self.switch_health_status:
            if self.health == status:
                setattr(switch_health, status, getattr(switch_health, status) + 1)
                session.add(switch_health)
                break

    def update_switch_roles(self, session):
        """
        Update the switch roles, incrementing the count for the role specified in self.role.

        Add the updated switch roles to the session.
        """
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.id == 1)
        switch_roles = session.exec(statement).first()

        for role in self.switch_roles:
            if self.role == role:
                setattr(switch_roles, role, getattr(switch_roles, role) + 1)
                session.add(switch_roles)
                break

    def update_switch_hw_versions(self, session):
        """
        Update the switch hardware versions, incrementing the count for the hardware version
        specified in self.hw_version.

        Add the updated switch hardware versions to the session.
        """
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
        """
        Update the switch software versions, incrementing the count for the software version
        specified in self.sw_version.

        Add the updated switch software versions to the session.
        """
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
        Persists the changes to the database.
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

    def response(self) -> str:
        """
        Returns the current switch overview data.

        Returns:
            str: The current switch overview data as JSON
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
            switchConfig=switch_config.model_dump(exclude={"id"}),
            switchHealth=switch_health.model_dump(exclude={"id"}),
            switchRoles=switch_roles.model_dump(exclude={"id"}),
            switchHWVersions=hw_response,
            switchSWVersions=sw_response,
        )
        return response.model_dump_json()

    @property
    def health(self) -> str:
        """
        Get the health status of the switch.

        Valid values: "Healthy", "Major", "Minor"
        """
        return self._health

    @health.setter
    def health(self, value: str):
        self._health = value

    @property
    def hw_version(self) -> str:
        """
        The hardware version of the switch.
        """
        return self._hw_version

    @hw_version.setter
    def hw_version(self, value: str):
        self._hw_version = value

    @property
    def role(self) -> str:
        """
        The role of the switch in the fabric.
        """
        return self._role

    @role.setter
    def role(self, value: str):
        self._role = value

    @property
    def sw_version(self) -> str:
        """
        The software version of the switch.
        """
        return self._sw_version

    @sw_version.setter
    def sw_version(self, value: str):
        self._sw_version = value

    @property
    def sync(self) -> bool:
        """
        The synchronization status of the switch.

        True: In sync
        False: Out of sync
        """
        return self._sync

    @sync.setter
    def sync(self, value: bool):
        self._sync = value


class SwitchOverviewHealth:
    """
    # Summary

    Manage the health status of switches in the fabric.

    ## Methods

    - add: Increment the count of the record attribute matching self.fabric and self.health.
    - remove: Decrement the count of the record attribute matching self.fabric and self.health.
    - response_json: Return the current switch health data for self.fabric as JSON.
    - response_model: Return the current switch health data for self.fabric as a model.
    - initialize_db_table: Initialize the database record for self.fabric.

    ## Properties

    - fabric: The fabric name.
    - health: The health status of the switch.  One of Healthy, Major, Minor.
    - session: A database session object.

    ## Example Usage

    ```python
    from sqlmodel import Session, create_engine

    DATABASE_URL = "sqlite:///./nexus_dashboard.db"
    engine = create_engine(DATABASE_URL, echo=False)

    with Session(engine) as session:
        health = SwitchOverviewHealth()
        health.session = session
        health.fabric = "fabric1"
        health.initialize_db_table()
        health.health = "Healthy"
        health.add()
        print(f"response: {health.response_json()}")
    ```
    """

    def __init__(self):
        self._fabric = None
        self._health = None
        self._session = None
        self._model_init = SwitchHealthDbModel(Healthy=0, Major=0, Minor=0)
        self.attributes = {"Healthy", "Major", "Minor"}

    def initialize_db_table(self):
        """
        # Summary

        Initialize the database table associated with this class.
        """
        commit = False
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        switch_health_db = self.session.exec(statement).first()
        if switch_health_db is None:
            self._model_init.fabric = self.fabric
            switch_health_db = SwitchHealthDbModel(**self._model_init.model_dump())
            self.session.add(switch_health_db)
            commit = True

        # Persist the database table
        if commit:
            self.session.commit()

    def validate_properties(self):
        """
        Validate the properties of the class.
        """
        if self._fabric is None:
            raise ValueError("Fabric name not set.")
        if self._session is None:
            raise ValueError("Session not set")

    def add(self):
        """
        # Summary

        - Increment by 1 the count of the record attribute matching self.health.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            if self.health == attribute:
                setattr(record, attribute, getattr(record, attribute) + 1)
                self.session.add(record)
                break
        self.session.commit()

    def remove(self):
        """
        # Summary

        - Decrement by 1 the count of the record attribute matching self.health.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            if self.health == attribute and getattr(record, attribute) > 0:
                setattr(record, attribute, getattr(record, attribute) - 1)
                self.session.add(record)
                break
        self.session.commit()

    def response_json(self) -> str:
        """
        Returns the current switch health data for self.fabric as JSON.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        switch_health = self.session.exec(statement).first()
        return switch_health.model_dump_json(exclude={"fabric"})

    def response_model(self) -> SwitchHealthDbModel:
        """
        Returns the current switch health data for self.fabric as a model.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        switch_health = self.session.exec(statement).first()
        return switch_health

    @property
    def fabric(self) -> str:
        """
        The fabric name.
        """
        return self._fabric

    @fabric.setter
    def fabric(self, value: str):
        self._fabric = value

    @property
    def health(self) -> str:
        """
        Get the health status of the switch.

        Valid values: "Healthy", "Major", "Minor"
        """
        return self._health

    @health.setter
    def health(self, value: str):
        self._health = value

    @property
    def session(self):
        """
        Get the session object.
        """
        return self._session

    @session.setter
    def session(self, value):
        self._session = value


class SwitchOverviewRoles:
    """
    # Summary

    Manage the roles of switches in the fabric.

    ## Methods

    - add: Increment the count of the record attribute matching self.fabric and self.role.
    - remove: Decrement the count of the record attribute matching self.fabric and self.role.
    - response_json: Return the current switch role data for self.fabric as JSON.
    - response_model: Return the current switch role data for self.fabric as a model.
    - initialize_db_table: Initialize the database record for self.fabric.

    ## Properties

    - fabric: The fabric name.
    - role: The role of the switch.  One of access, aggregation, border, border_gateway,
    border_gateway_spine, border_gateway_super_spine, border_spine, border_super_spine,
    core_router, edge_router, leaf, spine, super_spine, tor
    - session: A database session object.

    ## Example Usage

    ```python
    from sqlmodel import Session, create_engine

    DATABASE_URL = "sqlite:///./nexus_dashboard.db"
    engine = create_engine(DATABASE_URL, echo=False)

    with Session(engine) as session:
        roles = SwitchOverviewRoles()
        roles.session = session
        roles.fabric = "fabric1"
        roles.initialize_db_table()
        roles.role = "spine"
        roles.add()
        print(f"response: {roles.response_json()}")
    ```
    """

    def __init__(self):
        self._fabric = None
        self._session = None
        self._model_init = SwitchRolesDbModel(
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
            tor=0,
        )
        self.attributes = {
            "access",
            "aggregation",
            "border",
            "border_gateway",
            "border_gateway_spine",
            "border_gateway_super_spine",
            "border_spine",
            "border_super_spine",
            "core_router",
            "edge_router",
            "leaf",
            "spine",
            "super_spine",
            "tor",
        }

    def initialize_db_table(self):
        """
        Initializes the switch roles database table.
        """
        commit = False
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.fabric == self.fabric)
        switch_roles_db = self.session.exec(statement).first()
        if switch_roles_db is None:
            self._model_init.fabric = self.fabric
            switch_roles_db = SwitchRolesDbModel(**self._model_init.model_dump())
            self.session.add(switch_roles_db)
            commit = True

        # Persist the database table
        if commit:
            self.session.commit()

    def validate_properties(self):
        """
        Validate the properties of the class.
        """
        if self._fabric is None:
            raise ValueError("Fabric name not set.")
        if self._session is None:
            raise ValueError("Session not set")

    def add(self):
        """
        # Summary

        - Increment by 1 the count of the record attribute matching self.role.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            if attribute == self.role:
                setattr(record, attribute, getattr(record, attribute) + 1)
                self.session.add(record)
                break
        self.session.commit()

    def remove(self):
        """
        # Summary

        - Decrement by 1 the count of the record attribute matching self.role.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            if self.role == attribute and getattr(record, attribute) > 0:
                setattr(record, attribute, getattr(record, attribute) - 1)
                self.session.add(record)
                break
        self.session.commit()

    def response_json(self) -> str:
        """
        Returns the current switch health data as JSON.
        """
        self.validate_properties()
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        return model.model_dump_json(exclude={"fabric"})

    def response_model(self) -> SwitchRolesDbModel:
        """
        Returns the current switch health data as a model.
        """
        self.validate_properties()
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        return model

    @property
    def fabric(self) -> str:
        """
        The fabric name.
        """
        return self._fabric

    @fabric.setter
    def fabric(self, value: str):
        self._fabric = value

    @property
    def role(self) -> str:
        """
        Get the role of the switch.

        Valid values: "access", "aggregation", "border", "border_gateway",
        "border_gateway_spine", "border_gateway_super_spine", "border_spine",
        "border_super_spine", "core_router", "edge_router", "leaf", "spine",
        "super_spine", "tor"
        """
        return self._role

    @role.setter
    def role(self, value: str):
        if value not in self.attributes:
            raise ValueError(f"Invalid role: {value}")
        self._role = value

    @property
    def session(self):
        """
        Get the session object.
        """
        return self._session

    @session.setter
    def session(self, value):
        self._session = value


class SwitchOverviewSync:
    """
    # Summary

    Manage the configuration synchronization status of switches in the fabric.

    ## Methods

    - add: Increment the count of the record attribute matching self.fabric and self.sync.
    - remove: Decrement the count of the record attribute matching self.fabric and self.sync.
    - response_json: Return the current switch configuration synchronization data for self.fabric as JSON.
    - response_model: Return the current switch configuration synchronization data for self.fabric as a model.
    - initialize_db_table: Initialize the database record for self.fabric.

    ## Properties

    - fabric: The fabric name.
    - sync: The synchronization status of the switch.  One of in_sync, out_of_sync.
    - session: A database session object.

    ## Example Usage

    ```python
    from sqlmodel import Session, create_engine

    DATABASE_URL = "sqlite:///./nexus_dashboard.db"
    engine = create_engine(DATABASE_URL, echo=False)

    with Session(engine) as session:
        sync = SwitchOverviewSync()
        sync.session = session
        sync.fabric = "fabric1"
        sync.initialize_db_table()
        sync.sync = "in_sync"
        sync.add()
        print(f"response: {sync.response_json()}")
    ```
    """

    def __init__(self):
        self._fabric = None
        self._sync = None
        self._session = None
        self._model_init = SwitchConfigDbModel(in_sync=0, out_of_sync=0)
        self.attributes = {"in_sync", "out_of_sync"}

    def initialize_db_table(self):
        """
        Initializes the switch configuration synchronization database table.
        """
        commit = False
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.fabric == self.fabric)
        switch_config_db = self.session.exec(statement).first()
        if switch_config_db is None:
            self._model_init.fabric = self.fabric
            switch_config_db = SwitchConfigDbModel(**self._model_init.model_dump())
            self.session.add(switch_config_db)
            commit = True

        # Persist the database table
        if commit:
            self.session.commit()

    def validate_properties(self):
        """
        Validate the properties of the class.
        """
        if self._fabric is None:
            raise ValueError("Fabric name not set.")
        if self._session is None:
            raise ValueError("Session not set")

    def add(self):
        """
        # Summary

        - Increment by 1 the count of the record attribute matching self.sync.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            if attribute == self.sync:
                setattr(record, attribute, getattr(record, attribute) + 1)
                self.session.add(record)
                break
        self.session.commit()

    def remove(self):
        """
        # Summary

        - Decrement by 1 the count of the record attribute matching self.sync.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            if self.sync == attribute and getattr(record, attribute) > 0:
                setattr(record, attribute, getattr(record, attribute) - 1)
                self.session.add(record)
                break
        self.session.commit()

    def response_json(self) -> str:
        """
        Returns the current switch sync status data as JSON.
        """
        self.validate_properties()
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        return model.model_dump_json(exclude={"fabric"})

    def response_model(self) -> SwitchConfigDbModel:
        """
        Returns the current switch sync status data as a model.
        """
        self.validate_properties()
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        return model

    @property
    def fabric(self) -> str:
        """
        The fabric name.
        """
        return self._fabric

    @fabric.setter
    def fabric(self, value: str):
        self._fabric = value

    @property
    def sync(self) -> bool:
        """
        Get the sync status of the switch.

        Valid values: in_sync, out_of_sync
        """
        return self._sync

    @sync.setter
    def sync(self, value: bool):
        if value not in self.attributes:
            msg = f"Invalid sync status: {value}. "
            msg += f"Expected one of {','.join(self.attributes)}."
            raise ValueError(msg)
        self._sync = value

    @property
    def session(self):
        """
        Get the session object.
        """
        return self._session

    @session.setter
    def session(self, value):
        self._session = value


if __name__ == "__main__":

    SQLModel.metadata.create_all(engine)

    print("Health: ==========================================================")
    print("Health: add Healthy ==============================================")
    with Session(engine) as db_session:
        health = SwitchOverviewHealth()
        health.session = db_session
        health.fabric = "fabric1"
        health.initialize_db_table()
        health.health = "Healthy"
        health.add()
        print(f"Health: response: {health.response_json()}")
        health_model = health.response_model()
        print("Health: Model access")
        print(f"  fabric:  {health_model.fabric}")
        print(f"  Healthy: {health_model.Healthy}")
        print(f"  Major:   {health_model.Major}")
        print(f"  Minor:   {health_model.Minor}")

    print("Health: remove Healthy, add Minor ================================")
    with Session(engine) as db_session:
        health = SwitchOverviewHealth()
        health.session = db_session
        health.fabric = "fabric1"
        health.initialize_db_table()
        health.health = "Healthy"
        health.remove()
        health.health = "Minor"
        health.add()
        print(f"Health: response: {health.response_json()}")
        health_model = health.response_model()
        print("Health: Model access")
        print(f"  fabric:  {health_model.fabric}")
        print(f"  Healthy: {health_model.Healthy}")
        print(f"  Major:   {health_model.Major}")
        print(f"  Minor:   {health_model.Minor}")

    # Try to remove a health status that is already 0
    print("Health: remove Healthy (it's already 0) ==========================")
    with Session(engine) as db_session:
        health = SwitchOverviewHealth()
        health.session = db_session
        health.fabric = "fabric1"
        health.initialize_db_table()
        health.health = "Healthy"
        health.remove()
        print(f"Health: response: {health.response_json()}")
        health_model = health.response_model()
        print("Health: Model access")
        print(f"  fabric:  {health_model.fabric}")
        print(f"  Healthy: {health_model.Healthy}")
        print(f"  Major:   {health_model.Major}")
        print(f"  Minor:   {health_model.Minor}")

    print()

    print("Roles: ===========================================================")
    print("Roles: add spine =================================================")
    with Session(engine) as db_session:
        roles = SwitchOverviewRoles()
        roles.session = db_session
        roles.fabric = "fabric1"
        roles.initialize_db_table()
        roles.role = "spine"
        roles.add()
        print(f"Roles: response: {roles.response_json()}")
        roles_model = roles.response_model()
        print("Roles: Model access")
        print(f"  fabric: {roles_model.fabric}")
        print(f"  leaf:   {roles_model.leaf}")
        print(f"  spine:  {roles_model.spine}")

    print("Roles: remove spine, add leaf ====================================")
    with Session(engine) as db_session:
        roles = SwitchOverviewRoles()
        roles.session = db_session
        roles.fabric = "fabric1"
        roles.initialize_db_table()
        roles.role = "spine"
        roles.remove()
        roles.role = "leaf"
        roles.add()
        print(f"Roles: response: {roles.response_json()}")
        roles_model = roles.response_model()
        print("Roles: Model access")
        print(f"  fabric: {roles_model.fabric}")
        print(f"  leaf:   {roles_model.leaf}")
        print(f"  spine:  {roles_model.spine}")

    # Try to remove a role that is already 0
    print("Roles: remove spine (it's already 0 ==========================")
    with Session(engine) as db_session:
        roles = SwitchOverviewRoles()
        roles.session = db_session
        roles.fabric = "fabric1"
        roles.initialize_db_table()
        roles.role = "spine"
        roles.remove()
        print(f"Roles: response: {roles.response_json()}")
        roles_model = roles.response_model()
        print("Roles: Model access")
        print(f"  fabric: {roles_model.fabric}")
        print(f"  leaf:   {roles_model.leaf}")
        print(f"  spine:  {roles_model.spine}")

    print()

    print("Sync: ============================================================")
    print("Sync: add in_sync ================================================")
    with Session(engine) as db_session:
        sync = SwitchOverviewSync()
        sync.session = db_session
        sync.fabric = "fabric1"
        sync.initialize_db_table()
        sync.sync = "in_sync"
        sync.add()
        print(f"Sync: response: {sync.response_json()}")
        sync_model = sync.response_model()
        print("Sync: Model access")
        print(f"  fabric:      {sync_model.fabric}")
        print(f"  in_sync:     {sync_model.in_sync}")
        print(f"  out_of_sync: {sync_model.out_of_sync}")

    print("Sync: remove in_sync, add out_of_sync ============================")
    with Session(engine) as db_session:
        sync = SwitchOverviewSync()
        sync.session = db_session
        sync.fabric = "fabric1"
        sync.initialize_db_table()
        sync.sync = "in_sync"
        sync.remove()
        sync.sync = "out_of_sync"
        sync.add()
        print(f"Sync: response: {sync.response_json()}")
        sync_model = sync.response_model()
        print("Sync: Model access")
        print(f"  fabric:      {sync_model.fabric}")
        print(f"  in_sync:     {sync_model.in_sync}")
        print(f"  out_of_sync: {sync_model.out_of_sync}")

    # Try to remove a sync status that is already 0
    print("Sync: remove in_sync (it's already 0 =============================")
    with Session(engine) as db_session:
        sync = SwitchOverviewSync()
        sync.session = db_session
        sync.fabric = "fabric1"
        sync.initialize_db_table()
        sync.sync = "in_sync"
        sync.remove()
        print(f"Sync: response: {sync.response_json()}")
        sync_model = sync.response_model()
        print("Sync: Model access")
        print(f"  fabric:      {sync_model.fabric}")
        print(f"  in_sync:     {sync_model.in_sync}")
        print(f"  out_of_sync: {sync_model.out_of_sync}")

    print()
