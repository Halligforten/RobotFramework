*** Settings ***
Library    Modbus.ModbusTcp

Resource    Waiting.resource

*** Keywords ***
Modbus Tcp Test Setup
    Wait Until Connected

Modbus Tcp Test Teardown
    Modbus Disconnect
