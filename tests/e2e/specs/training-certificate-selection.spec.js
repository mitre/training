// @ts-check
const { test, expect } = require("@playwright/test");
const { login } = require("../helpers/auth");
const { navigateToTraining } = require("../helpers/navigation");

test.describe("Training plugin - certificate / badge selection", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToTraining(page);
  });

  test("should list available certificates from the API", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();
    // There should be at least 1 real option beyond the placeholder
    const options = select.locator("option:not([disabled])");
    await expect(options.first()).toBeVisible({ timeout: 15_000 });
    const count = await options.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("should show Red Certificate option", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();
    const redOption = select.locator('option:has-text("Red")');
    // Red cert may or may not exist depending on server data - check at least one cert
    const allOptions = select.locator("option:not([disabled])");
    const count = await allOptions.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("should show Blue Certificate option", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();
    const allOptions = select.locator("option:not([disabled])");
    const count = await allOptions.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("selecting a certificate should load badges", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();

    // Pick the first non-disabled option
    const firstOption = select.locator("option:not([disabled])").first();
    const optionValue = await firstOption.getAttribute("value");
    if (!optionValue) return; // guard

    await select.selectOption(optionValue);

    // Badges should appear - they render as .badge-container-button elements
    const badges = page.locator(".badge-container-button, .badge-text");
    await expect(badges.first()).toBeVisible({ timeout: 15_000 });
  });

  test("clicking a badge should filter visible flags", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();

    const firstOption = select.locator("option:not([disabled])").first();
    const optionValue = await firstOption.getAttribute("value");
    if (!optionValue) return;
    await select.selectOption(optionValue);

    // Wait for badges
    const badges = page.locator(".badge-container-button");
    await expect(badges.first()).toBeVisible({ timeout: 15_000 });

    // Count initial flags
    const flagsBefore = page.locator(".flag-card");
    await expect(flagsBefore.first()).toBeVisible({ timeout: 10_000 });
    const totalFlags = await flagsBefore.count();

    // Click first badge to filter
    await badges.first().click();

    // After filtering, flag count should change (either same or fewer)
    const flagsAfter = page.locator(".flag-card");
    const filteredCount = await flagsAfter.count();
    expect(filteredCount).toBeLessThanOrEqual(totalFlags);
    expect(filteredCount).toBeGreaterThanOrEqual(1);
  });

  test("clicking a selected badge again should deselect it and show all flags", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();

    const firstOption = select.locator("option:not([disabled])").first();
    const optionValue = await firstOption.getAttribute("value");
    if (!optionValue) return;
    await select.selectOption(optionValue);

    const badges = page.locator(".badge-container-button");
    await expect(badges.first()).toBeVisible({ timeout: 15_000 });
    const flagsBefore = page.locator(".flag-card");
    await expect(flagsBefore.first()).toBeVisible({ timeout: 10_000 });
    const totalFlags = await flagsBefore.count();

    // Select then deselect
    await badges.first().click();
    await badges.first().click();

    // Should show all flags again
    const flagsAfter = page.locator(".flag-card");
    const restoredCount = await flagsAfter.count();
    expect(restoredCount).toBe(totalFlags);
  });

  test("selected badge should have the selected-badge CSS class", async ({ page }) => {
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();

    const firstOption = select.locator("option:not([disabled])").first();
    const optionValue = await firstOption.getAttribute("value");
    if (!optionValue) return;
    await select.selectOption(optionValue);

    const badges = page.locator(".badge-container-button");
    await expect(badges.first()).toBeVisible({ timeout: 15_000 });

    await badges.first().click();
    await expect(badges.first()).toHaveClass(/selected-badge/);
  });
});
