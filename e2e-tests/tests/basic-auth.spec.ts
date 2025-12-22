import { test, expect } from '@playwright/test';
import callSramForUserLogin from '../helpers/callSramApi';
import loginAsPlatformAdmin from './platform-admin/login';
import seedDatabase from './platform-admin/setup';
import createCollaboration from './platform-admin/create-co';
import acceptCoInvite from './co-admin/accept-invite';
import connectApplication from './co-admin/connect-app';
import approveApplication from './platform-admin/approve-app';
import loginAsCoAdmin from './co-admin/login';


test.use({
  ignoreHTTPSErrors: true,
});

// See SBS/server/test/seed.py
const cloudApp = {
  url: 'https://cloud',
};

test.describe.serial('Basic Authentication E2E test', () => {
  test('admin: create new co', async ({ page }) => {
    try {      
      await page.goto('https://sbs.scz-vm.net/');
      await page.screenshot({ path: 'start-screenshot.png', fullPage: true });
    
      await loginAsPlatformAdmin(page);
      await page.screenshot({ path: 'loggedin-screenshot.png', fullPage: true });
      
      const html = await page.locator('body').innerHTML();
      console.log('Current HTML:', html);
      await seedDatabase(page);
      await createCollaboration(page);
  
      await expect(page.getByRole('link', { name: 'test collab' })).toBeVisible();
    } catch (error) {
      await page.screenshot({ path: 'debug-screenshot.png', fullPage: true });
      throw error;
    }
  });
  
  test('co-admin: accept invite and request access to application', async ({ page }) => {
    await page.goto('http://localhost:8025/');

    const sramPage = await acceptCoInvite(page);
  
    await expect(sramPage.getByRole('link', { name: 'SCZ User One' })).toBeVisible();

    await connectApplication(sramPage);

    await expect(sramPage.getByRole('button', { name: 'Pending' })).toBeVisible();
  });
  
  test('admin: approve application access request', async ({ page }) => {
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
  
  test('user: login to web application', async () => {  
    const response = await callSramForUserLogin('user1', cloudApp.url);
    
    console.log(response?.data.attributes.eduPersonEntitlement);
    expect(response?.status === 200)
    expect(response?.data?.attributes.eduPersonEntitlement).toContain('urn:mace:surf.nl:x-sram-vm:group:ufra:testcollab');
  });
});


