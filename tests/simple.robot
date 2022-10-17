
*** Settings ***
Library    Actuator

*** Variables ***

*** Test Cases ***
TestCase1
    Log    "Hello World!"
    ${position}    Read    POSITION
    Log    ${position}
    