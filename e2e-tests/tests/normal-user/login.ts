import { Page } from "@playwright/test";

export default async function loginAsNormalUser(page: Page): Promise<void> {
    await page.getByRole('button', { name: 'Log in' }).click();
    await page.locator('#username').fill('user3');
    await page.locator('#password').fill('user3');
    await page.getByRole('button', { name: 'Get me in secure!'}).click();
    await page.getByText('I hereby certify that I have').click();
    await page.getByRole('button', { name: 'Onwards' }).click();
}