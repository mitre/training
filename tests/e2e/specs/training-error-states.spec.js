// @ts-check
const { test, expect } = require("@playwright/test");
const { login } = require("../helpers/auth");
const { navigateToTraining } = require("../helpers/navigation");

test.describe("Training plugin - error states", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToTraining(page);
  });

  test("should not display flags before a certificate is selected", async ({ page }) => {
    // Without selecting a certificate, no flags should be visible
    const flags = page.locator(".flag-card");
    await page.waitForTimeout(2_000); // give time for any erroneous rendering
    const count = await flags.count();
    expect(count).toBe(0);
  });

  test("should not display badges before a certificate is selected", async ({ page }) => {
    const badges = page.locator(".badge-container-button");
    await page.waitForTimeout(2_000);
    const count = await badges.count();
    expect(count).toBe(0);
  });

  test("should not show certificate completion banner on initial load", async ({ page }) => {
    const banner = page.locator("h3:has-text('Certificate complete')");
    await page.waitForTimeout(2_000);
    await expect(banner).toBeHidden();
  });

  test("API error should not crash the page when fetching flags", async ({ page }) => {
    // Intercept the flags API to simulate an error
    await page.route("**/plugin/training/flags", (route) => {
      route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ error: "Internal Server Error" }),
      });
    });

    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();

    const firstOption = select.locator("option:not([disabled])").first();
    const optionValue = await firstOption.getAttribute("value");
    if (!optionValue) return;
    await select.selectOption(optionValue);

    // Page should still be functional - heading should remain
    await expect(page.locator("h2:has-text('Training')").first()).toBeVisible();
    // No flags should be shown since the API errored
    await page.waitForTimeout(3_000);
    const flags = page.locator(".flag-card");
    const count = await flags.count();
    expect(count).toBe(0);
  });

  test("API error should not crash the page when fetching certificates", async ({ page }) => {
    // Navigate fresh and intercept the certs API
    await page.route("**/plugin/training/certs", (route) => {
      route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ error: "Internal Server Error" }),
      });
    });

    // Reload to trigger the certs fetch with the mock
    await page.reload();

    // Navigate back to training
    const navItem = page.locator(
      'a:has-text("Training"), .nav-item:has-text("Training"), button:has-text("Training")'
    ).first();
    if ((await navItem.count()) > 0) {
      await navItem.click();
    }

    // Page should still render the heading
    await expect(page.locator("h2:has-text('Training')").first()).toBeVisible({ timeout: 15_000 });
  });

  test("badge images with broken src should fall back to default lock image", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();

    const firstOption = select.locator("option:not([disabled])").first();
    const optionValue = await firstOption.getAttribute("value");
    if (!optionValue) return;
    await select.selectOption(optionValue);

    const badges = page.locator(".badge-icon-img");
    await expect(badges.first()).toBeVisible({ timeout: 15_000 });

    // Badge images have an onerror handler pointing to defaultlock.png
    // Verify the onerror attribute is set on at least the first image
    const onerror = await badges.first().getAttribute("onerror");
    expect(onerror).toContain("defaultlock.png");
  });
});
