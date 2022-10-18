*** Settings ***
Resource    Common.resource

Test Setup    Setup Actuator For Test

*** Test Cases ***
Verify Run EOS In Out In
    Run Until EOS    Out
    Eos Must Be    Out
    Run Until EOS    In
    Eos Must Be    In

Verify Run To A Target Position
    Run Until Target Position    250
    Position Must Be    250   