import { Page } from "@playwright/test";
import { login } from "../../helpers/login";

export default async function acceptOrgAdminInvite(page: Page): Promise<Page> {
    await page.goto('http://localhost:8025/');
    await page.getByRole('link').filter({ hasText: 'Invitation to join organisation Academia Franekerensis' }).nth(0).click();
    const page1Promise = page.waitForEvent('popup');
    await page.locator('#preview-html').contentFrame().getByRole('link', { name: 'Accept invitation' }).click();
    const sramPage = await page1Promise;
    await sramPage.getByRole('button', { name: 'Log in to accept the invite' }).click();
    await sramPage.getByRole('heading', { name: 'Testing MFA log in' }).waitFor({ state: 'visible' });
    await login(sramPage, 'user1', 'user1');
    await sramPage.getByText('I hereby certify that I have').click();
    await sramPage.getByRole('button', { name: 'Onwards' }).click();
    await sramPage.getByText('Accept, show me the organisation').click();
    return sramPage;
}
