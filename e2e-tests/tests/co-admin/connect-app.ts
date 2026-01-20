import { Page } from "@playwright/test";

export default async function connectApplication(sramPage: Page): Promise<void> {
    await sramPage.getByRole('button', { name: 'Applications' }).click();
    await sramPage.getByRole('link', { name: 'Available applications' }).click();
    await sramPage.getByRole('button', { name: 'Request' }).nth(1).click();
    await sramPage.getByRole('textbox', { name: 'Your motivation to request an application connection' }).fill('for testing purposes');
    await sramPage.getByRole('button', { name: 'Send' }).click();
    await sramPage.getByRole('link', { name: 'Connections' }).click();
}