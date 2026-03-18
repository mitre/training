/**
 * Navigation helpers for reaching plugin tabs inside Caldera / Magma.
 */

/**
 * Navigate to the Training plugin tab in the Magma Vue app.
 * The training plugin registers under the "Training" nav item.
 */
async function navigateToTraining(page) {
  // Magma renders a left-nav or top-nav with plugin names.
  // Click the Training entry to load the plugin view.
  const navItem = page.locator(
    'a:has-text("Training"), .nav-item:has-text("Training"), [data-test="nav-training"], button:has-text("Training")'
  ).first();
  await navItem.waitFor({ state: "visible", timeout: 15_000 });
  await navItem.click();

  // Wait for the training page root element to appear
  await page.locator("#trainingPage, h2:has-text('Training')").first().waitFor({
    state: "visible",
    timeout: 15_000,
  });
}

module.exports = { navigateToTraining };
