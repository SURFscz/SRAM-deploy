import { Page } from "@playwright/test";

export default async function seedDatabase(page: Page): Promise<void> {
    await page.goto('https://sbs.scz-vm.net/system/seed');
    await page.getByRole('button', { name: 'Run' }).first().click();
    await page.getByRole('button', { name: 'Confirm' }).click();
    await page.getByText('I hereby certify that I have').click();
    await page.getByRole('button', { name: 'Onwards' }).click();
    await page.getByRole('link', { name: 'Home' }).click();
}