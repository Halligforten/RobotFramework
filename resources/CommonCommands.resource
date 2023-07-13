
*** Settings ***
Resource    ${INTERFACE}Commands.resource
Resource    Waiting.resource

*** Keywords ***
Test Setup
    Run Keyword    ${INTERFACE} Test Setup

Test Teardown
    Run Keyword    ${INTERFACE} Test Teardown

Run Until EOS
    [Arguments]    ${direction}
    
    Run Keyword    ${INTERFACE} Start Stop
    Run Keyword    ${INTERFACE} Start Run ${direction}
    Wait Until EOS Is    ${direction}
    Wait Until Stopped
    Run Keyword    ${INTERFACE} Start Stop