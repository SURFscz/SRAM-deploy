import { test, expect } from '@playwright/test';

test.use({
  ignoreHTTPSErrors: true,
});

test('admin: update org settings and create new co', async ({ page }) => {
  await page.goto('https://sbs.scz-vm.net/');

  // Log in as admin
  await page.getByRole('button', { name: 'Log in' }).click();
  await page.locator('#username').fill('admin');
  await page.locator('#password').fill('admin');
  await page.getByRole('button', { name: 'Get me in secure!'}).click();

  // Seed the database
  await page.getByRole('button').filter({ hasText: /^$/ }).click();
  await page.getByRole('link', { name: 'System' }).click();
  await page.getByRole('button', { name: 'Seed' }).click();
  await page.getByRole('button', { name: 'Run' }).first().click();
  await page.getByRole('button', { name: 'Confirm' }).click();
  await page.getByText('I hereby certify that I have').click();
  await page.getByRole('button', { name: 'Onwards' }).click();

  // Add new labels
  await page.getByRole('link', { name: 'Home' }).click();
  await page.getByRole('searchbox', { name: 'Search organisations...' }).fill('Academia Franekerensis');
  await page.getByRole('cell', { name: 'Academia Franekerensis' }).click();
  await page.getByRole('button', { name: 'Details & settings' }).click();
  await page.getByRole('link', { name: 'Labels' }).click();
  await page.getByRole('textbox').fill('new label');
  await page.getByRole('link', { name: '+ Add label' }).click();
  await page.getByRole('textbox').nth(1).fill('new label for cloud unit');
  await page.locator('.units-inner__placeholder').nth(1).click();
  const locator = page.locator('.units-inner__option').filter({ hasText: 'Cloud Unit' });
  await locator.click({ force: true });
  await page.getByRole('button', { name: 'Update' }).click();

  // Update messages
  await page.getByRole('link', { name: 'Messaging' }).click();
  await page.getByRole('button', { name: 'Markdown' }).click();
  await page.getByTestId('text-area').fill('New default message for testing, new collaborations');
  await page.getByRole('textbox', { name: 'Please join us, at this new' }).fill('New default message for testing, new invitations');
  await page.getByRole('textbox', { name: 'Organisational department of' }).fill('Acceptance Tester');
  await page.getByRole('button', { name: 'Update' }).click();
  await expect(page.getByRole('heading', { name: 'Messaging settings' })).toBeVisible();
  
  // Create new collaboration
  await page.getByRole('button', { name: 'Collaborations' }).click();
  await page.getByRole('button', { name: 'Add collaboration' }).click({ force: true });
  await page.getByRole('textbox', { name: 'The unique name of a' }).fill('test collab');
  await page.getByRole('textbox', { name: 'Provide a clear description' }).fill('for testing purposes');
  await page.getByRole('textbox', { name: 'Add email addresses separated' }).fill('user1@scz-vm.net');
  await page.getByText('Make me admin of this').click();
  await page.getByRole('button', { name: 'Add an image' }).click();
  await page.getByRole('button', { name: 'Select from gallery' }).click();
  await page.getByRole('img', { name: 'Logo' }).first().click();
  await page.getByRole('button', { name: 'Apply' }).click();
  await page.getByRole('button', { name: 'Apply' }).click();
  await expect(page.getByRole('button', { name: 'Change image' })).toBeVisible();
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByRole('heading', { name: 'test collab' })).toBeVisible();
  await page.getByRole('link', { name: 'Home' }).click();
  await page.getByRole('searchbox', { name: 'Search organisations...' }).fill('Academia Franekerensis');
  await page.getByRole('link', { name: 'Academia Franekerensis' }).click();
  await expect(page.getByRole('link', { name: 'test collab' })).toBeVisible();
})

test('co-admin: accept invite and request access to application', async ({ page }) => {
  // Open mailpit and accept invite
  await page.goto('http://localhost:8025/');
  await page.getByRole('link').filter({ hasText: 'Invitation to join collaboration test collab' }).nth(0).click();
  const page1Promise = page.waitForEvent('popup');
  await page.locator('#preview-html').contentFrame().getByRole('link', { name: 'Join this collaboration' }).click();
  const sramPage = await page1Promise;

  // Log in to SRAM to accept invite
  await sramPage.getByRole('button', { name: 'Log in to accept the invite' }).click();
  await expect(sramPage.getByRole('heading', { name: 'Testing MFA log in' })).toBeVisible();
  await sramPage.locator('#username').fill('user1');
  await sramPage.locator('#password').fill('user1');
  await sramPage.getByRole('button', { name: 'Get me in secure!' }).click();
  await sramPage.getByText('I hereby certify that I have').click();
  await sramPage.getByRole('button', { name: 'Onwards' }).click();
  await sramPage.getByText('I agree to the organisation acceptable use policy').click();
  await sramPage.getByRole('button', { name: 'Proceed to test collab' }).click();
  await expect(sramPage.getByRole('link', { name: 'SCZ User One' })).toBeVisible();

  // Request access to application
  await sramPage.getByRole('button', { name: 'Applications' }).click();
  await sramPage.getByRole('link', { name: 'Available applications' }).click();
  await sramPage.getByRole('button', { name: 'Request' }).nth(1).click();
  await sramPage.getByRole('textbox', { name: 'Your motivation to request an application connection' }).fill('for testing purposes');
  await sramPage.getByRole('button', { name: 'Send' }).click();
  await sramPage.getByRole('link', { name: 'Connections' }).click();
  await expect(sramPage.getByRole('button', { name: 'Pending' })).toBeVisible();
})

test('admin: approve application access request', async ({ page }) => {
  // Open mailpit and click on request link
  await page.goto('http://localhost:8025/');
  await page.getByRole('link').filter({ hasText: 'Request for new service' }).nth(0).click();
  const page1Promise = page.waitForEvent('popup');
  await page.locator('#preview-html').contentFrame().getByRole('link', { name: 'Login to process this request' }).click();
  const sramPage = await page1Promise;

  await expect(sramPage.getByRole('heading', { name: 'Testing MFA log in' })).toBeVisible();
  await sramPage.locator('#username').fill('admin');
  await sramPage.locator('#password').fill('admin');
  await sramPage.getByRole('button', { name: 'Get me in secure!' }).click();
  await sramPage.getByRole('cell', { name: 'test collab' }).click();
  await sramPage.getByRole('button', { name: 'Accept' }).click();
  await sramPage.getByRole('button', { name: 'Confirm' }).click();
})

test('co-admin: verify application access approved', async ({ page }) => {
  // Log in to SRAM
  await page.goto('https://sbs.scz-vm.net/');
  await page.getByRole('button', { name: 'Log in' }).click();
  await page.locator('#username').fill('user1');
  await page.locator('#password').fill('user1');
  await page.getByRole('button', { name: 'Get me in secure!' }).click();

  // Verify application access approved
  await page.getByRole('button', { name: 'Open' }).click();
  await page.getByRole('button', { name: 'Applications' }).click();
  await expect(page.getByRole('button', { name: 'Disconnect' })).toBeVisible();
});