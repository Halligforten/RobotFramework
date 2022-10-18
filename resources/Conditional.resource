*** Settings ***
Resource    GetSet.resource

*** Keywords ***
Eos Must Be
    [Arguments]    ${direction}

    ${eos}    Get Eos
    Should Be Equal    ${eos}    ${direction}

Running Direction Must Be
    [Arguments]    ${direction}

    ${actual_direction}    Get Running Direction
    Should Be Equal    ${direction}    ${actual_direction} 

Running Direction Must Not Be
    [Arguments]    ${direction}

    ${actual_direction}    Get Running Direction
    Should Not Be Equal    ${direction}    ${actual_direction}    

Position Must Be
    [Arguments]    ${position}

    ${expected_position}    Convert To Integer    ${position}
    ${actual_position}    Get Parameter    POSITION
    Should Be Equal    ${expected_position}    ${actual_position}

