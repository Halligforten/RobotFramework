*** Settings ***
Library    Actuator

*** Keywords ***
Get Eos
    ${eos}    Get Parameter    STATUS_EOS
    ${eos}    Evaluate    {0:"None",1:"Out",2:"In"}.get(${eos})
    [Return]    ${eos}

Get Running Direction
    ${run_dir}    Get Parameter    STATUS_RUN_DIR
    ${run_dir}    Evaluate    {0:"Stopped",1:"Out",2:"In"}.get(${run_dir})
    [Return]    ${run_dir}

Get Position
    ${position}    Get Parameter    POSITION
    [Return]    ${position}
    
Get Parameter
    [Arguments]    ${ini_name}
    
    ${value}    Read    ${ini_name}
    [Return]    ${value}

Set Parameter
    [Arguments]    ${ini_name}    ${value}
    
    Write    ${ini_name}    ${value}