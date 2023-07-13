*** Settings ***
Resource    Common.resource

Test Setup    Modbus Tcp Test Setup
Test Teardown    Modbus Tcp Test Teardown

*** Test Cases ***
Test 1
    Run Until EOS    in
    Run Until EOS    out

