# Local AUP Playwright Test

This folder contains local-only Playwright tests for the SBS AUP page. These tests live outside the default `tests` folder, so they are excluded from the default `yarn playwright test --ui` run.

## Run the AUP Test

Start the local SBS backend with mock users enabled:

```bash
SBS $ source .venv/bin/activate
SBS $ ALLOW_MOCK_USER_API=1 EVENTLET_HUB=poll PROFILE=local PYDEVD_USE_CYTHON=NO PYDEVD_USE_FRAME_EVAL=NO PYTHONUNBUFFERED=1 CONFIG=$(pwd)/server/config/test_config.yml python -m server
```

Start the local SBS frontend:

```bash
SBS/client $ yarn dev
```

Then run the local Playwright test:

```bash
SRAM-deploy/e2e-tests $ yarn test:local
```

For the Playwright UI:

```bash
SRAM-deploy/e2e-tests $ yarn test:local:ui
```

The default URL is:

- Frontend: `http://localhost:3000`

The test runs against the local React app and mocks the AUP API calls in Playwright. This keeps the test focused on `SBS/client/src/pages/aup/Aup.jsx` and avoids depending on the hardcoded local `John Doe` session.

The script points Playwright at the local frontend:

- `SBS_LOCAL_BASE_URL=http://localhost:3000`

Override it when needed:

```bash
SBS_LOCAL_BASE_URL=http://localhost:3001 yarn test:local
```

## Manual AUP Test

1. Start the SBS backend with `ALLOW_MOCK_USER_API=1`.
2. Start the SBS frontend on `http://localhost:3000`.
3. Open the app in a fresh browser session or clear the current local session.
4. In local mode SBS automatically logs in as the hardcoded local user `John Doe`. Logging out does not help for this manual test, because opening the app again logs `John Doe` back in.
5. If `John Doe` already accepted the AUP, `/aup` redirects away immediately. To manually see the AUP page again, use a database where `John Doe` has not accepted the current AUP version, or change the hardcoded local user in `SBS/client/src/api/index.js` temporarily.
6. Go to `http://localhost:3000/aup`.
7. Verify the page says hi to the user and shows the acceptable use policy link.
8. Verify the `Onwards` button is disabled.
9. Check `I hereby certify that I have read the acceptable use policy and that I accept it`.
10. Verify the `Onwards` button becomes enabled.
11. Click `Onwards`.
12. Verify the user lands on the home page.
