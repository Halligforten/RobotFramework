*** Settings ***
Library    Ethernet
Library    DateTime
Library    Assertions

Resource    GetSet.Resource


*** Variables ***
${ETHERNET_ACTUATOR_IP_ADDRESS}    192.168.1.10
${ETHERNET_ACTUATOR_MODBUS_PORT}    502

*** Test Cases ***
07719 Ethernet Link Up Test
    [Tags]    07719

    U2L Start Restart
    Sleep    10ms
    Wait Until Keyword Succeeds    4s    10ms
    ...    Can Connect To Ethernet TCP    ${ETHERNET_ACTUATOR_IP_ADDRESS}    ${ETHERNET_ACTUATOR_MODBUS_PORT}

07720 Ethernet Restrict TCP Ports To Modbus
    [Tags]    07720

    ${only_modbus_port_open}    Ethernet Check Only Modbus Tcp Port Open    ${ETHERNET_ACTUATOR_IP_ADDRESS}
    Should Be True    ${only_modbus_port_open}


*** Keywords ***
Can Connect To Ethernet TCP
    [Arguments]    ${ip_address}    ${port}

    ${could_connect}    Ethernet Can Connect Tcp    ${ip_address}    ${port}
    Should Be True    ${could_connect}