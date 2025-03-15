#!/usr/bin/env python

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ........db import get_session
from .......models.fabric import Fabric
from .......models.inventory import SwitchDbModel, SwitchDiscoverBodyModel, SwitchDiscoverItem

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


def build_db_switch(switch: SwitchDiscoverItem, db_fabric: Fabric) -> SwitchDbModel:
    """
    # Summary

    Given a  SwitchDiscoverBodyModel and a Fabric model,
    return a populated SwitchDbModel object.
    """
    return SwitchDbModel(
        activeSupSlot=1,
        availPorts=48,
        ccStatus="",
        cfsSyslogStatus=0,
        colDBId=0,
        connUnitStatus=0,
        consistencyState=True,
        contact="",
        cpuUsage=0,
        deviceType=db_fabric.FABRIC_TYPE,
        displayHdrs="",
        displayValues="",
        domain="",
        domainID=0,
        elementType="",
        fabricId=db_fabric.id,
        fabricName=db_fabric.FABRIC_NAME,
        fabricTechnology=db_fabric.FF,
        fcoeEnabled=False,
        fex=False,
        fid=0,
        freezeMode="",
        health=0,
        hostName=switch.sysName,
        index=0,
        intentedpeerName="",
        interfaces="",
        ipAddress=switch.ipaddr,
        ipDomain="",
        isEchSupport=False,
        isLan=False,
        isNonNexus=False,
        isPmCollect=False,
        isSharedBorder=False,
        isTrapDelayed=False,
        isVpcConfigured=False,
        is_smlic_enabled=False,
        keepAliveState="",
        lastScanTime=0,
        licenseDetail="",
        licenseViolation=False,
        linkName="",
        logicalName=switch.sysName,
        managable=True,
        mds=False,
        membership="",
        mgmtAddress="",
        memoryUsage=0,
        mode="Normal",
        model="",
        moduleIndexOffset=9999,
        modelType=0,
        name=switch.sysName,
        npvEnabled=False,
        numberOfPorts=48,
        operMode=None,
        operStatus="Minor",
        peer="",
        peerlinkState="",
        peerSerialNumber="",
        peerSwitchDbId=0,
        ports=0,
        present=True,
        primaryIP="",
        primarySwitchDbID=0,
        principal="",
        protoDiscSettings="",
        recvIntf="",
        release=switch.version,
        role="",
        sanAnalyticsCapable=False,
        scope="",
        secondaryIP="",
        secondarySwitchDbID=0,
        sendIntf="",
        serialNumber=switch.serialNumber,
        sharedBorder=False,
        sourceInterface="mgmt0",
        sourceVrf="management",
        standbySupState=0,
        status="",
        switchDbID=None,
        swType="",
        swUUID="DCNM-UUID-TEMP",
        swUUIDId=99999,
        swWwn="",
        swWwnName="",
        sysDescr="",
        systemMode=None,
        uid=0,
        unmanagableCause="",
        upTime=0,
        upTimeNumber=0,
        upTimeStr="",
        usedPorts=0,
        username="",
        vdcId=0,
        vdcName="",
        vdcMac="",
        vendor="cisco",
        version=switch.version,
        vpcDomain=0,
        vrf="management",
        vsanWwn="",
        vsanWwnName="",
        waitForSwitchModeChg=False,
        wwn="",
    )


def build_success_response():
    """
    # Summary

    Build a 200 response body for a successful operation.

    ## Notes

    """
    return {"status": "Success"}


@router.post("/{fabric_name}/inventory/discover")
def v1_inventory_discover_post(*, session: Session = Depends(get_session), fabric_name: str, switch_discovery_body: SwitchDiscoverBodyModel):
    """
    # Summary

    Discover switches for a given fabric_name.

    ## Endpoint

    ### Verb

    POST

    ### Path

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/discover
    """
    db_fabric = session.exec(select(Fabric).where(Fabric.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    fabric_id = db_fabric.id
    # Get all switches in the fabric
    db_switches = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricId == fabric_id)).all()
    # Raise an error if any switches in the discovery body already exist in the fabric
    for db_switch in db_switches:
        if db_switch.serialNumber in [discovery_body.serialNumber for discovery_body in switch_discovery_body.switches]:
            raise HTTPException(status_code=500, detail=f"Switch {db_switch.serialNumber} already exists in fabric {fabric_name}")
    # Add all switches in the discovery body to the fabric
    for discovery_body in switch_discovery_body.switches:
        db_switch = build_db_switch(discovery_body, db_fabric)
        session.add(db_switch)
    session.commit()
    response = build_success_response()
    return response
