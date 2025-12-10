# E2E Tests

## Intro
The Playwright tests in this folder are meant to complement the existing manual acceptance tests: where those acceptance tests test the integration with the whole IAM landscape surrounding it (EduTeams / EngineBlock proxy, existing IdP's, etc.), these E2E tests test SRAM more in isolation. It uses the `./start-vm` script to spin up all necessary docker containers for a full SRAM environment running in https://sbs.scz-vm.net/, where the users defined in `SRAM-deploy/roles/oidc-op/templates/sram_users.json.j2` and `SRAM-deploy/roles/oidc-op/templates/sram_passwd.json.j2` are available. It also deploys a local mailpit server where all the emails to all different users will go at http://localhost:8025/. The available seed test data, such as the available applications, is given in `SBS/server/test/seed.py`.

## Quick Start
```bash
SRAM-deploy $ ./start-vm
SRAM-deploy $ cd e2e-tests
SRAM-deploy/e2e-tests $ yarn install
SRAM-deploy/e2e-tests $ yarn playwright test --ui
```

