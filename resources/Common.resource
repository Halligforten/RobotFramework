*** Settings ***
Resource    Conditional.resource
Resource    Waiting.resource
Resource    RunHandling.resource
Resource    GetSet.resource

*** Variables ***
${DEFAULT_SPEED}    100

*** Keywords ***
Setup Actuator For Test
    Set Parameter    SPEED    ${DEFAULT_SPEED}
    Run Until EOS    In

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