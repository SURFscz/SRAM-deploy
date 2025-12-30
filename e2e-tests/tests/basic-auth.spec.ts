import { test, expect } from '@playwright/test';
import callSramForUserLogin from '../helpers/callSramApi';
import loginAsPlatformAdmin from './platform-admin/login';
import seedDatabase from './platform-admin/setup';
import acceptCoInvite from './co-admin/accept-invite';
import connectApplication from './co-admin/connect-app';
import approveApplication from './org-admin/approve-app';
import loginAsCoAdmin from './co-admin/login';
import inviteOrgAdmin from './platform-admin/invite-org-admin';
import acceptOrgAdminInvite from './org-admin/accept-org-invite';
import createCollaboration from './org-admin/create-co';
import loginAsNormalUser from './normal-user/login';
import inviteUserToCo from './co-admin/invite-user';
import acceptCoInviteAsUser from './normal-user/accept-invite';

test.use({
  ignoreHTTPSErrors: true,
});

// See SBS/server/test/seed.py
const cloudApp = {
  url: 'https://cloud',
};

test.describe.serial('Basic Authentication E2E test', () => {
  test('platform-admin: seed db', async ({ page }) => {
    try {
      await page.goto('https://sbs.scz-vm.net/');
      // await page.screenshot({ path: 'start-screenshot.png', fullPage: true });
    
      await loginAsPlatformAdmin(page);
      // await page.screenshot({ path: 'loggedin-screenshot.png', fullPage: true });
      
      // const html = await page.locator('body').innerHTML();
      // console.log('Current HTML:', html);
      await page.getByRole('link', { name: 'Research Access Management' }).waitFor({ state: 'visible' });
      await seedDatabase(page);
      await inviteOrgAdmin(page);

    } catch (error) {
      await page.screenshot({ path: 'debug-screenshot.png', fullPage: true });
      throw error;
    }
  });

  test('org-admin: accept invite and create new co', async ({ page }) => {
    await page.goto('http://localhost:8025/');

    const sramPage = await acceptOrgAdminInvite(page);
    await createCollaboration(sramPage);
    await expect(sramPage.getByRole('heading', { name: 'test collab' })).toBeVisible();
  });
  
  test('co-admin: accept invite and request access to application', async ({ page }) => {
    await page.goto('http://localhost:8025/');

    const sramPage = await acceptCoInvite(page);
  
    await expect(sramPage.getByRole('link', { name: 'SCZ User Two' })).toBeVisible();
  });

  test('user: login to web application while nonexisting', async () => {
    const response = await callSramForUserLogin('user3', cloudApp.url);
    
    console.log(response?.data);
    expect(response?.status).toBe(200);
    expect(response?.data?.status.info).toBe('USER_UNKNOWN');
  });

  test('user: login to SRAM so user exists', async ({ page }) => {
    await page.goto('https://sbs.scz-vm.net/');

    await loginAsNormalUser(page);
  });

  test('user: login to web application while existing in SRAM', async () => {
    const response = await callSramForUserLogin('user3', cloudApp.url);
    
    console.log(response?.data);
    expect(response?.status).toBe(200);
    expect(response?.data?.status.info).toBe('SERVICE_NOT_CONNECTED');
  });

  test('co-admin: request access to application', async ({ page }) => {
    await page.goto('https://sbs.scz-vm.net/');

    await loginAsCoAdmin(page);

    await connectApplication(page);

    await expect(page.getByRole('button', { name: 'Pending' })).toBeVisible();
  });
  
  test('org-admin: approve application access request', async ({ page }) => {
    await page.waitForTimeout(1000);
    await page.goto('http://localhost:8025/');
    await approveApplication(page);
  });
  
  test('co-admin: verify application access approved', async ({ page }) => {
    await page.waitForTimeout(1000);
    await page.goto('https://sbs.scz-vm.net/');

    await loginAsCoAdmin(page);
  
    await page.getByRole('button', { name: 'Open' }).click();
    await page.getByRole('button', { name: 'Applications' }).click();
    await expect(page.getByRole('button', { name: 'Disconnect' })).toBeVisible();
  });
  
  test('user: login to web application after app is connected to co', async () => {
    const response = await callSramForUserLogin('user3', cloudApp.url);
    
    console.log(response?.data);
    expect(response?.status).toBe(200);
    expect(response?.data?.status.info).toBe('SERVICE_NOT_CONNECTED');
  });

  test('co-admin: invite normal user to co', async ({ page }) => {
    await page.goto('https://sbs.scz-vm.net/');

    await loginAsCoAdmin(page);
    await inviteUserToCo(page);
  });

  test('user: accept co invitation', async ({ page }) => {
    await page.goto('http://localhost:8025/');
    await acceptCoInviteAsUser(page);
  });

  test('user: login to web application after user is added to co', async () => {
    const response = await callSramForUserLogin('user3', cloudApp.url);
    
    console.log(response?.data);
    expect(response?.status).toBe(200);
    expect(response?.data?.attributes.eduPersonEntitlement).toContain('urn:mace:surf.nl:x-sram-vm:group:ufra:testcollab');
  })
});
