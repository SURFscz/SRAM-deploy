import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:8025/');
  await page.getByRole('link').filter({ hasText: 'Invitation to join collaboration test collab' }).click();
  const page1Promise = page.waitForEvent('popup');
  await page.locator('#preview-html').contentFrame().getByRole('link', { name: 'Join this collaboration' }).click();
  const page1 = await page1Promise;
  await page1.getByRole('button', { name: 'Advanced' }).click();
  await page1.getByRole('link', { name: 'Proceed to sbs.scz-vm.net (' }).click();
  await page1.getByRole('button', { name: 'Log in to accept the invite' }).click();
  await page1.getByRole('button', { name: 'Advanced' }).click();
  await page1.getByRole('link', { name: 'Proceed to oidc-op.scz-vm.net' }).click();
  await page1.getByRole('textbox', { name: 'Secret MFA sauce' }).click();
  await page1.getByRole('textbox', { name: 'Secret MFA sauce' }).fill('user1');
  await page1.getByRole('button', { name: 'Get me in secure!' }).click();
  await page1.locator('label').getByRole('img').click();
  await page1.getByRole('button', { name: 'Onwards' }).click();
  await page1.locator('label').getByRole('img').click();
  await page1.getByRole('button', { name: 'Proceed to test collab' }).click();
  await expect(page1.getByRole('link', { name: 'SCZ User One' })).toBeVisible();
});