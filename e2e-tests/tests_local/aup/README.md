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

With the normal local frontend (`yarn dev`) SBS automatically logs in as the hardcoded local user `John Doe` from `SBS/client/src/api/index.js`. Logging out does not help, because opening the app logs `John Doe` back in.

If `John Doe` already accepted the current AUP version, `/aup` redirects away immediately and the AUP page cannot be tested manually in that session. Use the Playwright test for the normal refactor safety check.

To manually see the AUP page anyway, first make sure the local auto-login user has not accepted the current AUP version. For example:

1. Use a local database where `John Doe` has not accepted the current AUP version.
2. Or temporarily change the hardcoded local user in `SBS/client/src/api/index.js` from `urn:john` to a new user, such as `urn:aup_manual_test`.

Then:

1. Start the SBS backend with `ALLOW_MOCK_USER_API=1`.
2. Start the SBS frontend on `http://localhost:3000`.
3. Go to `http://localhost:3000/aup`.
4. Verify the page says hi to the user and shows the acceptable use policy link.
5. Verify the `Onwards` button is disabled.
6. Check `I hereby certify that I have read the acceptable use policy and that I accept it`.
7. Verify the `Onwards` button becomes enabled.
8. Click `Onwards`.
9. Verify the user leaves the AUP page and lands on the configured home page.
