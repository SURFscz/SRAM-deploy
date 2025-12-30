import { Page } from "@playwright/test";

export default async function createCollaboration(page: Page): Promise<void> {
    await page.getByRole('button', { name: 'Collaborations' }).click();
    await page.getByRole('button', { name: 'Add collaboration' }).click({ force: true });
    await page.getByRole('textbox', { name: 'The unique name of a' }).fill('test collab');
    await page.getByRole('textbox', { name: 'Provide a clear description' }).fill('for testing purposes');
    await page.getByRole('textbox', { name: 'Add email addresses separated' }).fill('user2@scz-vm.net');
    await page.getByText('Make me admin of this').click();
    await page.getByRole('button', { name: 'Add an image' }).click();
    await page.getByRole('button', { name: 'Select from gallery' }).click();
    await page.getByRole('img', { name: 'Logo' }).first().click();
    await page.getByRole('button', { name: 'Apply' }).click();
    await page.getByRole('button', { name: 'Apply' }).click();
    await page.getByRole('button', { name: 'Change image' }).waitFor({ state: 'visible' });
    await page.getByRole('button', { name: 'Save' }).click();
    await page.getByText('Collaboration test collab was').waitFor({ state: 'visible' });
}