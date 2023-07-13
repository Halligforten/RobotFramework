*** Settings ***
Library    Modbus.ModbusTcp
Library    Usb2Lin
Resource    Waiting.resource

*** Variables ***
${DEFAULT_IP_ADDRESS}    192.168.1.10
${DEFAULT_CONNECTION_TIMEOUT}    1

*** Keywords ***
Initialize Ethernet
    [Arguments]    ${ip_address}=${DEFAULT_IP_ADDRESS}    ${timeout}=${DEFAULT_CONNECTION_TIMEOUT}

    Wait Until Connected

Deinitialize Ethernet
    Modbus Stop Heartbeat
    Modbus Disconnect

Get Ready For Running
    Modbus Start Heartbeat    250
    Wait Until No Error

Run
    [Arguments]    ${direction}

    Run Keyword    Run ${direction}

Run Out
    Modbus Run Out

Run In
    Modbus Run In

Run To Position
    [Arguments]    ${target_position}

    Modbus Run To Position    ${target_position}

Stop Running
    Modbus Stop Run

Get Eos
    ${eos}    Modbus Get Eos Status
    [Return]    ${eos}

Get Running Direction
    ${run_dir}    Modbus Get Running Status
    [Return]    ${run_dir}

Get Position
    ${position}    Modbus Get Position
    [Return]    ${position}

Get Error Code
    ${error_code}    Modbus Get Error Code
    [Return]    ${error_code}
    
Read Regsiter
    [Arguments]    ${address}
    
    ${value}    Modbus Read Register    ${address}
    [Return]    ${value}

Write Register
    [Arguments]    ${address}    ${value}
    
    Modbus Write Register    ${address}    ${value}

U2L Start Restart
    U2l FindAllLinakDevices
    ${device}    U2l GetFirstDevice
    U2l CloseDevice
    Sleep   200ms
    U2l OpenSpecificDevice    ${device}
    Lin UseSync    ${True}
    Sleep   100ms
    ${hardware_id}    Lin ConnectAnyLinConfig    ${True}
    Lin ActivateConfig