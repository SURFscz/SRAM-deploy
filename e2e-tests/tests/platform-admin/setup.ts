import { Page } from "@playwright/test";

export default async function seedDatabase(page: Page): Promise<void> {
    await page.getByRole('button').filter({ hasText: /^$/ }).click();
    await page.getByRole('link', { name: 'System' }).click();
    await page.getByRole('button', { name: 'Seed' }).hover();
    await page.screenshot({ path: 'with-highlight.png' });
    await page.getByRole('button', { name: 'Seed' }).click();
    await page.getByRole('button', { name: 'Run' }).first().click();
    await page.getByRole('button', { name: 'Confirm' }).click();
    await page.getByText('I hereby certify that I have').click();
    await page.getByRole('button', { name: 'Onwards' }).click();
    await page.getByRole('link', { name: 'Home' }).click();
}