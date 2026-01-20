import { Page } from "@playwright/test";

export default async function acceptAup(page: Page): Promise<void> {
    await page.getByText('I hereby certify that I have').click();
    await page.getByRole('button', { name: 'Onwards' }).click();
}