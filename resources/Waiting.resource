*** Settings ***
Library    Modbus.ModbusTcp

Resource    Conditional.resource
Resource    GetSet.resource

*** Variables ***
${DEFAULT_TIMEOUT}    10s
${DEFAULT_RETRY_INTERVAL}    100ms

*** Keywords ***
# Wait Until Connected
#     [Arguments]    ${timeout}=${DEFAULT_TIMEOUT}    ${retry_interval}=${DEFAULT_RETRY_INTERVAL}
#     Wait Until Keyword Succeeds    ${timeout}    ${retry_interval}    Run Keywords
#     ...    Modbus Connect Ethernet    192.168.1.10    1    AND
#     ...    Must Be Connected
Wait Until Connected
    [Arguments]    ${timeout}=${DEFAULT_TIMEOUT}    ${retry_interval}=${DEFAULT_RETRY_INTERVAL}
    Wait Until Keyword Succeeds    ${timeout}    ${retry_interval}    Run Keywords
    ...    Modbus Tcp Attempt To Connect    192.168.1.10    1    10    AND
    ...    Must Be Connected

Wait Until No Error
    [Arguments]    ${timeout}=${DEFAULT_TIMEOUT}    ${retry_interval}=${DEFAULT_RETRY_INTERVAL}

    Wait Until Keyword Succeeds    ${timeout}    ${retry_interval}    Run Keywords
    ...    Modbus Clear Error    AND
    ...    Error Code Must Be    no_error

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
    ...    Running Direction Must Not Be    stop

Wait Until Stopped
    [Arguments]    ${timeout}=${DEFAULT_TIMEOUT}    ${retry_interval}=${DEFAULT_RETRY_INTERVAL}

    Wait Until Keyword Succeeds    ${timeout}    ${retry_interval}
    ...    Running Direction Must Be    stop