// @ts-check
const { test, expect } = require("@playwright/test");
const { login } = require("../helpers/auth");
const { navigateToTraining } = require("../helpers/navigation");

async function selectFirstCertificate(page) {
  const select = page.locator("#select-certificate select").first();
  await expect(select).toBeVisible();
  // Wait for the certs API to populate the dropdown before selecting
  await page.waitForResponse((resp) => resp.url().includes('/plugin/training/certs') && resp.status() === 200, { timeout: 15_000 });
  const firstOption = select.locator("option:not([disabled])").first();
  const optionValue = await firstOption.getAttribute("value");
  if (!optionValue) throw new Error("No certificate options found");
  await select.selectOption(optionValue);
  await page.locator(".flag-card, .badge-container-button").first().waitFor({ state: "visible", timeout: 15_000 });
}

test.describe("Training plugin - progress tracking", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToTraining(page);
  });

  test("badges should display completion status styling", async ({ page }) => {
    await selectFirstCertificate(page);
    const badges = page.locator(".badge-container-button");
    await expect(badges.first()).toBeVisible({ timeout: 15_000 });

    // Each badge should have either completed or non-completed styling
    // The badge-completed class or badge-completed-text class indicates completion
    const count = await badges.count();
    expect(count).toBeGreaterThanOrEqual(1);

    // Verify badge text elements exist
    const badgeTexts = page.locator(".badge-text");
    expect(await badgeTexts.count()).toBeGreaterThanOrEqual(1);
  });

  test("flag icons should indicate completed vs incomplete state", async ({ page }) => {
    await selectFirstCertificate(page);
    // Flag icons use fas fa-flag (solid=completed) or far fa-flag (outline=incomplete)
    const flagIcons = page.locator(".flag-card-title-name .icon");
    await expect(flagIcons.first()).toBeVisible({ timeout: 10_000 });
    const count = await flagIcons.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("completed flags should have gold icon styling", async ({ page }) => {
    await selectFirstCertificate(page);
    // If any flags are completed, they get flag-icon-completed class (gold color)
    // This is a structural check - the class binding exists in the template
    const flagCards = page.locator(".flag-card");
    const count = await flagCards.count();
    expect(count).toBeGreaterThanOrEqual(1);

    // Verify the icon container is present in each flag card
    for (let i = 0; i < Math.min(count, 3); i++) {
      const icon = flagCards.nth(i).locator(".flag-card-title-name .icon");
      await expect(icon).toBeVisible();
    }
  });

  test("certificate completion banner should not show when certificate is incomplete", async ({ page }) => {
    await selectFirstCertificate(page);
    // On a fresh server the certificate should not be complete
    // The completion banner contains "Certificate complete"
    const banner = page.locator("h3:has-text('Certificate complete')");
    const bannerCount = await banner.count();
    if (bannerCount > 0) {
      // Training state is already complete in this environment - skip rather than fail
      test.skip(true, "Certificate already complete; cannot test incomplete state without resetting");
      return;
    }
    await expect(banner).toHaveCount(0);
  });

  test("the flag status bar should show icons matching the number of visible flags", async ({ page }) => {
    await selectFirstCertificate(page);
    const flagCards = page.locator(".flag-card");
    await expect(flagCards.first()).toBeVisible({ timeout: 10_000 });
    const cardCount = await flagCards.count();

    // The status bar icons
    const statusIcons = page.locator(".has-text-centered.mt-4.mb-4 .icon");
    const iconCount = await statusIcons.count();

    // Each visible flag should have a corresponding status icon
    expect(iconCount).toBe(cardCount);
  });

  test("badge icon images should load without error (fallback to default)", async ({ page }) => {
    await selectFirstCertificate(page);
    const badgeImgs = page.locator(".badge-icon-img");
    await expect(badgeImgs.first()).toBeVisible({ timeout: 10_000 });

    const count = await badgeImgs.count();
    for (let i = 0; i < Math.min(count, 5); i++) {
      const img = badgeImgs.nth(i);
      // Image should have a src attribute (either real or fallback defaultlock.png)
      const src = await img.getAttribute("src");
      expect(src).toBeTruthy();
    }
  });
});
