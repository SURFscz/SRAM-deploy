import { Page } from "@playwright/test";

export default async function inviteOrgAdmin(page: Page): Promise<void> {
    await page.getByRole('button', { name: 'Organisations' }).click();
    await page.getByRole('link', { name: 'Academia Franekerensis' }).click();
    await page.getByRole('button', { name: 'Organisation admins' }).click();
    await page.getByRole('button', { name: 'Invite admins' }).click();
    // await page.getByRole('textbox', { name: 'Add email addresses separated' }).click();
    await page.getByRole('textbox', { name: 'Add email addresses separated' }).fill('user1@scz-vm.net');
    // await page.locator('.inner-email-field').click();
    await page.getByRole('textbox', { name: 'Add email addresses separated' }).press('Tab');
    await page.getByText('Organisation Manager').click();
    await page.getByRole('option', { name: 'Organisation Admin' }).click();
    await page.getByRole('button', { name: 'Invite' }).click();
};