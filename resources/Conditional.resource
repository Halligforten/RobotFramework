*** Settings ***
Resource    GetSet.resource

*** Keywords ***
Eos Must Be
    [Arguments]    ${direction}

    ${eos}    Run Keyword    ${INTERFACE} Get Eos
    Should Be Equal    ${eos}    ${direction}

Running Direction Must Be
    [Arguments]    ${direction}

    ${actual_direction}    Run Keyword    ${INTERFACE} Get Running Direction
    Should Be Equal    ${direction}    ${actual_direction} 

Running Direction Must Not Be
    [Arguments]    ${direction}

    ${actual_direction}    Get Running Direction
    Should Not Be Equal    ${direction}    ${actual_direction}    

Position Must Be
    [Arguments]    ${position}

    ${expected_position}    Convert To Integer    ${position}
    ${actual_position}    Get Position
    Should Be Equal    ${expected_position}    ${actual_position}

Error Code Must Be
    [Arguments]    ${expected_error_code}

    ${actual_error_code}    Modbus Get Error Code
    Should Be Equal    ${expected_error_code}    ${actual_error_code}

Must Be Connected
    ${is_connected}    Modbus Is Connected
    Should Be True    ${is_connected}
