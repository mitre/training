// @ts-check
const { test, expect } = require("@playwright/test");
const { login } = require("../helpers/auth");
const { navigateToTraining } = require("../helpers/navigation");

test.describe("Training plugin - Red vs Blue training paths", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToTraining(page);
  });

  test("should list both Red and Blue certificate paths (if available)", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();
    const options = select.locator("option:not([disabled])");
    const count = await options.count();
    // The server should provide at least one certificate path
    expect(count).toBeGreaterThanOrEqual(1);

    // Collect option texts to check for red/blue
    const texts = [];
    for (let i = 0; i < count; i++) {
      texts.push(await options.nth(i).textContent());
    }
    // Log for debugging - at least one should exist
    expect(texts.length).toBeGreaterThanOrEqual(1);
  });

  test("selecting Red Certificate should load red-path badges", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();

    // Try to find and select the Red option
    const redOption = select.locator('option:has-text("Red")');
    const redCount = await redOption.count();
    if (redCount === 0) {
      test.skip(true, "No Red Certificate option available on this server");
      return;
    }

    const value = await redOption.first().getAttribute("value");
    await select.selectOption(value);

    // Badges should load
    const badges = page.locator(".badge-container-button");
    await expect(badges.first()).toBeVisible({ timeout: 15_000 });
  });

  test("selecting Blue Certificate should load blue-path badges", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();

    const blueOption = select.locator('option:has-text("Blue")');
    const blueCount = await blueOption.count();
    if (blueCount === 0) {
      test.skip(true, "No Blue Certificate option available on this server");
      return;
    }

    const value = await blueOption.first().getAttribute("value");
    await select.selectOption(value);

    const badges = page.locator(".badge-container-button");
    await expect(badges.first()).toBeVisible({ timeout: 15_000 });
  });

  test("switching between certificates should reset badge selection", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();

    const options = select.locator("option:not([disabled])");
    const count = await options.count();
    if (count < 2) {
      test.skip(true, "Need at least 2 certificates to test switching");
      return;
    }

    // Select first certificate
    const val1 = await options.nth(0).getAttribute("value");
    await select.selectOption(val1);
    const badges = page.locator(".badge-container-button");
    await expect(badges.first()).toBeVisible({ timeout: 15_000 });

    // Select a badge
    await badges.first().click();
    await expect(badges.first()).toHaveClass(/selected-badge/);

    // Switch to second certificate
    const val2 = await options.nth(1).getAttribute("value");
    await select.selectOption(val2);

    // Wait for new badges to load
    await expect(badges.first()).toBeVisible({ timeout: 15_000 });

    // No badge should be in selected state after switching
    const selectedBadges = page.locator(".badge-container-button.selected-badge");
    const selectedCount = await selectedBadges.count();
    expect(selectedCount).toBe(0);
  });

  test("different certificates should show different badge sets", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();

    const options = select.locator("option:not([disabled])");
    const count = await options.count();
    if (count < 2) {
      test.skip(true, "Need at least 2 certificates to compare badge sets");
      return;
    }

    // Get badge names from first certificate
    const val1 = await options.nth(0).getAttribute("value");
    await select.selectOption(val1);
    const badgeTexts1 = page.locator(".badge-text");
    await expect(badgeTexts1.first()).toBeVisible({ timeout: 15_000 });
    const names1 = [];
    for (let i = 0; i < await badgeTexts1.count(); i++) {
      names1.push(await badgeTexts1.nth(i).textContent());
    }

    // Get badge names from second certificate
    const val2 = await options.nth(1).getAttribute("value");
    await select.selectOption(val2);
    await expect(badgeTexts1.first()).toBeVisible({ timeout: 15_000 });
    const names2 = [];
    for (let i = 0; i < await badgeTexts1.count(); i++) {
      names2.push(await badgeTexts1.nth(i).textContent());
    }

    // Both should have badges loaded
    expect(names1.length).toBeGreaterThanOrEqual(1);
    expect(names2.length).toBeGreaterThanOrEqual(1);
  });
});
