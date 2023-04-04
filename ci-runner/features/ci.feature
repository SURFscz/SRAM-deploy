@relyingparty
Feature: Test RP logins

  @test1
  Scenario Outline: RP Test login
     Given we visit https://rp.ci-runner.sram.surf.nl/
       and we choose SRAM CI Runner Test IdP
       and we arrive at idp.ci-runner.sram.surf.nl
      When we login as <user>:<password>
      Then sub is <sub>

  Examples:
        | user    | password | sub                                                            |
        | student | student  | 8e7811387bc200409b395a7a156826875a4248f9@acc.sram.eduteams.org |
        | admin   | admin    | 98d4d0ddd179f57c0cbbf06ae2d7094522b21eab@acc.sram.eduteams.org |

  @test2
  Scenario Outline: RP Test login against all claims in file
     Given we visit https://rp.ci-runner.sram.surf.nl/
       and we choose SRAM CI Runner Test IdP
       and we arrive at idp.ci-runner.sram.surf.nl
      When we login as <user>:<password>
      Then tokens are <file>

  Examples:
        | user    | password | file                   |
        | student | student  | ci-runner/student.json |
        | admin   | admin    | ci-runner/admin.json   |
