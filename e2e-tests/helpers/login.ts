import { Page } from "@playwright/test";

export async function login(page: Page, username: string, password: string): Promise<void> {
    await page.locator('#username').fill(username);
    await page.locator('#password').fill(password);
    await page.getByRole('button', { name: 'Get me in secure!'}).click();
}

export async function loginOnHomePage(page: Page, username: string, password: string): Promise<void> {
    await page.getByRole('button', { name: 'Log in' }).click();
    await login(page, username, password);
}
