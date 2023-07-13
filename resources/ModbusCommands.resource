*** Settings ***
Library    Modbus.Modbus${MODBUS_INTERFACE}
Resource    Modbus${MODBUS_INTERFACE}.resource

*** Keywords ***
Modbus Test Setup
    Run Keyword    Modbus${MODBUS_INTERFACE} Test Setup
    Modbus Start Heartbeat    250
    Wait Until No Error

Modbus Test Teardown
    Run Keyword    Modbus${MODBUS_INTERFACE} Test Teardown

Modbus Start Stop
    Modbus Stop Run

Modbus Start Run Out
    Modbus Run Out

Modbus Start Run In
    Modbus Run In

Modbus Get Eos
    ${eos}    Modbus Get Eos Status
    [Return]    ${eos}

Modbus Get Running Direction
    ${run_dir}    Modbus Get Running Status
    [Return]    ${run_dir}
