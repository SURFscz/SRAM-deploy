import { Page } from "@playwright/test";

export default async function inviteUserToCo(page: Page): Promise<void> {
    await page.getByRole('button', { name: 'Open' }).click();
    await page.getByRole('button', { name: 'Members' }).click();
    await page.getByRole('button', { name: 'Invite members' }).click();
    await page.getByRole('textbox', { name: 'Add email addresses separated' }).fill('user3@scz-vm.net');
    await page.getByRole('textbox', { name: 'Add email addresses separated' }).press('Tab');
    await page.getByRole('button', { name: 'Invite' }).click();
}