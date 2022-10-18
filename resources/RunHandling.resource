*** Settings ***
Resource    GetSet.resource

*** Keywords ***
Run
    [Arguments]    ${direction}

    Run Keyword    Run ${direction}

Run Out
    Set Parameter    RUN_CMD    1

Run In
    Set Parameter    RUN_CMD    2

Run To Position
    [Arguments]    ${target_position}

    Set Parameter    TARGET_POSITION    ${target_position}
    Set Parameter    RUN_CMD    3

Stop Running
    Set Parameter    RUN_CMD    0