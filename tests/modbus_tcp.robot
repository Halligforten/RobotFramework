
*** Settings ***
Resource    CommonCommands.resource

Test Setup    Test Setup
Test Teardown    Test Teardown

*** Variables ***
${INTERFACE}    Modbus
${MODBUS_INTERFACE}    Tcp

*** Test Cases ***
Verify Run Full Stroke From EOS-out To EOS-in
    Run Until EOS    out
    Run Until EOS    in
