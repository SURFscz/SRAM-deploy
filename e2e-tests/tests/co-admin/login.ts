import { Page } from "@playwright/test";

export default async function loginAsCoAdmin(page: Page): Promise<void> {
    await page.getByRole('button', { name: 'Log in' }).click();
    await page.locator('#username').fill('user2');
    await page.locator('#password').fill('user2');
    await page.getByRole('button', { name: 'Get me in secure!'}).click();
}