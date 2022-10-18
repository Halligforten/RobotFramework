*** Settings ***
Resource    Conditional.resource
Resource    GetSet.resource

*** Variables ***
${DEFAULT_TIMEOUT}    10s
${DEFAULT_RETRY_INTERVAL}    100ms

*** Keywords ***
Wait Until EOS Is
    [Arguments]    ${direction}    ${timeout}=${DEFAULT_TIMEOUT}    ${retry_interval}=${DEFAULT_RETRY_INTERVAL}
    
    Wait Until Keyword Succeeds    ${timeout}    ${retry_interval}
    ...    Eos Must Be    ${direction}

Wait Until Running Direction Is
    [Arguments]    ${direction}    ${timeout}=${DEFAULT_TIMEOUT}    ${retry_interval}=${DEFAULT_RETRY_INTERVAL}

    Wait Until Keyword Succeeds    ${timeout}    ${retry_interval}
    ...    Running Direction Must Be    ${direction}

Wait Until Running
    [Arguments]    ${timeout}=${DEFAULT_TIMEOUT}    ${retry_interval}=${DEFAULT_RETRY_INTERVAL}

    Wait Until Keyword Succeeds    ${timeout}    ${retry_interval}
    ...    Running Direction Must Not Be    Stopped

Wait Until Stopped
    [Arguments]    ${timeout}=${DEFAULT_TIMEOUT}    ${retry_interval}=${DEFAULT_RETRY_INTERVAL}

    Wait Until Keyword Succeeds    ${timeout}    ${retry_interval}
    ...    Running Direction Must Be    Stopped