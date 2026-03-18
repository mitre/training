// @ts-check
const { test, expect } = require("@playwright/test");
const { login } = require("../helpers/auth");
const { navigateToTraining } = require("../helpers/navigation");

/**
 * Helper: select the first available certificate so flags and badges load.
 */
async function selectFirstCertificate(page) {
  const select = page.locator("#select-certificate select").first();
  await expect(select).toBeVisible();
  // Wait for the certs API to populate the dropdown before selecting
  await page.waitForResponse((resp) => resp.url().includes('/plugin/training/certs') && resp.status() === 200, { timeout: 15_000 });
  const firstOption = select.locator("option:not([disabled])").first();
  const optionValue = await firstOption.getAttribute("value");
  if (!optionValue) throw new Error("No certificate options found");
  await select.selectOption(optionValue);
  // Wait for flags to render
  await page.locator(".flag-card").first().waitFor({ state: "visible", timeout: 15_000 });
}

test.describe("Training plugin - flag exercises", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToTraining(page);
  });

  test("should display flag cards after selecting a certificate", async ({ page }) => {
    await selectFirstCertificate(page);
    const flags = page.locator(".flag-card");
    const count = await flags.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("each flag card should display a flag name", async ({ page }) => {
    await selectFirstCertificate(page);
    const flagNames = page.locator(".flag-card-title-name p");
    await expect(flagNames.first()).toBeVisible();
    const text = await flagNames.first().textContent();
    expect(text?.trim().length).toBeGreaterThan(0);
  });

  test("each flag card should display a challenge description", async ({ page }) => {
    await selectFirstCertificate(page);
    const challenges = page.locator(".flag-card-text .has-text-weight-bold");
    await expect(challenges.first()).toBeVisible();
    const text = await challenges.first().textContent();
    expect(text?.trim().length).toBeGreaterThan(0);
  });

  test("flag cards should have a show-more/expand button", async ({ page }) => {
    await selectFirstCertificate(page);
    const expandBtns = page.locator(".flag-show-more-button");
    await expect(expandBtns.first()).toBeVisible();
  });

  test("clicking show-more should expand the flag card", async ({ page }) => {
    await selectFirstCertificate(page);
    const firstCard = page.locator(".flag-card").first();
    const expandBtn = firstCard.locator(".flag-show-more-button");
    await expandBtn.click();

    // The card content should gain the flag-show-more class
    const content = firstCard.locator(".flag-card-content");
    await expect(content).toHaveClass(/flag-show-more/);
  });

  test("clicking show-more again should collapse the flag card", async ({ page }) => {
    await selectFirstCertificate(page);
    const firstCard = page.locator(".flag-card").first();
    const expandBtn = firstCard.locator(".flag-show-more-button");

    // Expand
    await expandBtn.click();
    await expect(firstCard.locator(".flag-card-content")).toHaveClass(/flag-show-more/);

    // Collapse
    await expandBtn.click();
    await expect(firstCard.locator(".flag-card-content")).not.toHaveClass(/flag-show-more/);
  });

  test("flag status icons should be displayed for visible flags", async ({ page }) => {
    await selectFirstCertificate(page);
    // The flag status bar shows flag icons (fas fa-flag or far fa-flag)
    const statusIcons = page.locator(".has-text-centered.mt-4.mb-4 .icon, .has-text-centered .icon");
    await expect(statusIcons.first()).toBeVisible({ timeout: 10_000 });
  });

  test("the first incomplete flag should be marked as active", async ({ page }) => {
    await selectFirstCertificate(page);
    // Active flags get flag-card-content-active or flag-card-title-active classes
    const activeCards = page.locator(".flag-card-content-active, .flag-card-title-active");
    // There should be at least one active card (the first incomplete one)
    const count = await activeCards.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("flag cards should show badge icon in title area", async ({ page }) => {
    await selectFirstCertificate(page);
    const badgeIcons = page.locator(".flag-card-title-badge img");
    await expect(badgeIcons.first()).toBeVisible();
  });

  test("solution guide links should be present on flags that have them", async ({ page }) => {
    await selectFirstCertificate(page);
    // Solution guide links exist but may be hidden for flags without guides
    const guideLinks = page.locator(".solution-guide-link");
    const count = await guideLinks.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });
});
