import { Page } from "@playwright/test";

export default async function loginAsPlatformAdmin(page: Page): Promise<void> {
    await page.getByRole('button', { name: 'Log in' }).click();
    await page.locator('#username').fill('admin');
    await page.locator('#password').fill('admin');
    await page.getByRole('button', { name: 'Get me in secure!'}).click();
}