from .......models.fabric import Fabric as FabricModel
from .......models.inventory import SwitchDbModel, SwitchDiscoverItem, SwitchResponseModel


def build_db_switch(switch: SwitchDiscoverItem, db_fabric: FabricModel) -> SwitchDbModel:
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


def build_response_switch(db_switch: SwitchDbModel) -> SwitchResponseModel:
    """
    # Summary

    Build a SwitchResponseModel object from a SwitchDbModel object.

    TODO:   This function should be moved to a common location and shared
            with internal_inventory_get.py
    """
    return SwitchResponseModel(
        activeSupSlot=db_switch.activeSupSlot,
        availPorts=db_switch.availPorts,
        ccStatus=db_switch.ccStatus,
        cfsSyslogStatus=db_switch.cfsSyslogStatus,
        colDBId=db_switch.colDBId,
        connUnitStatus=db_switch.connUnitStatus,
        consistencyState=db_switch.consistencyState,
        contact=db_switch.contact,
        cpuUsage=db_switch.cpuUsage,
        deviceType=db_switch.deviceType,
        displayHdrs=db_switch.displayHdrs,
        displayValues=db_switch.displayValues,
        domain=db_switch.domain,
        domainID=db_switch.domainID,
        elementType=db_switch.elementType,
        fabricId=db_switch.fabricId,
        fabricName=db_switch.fabricName,
        fabricTechnology=db_switch.fabricTechnology,
        fcoeEnabled=db_switch.fcoeEnabled,
        fex=db_switch.fex,
        fexMap={},
        fid=db_switch.fid,
        freezeMode=db_switch.freezeMode,
        health=db_switch.health,
        hostName=db_switch.hostName,
        index=db_switch.index,
        intentedpeerName=db_switch.intentedpeerName,
        interfaces=db_switch.interfaces,
        ipAddress=db_switch.ipAddress,
        ipDomain=db_switch.ipDomain,
        isEchSupport=db_switch.isEchSupport,
        isLan=db_switch.isLan,
        isNonNexus=db_switch.isNonNexus,
        isPmCollect=db_switch.isPmCollect,
        isSharedBorder=db_switch.isSharedBorder,
        isTrapDelayed=db_switch.isTrapDelayed,
        isVpcConfigured=db_switch.isVpcConfigured,
        is_smlic_enabled=db_switch.is_smlic_enabled,
        keepAliveState=db_switch.keepAliveState,
        lastScanTime=db_switch.lastScanTime,
        licenseDetail=db_switch.licenseDetail,
        licenseViolation=db_switch.licenseViolation,
        linkName=db_switch.linkName,
        location=db_switch.location,
        logicalName=db_switch.logicalName,
        managable=db_switch.managable,
        mds=db_switch.mds,
        membership=db_switch.membership,
        memoryUsage=db_switch.memoryUsage,
        mgmtAddress=db_switch.mgmtAddress,
        mode=db_switch.mode,
        model=db_switch.model,
        modelType=db_switch.modelType,
        modules=db_switch.modules,
        moduleIndexOffset=db_switch.moduleIndexOffset,
        monitorMode=db_switch.monitorMode,
        name=db_switch.name,
        npvEnabled=db_switch.npvEnabled,
        numberOfPorts=db_switch.numberOfPorts,
        network=db_switch.network,
        nonMdsModel=db_switch.nonMdsModel,
        operMode=db_switch.operMode,
        operStatus=db_switch.operStatus,
        peer=db_switch.peer,
        peerlinkState=db_switch.peerlinkState,
        peerSerialNumber=db_switch.peerSerialNumber,
        peerSwitchDbId=db_switch.peerSwitchDbId,
        ports=db_switch.ports,
        present=db_switch.present,
        primaryIP=db_switch.primaryIP,
        primarySwitchDbID=db_switch.primarySwitchDbID,
        principal=db_switch.principal,
        protoDiscSettings=db_switch.protoDiscSettings,
        recvIntf=db_switch.recvIntf,
        release=db_switch.release,
        role="",
        sanAnalyticsCapable=db_switch.sanAnalyticsCapable,
        scope=db_switch.scope,
        secondaryIP=db_switch.secondaryIP,
        secondarySwitchDbID=db_switch.secondarySwitchDbID,
        sendIntf=db_switch.sendIntf,
        serialNumber=db_switch.serialNumber,
        sharedBorder=db_switch.sharedBorder,
        sourceInterface=db_switch.sourceInterface,
        sourceVrf=db_switch.sourceVrf,
        standbySupState=db_switch.standbySupState,
        status=db_switch.status,
        switchDbID=db_switch.switchDbID,
        switchRole=db_switch.switchRole,
        switchRoleEnum=db_switch.switchRoleEnum,
        swType=db_switch.swType,
        swUUID=db_switch.swUUID,
        swUUIDId=db_switch.swUUIDId,
        swWwn=db_switch.swWwn,
        swWwnName=db_switch.swWwnName,
        sysDescr=db_switch.sysDescr,
        systemMode=db_switch.systemMode,
        uid=db_switch.uid,
        unmanagableCause=db_switch.unmanagableCause,
        upTime=db_switch.upTime,
        upTimeNumber=db_switch.upTimeNumber,
        upTimeStr=db_switch.upTimeStr,
        usedPorts=db_switch.usedPorts,
        username=db_switch.username,
        vdcId=db_switch.vdcId,
        vdcName=db_switch.vdcName,
        vdcMac=db_switch.vdcMac,
        vendor=db_switch.vendor,
        version=db_switch.version,
        vpcDomain=db_switch.vpcDomain,
        vrf=db_switch.vrf,
        vsanWwn=db_switch.vsanWwn,
        vsanWwnName=db_switch.vsanWwnName,
        waitForSwitchModeChg=db_switch.waitForSwitchModeChg,
        wwn=db_switch.wwn,
    )
