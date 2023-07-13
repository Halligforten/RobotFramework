*** Settings ***
Library    Modbus.Modbus${MODBUS_INTERFACE}

Resource    Conditional.resource
Resource    Waiting.resource
Resource    GetSet.resource

*** Keywords ***
Modbus Tcp Test Setup
    Initialize Ethernet
    Get Ready For Running

Modbus Tcp Test Teardown
    Deinitialize Ethernet
    
Run Until EOS
    [Arguments]    ${direction}
    
    Stop Running
    Run    ${direction}
    Wait Until EOS Is    ${direction}
    Wait Until Stopped
    Stop Running

Run Until Target Position
    [Arguments]    ${target_position}

    Run To Position    ${target_position}
    Wait Until Running
    Wait Until Stopped
