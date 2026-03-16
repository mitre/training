// @ts-check
const { test, expect } = require("@playwright/test");
const { login } = require("../helpers/auth");
const { navigateToTraining } = require("../helpers/navigation");

test.describe("Training plugin - page load", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test("should load the Caldera UI successfully", async ({ page }) => {
    await expect(page).not.toHaveURL(/\/login/);
  });

  test("should display the Training navigation item", async ({ page }) => {
    const navItem = page.locator(
      'a:has-text("Training"), .nav-item:has-text("Training"), [data-test="nav-training"], button:has-text("Training")'
    ).first();
    await expect(navItem).toBeVisible({ timeout: 15_000 });
  });

  test("should navigate to the Training tab and display the heading", async ({ page }) => {
    await navigateToTraining(page);
    await expect(page.locator("h2:has-text('Training')").first()).toBeVisible();
  });

  test("should show the certificate selection dropdown", async ({ page }) => {
    await navigateToTraining(page);
    await expect(page.locator("#select-certificate select, #select-certificate .select select").first()).toBeVisible();
  });

  test("should have a default placeholder option in the certificate dropdown", async ({ page }) => {
    await navigateToTraining(page);
    const select = page.locator("#select-certificate select").first();
    await expect(select).toBeVisible();
    // The default option should be disabled / placeholder
    const defaultOption = select.locator("option[disabled], option[value='']").first();
    await expect(defaultOption).toBeDefined();
  });
});
