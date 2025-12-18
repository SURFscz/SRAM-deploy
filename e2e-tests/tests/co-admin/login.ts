import { Page } from "@playwright/test";

export default async function loginAsCoAdmin(page: Page): Promise<void> {
    await page.getByRole('button', { name: 'Log in' }).click();
    await page.locator('#username').fill('user1');
    await page.locator('#password').fill('user1');
    await page.getByRole('button', { name: 'Get me in secure!'}).click();
}