import { Page } from "@playwright/test";

export default async function approveApplication(page: Page): Promise<Page> {
    await page.getByRole('link').filter({ hasText: 'Request for new service' }).nth(0).click();
    const page1Promise = page.waitForEvent('popup');
    await page.locator('#preview-html').contentFrame().getByRole('link', { name: 'Login to process this request' }).click();
    const sramPage = await page1Promise;
    sramPage.getByRole('heading', { name: 'Testing MFA log in' }).waitFor({ state: 'visible' });
    await sramPage.locator('#username').fill('user1');
    await sramPage.locator('#password').fill('user1');
    await sramPage.getByRole('button', { name: 'Get me in secure!' }).click();
    await sramPage.getByRole('cell', { name: 'test collab' }).click();
    await sramPage.getByRole('button', { name: 'Accept' }).click();
    await sramPage.getByRole('button', { name: 'Confirm' }).click();
    return sramPage;
}