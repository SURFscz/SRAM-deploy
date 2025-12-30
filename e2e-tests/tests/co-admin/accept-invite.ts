import { Page } from "@playwright/test";
import { login } from "../../helpers/login";

export default async function acceptCoInvite(page: Page): Promise<Page> {
    await page.getByRole('link').filter({ hasText: 'Invitation to join collaboration test collab' }).nth(0).click();
    const page1Promise = page.waitForEvent('popup');
    await page.locator('#preview-html').contentFrame().getByRole('link', { name: 'Join this collaboration' }).click();
    const sramPage = await page1Promise;
    await sramPage.getByRole('button', { name: 'Log in to accept the invite' }).click();
    await sramPage.getByRole('heading', { name: 'Testing MFA log in' }).waitFor({ state: 'visible' });
    await login(sramPage, 'user2', 'user2');
    await sramPage.getByText('I hereby certify that I have').click();
    await sramPage.getByRole('button', { name: 'Onwards' }).click();
    await sramPage.getByText('I agree to the organisation acceptable use policy').click();
    await sramPage.getByRole('button', { name: 'Proceed to test collab' }).click();
    return sramPage;
}