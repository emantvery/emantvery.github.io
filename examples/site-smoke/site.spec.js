const { test, expect } = require("playwright/test");

test("homepage links to a readable technical article", async ({ page }) => {
  await page.goto("/");
  const article = page.getByRole("link", { name: /挂号接口：从业务状态到测试用例/ });
  await expect(article).toBeVisible();
  await article.click();
  await expect(page).toHaveURL(/appointment-api-testing\.html$/);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "挂号接口：从业务状态到测试用例"
  );
});

test("mobile navigation opens, follows the project link, and has no page overflow", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/tech/");
  const menu = page.getByRole("button", { name: "菜单" });
  await menu.click();
  await expect(menu).toHaveAttribute("aria-expanded", "true");
  await page.getByRole("navigation", { name: "主导航" }).getByRole("link", { name: "项目" }).click();
  await expect(page).toHaveURL(/\/#projects$/);
  await expect(page.getByRole("heading", { name: "项目实践" })).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  expect(overflow).toBe(false);
});

test("theme toggle changes the visible theme", async ({ page }) => {
  await page.goto("/tech/pytest-api-tests.html");
  const before = await page.locator("html").getAttribute("data-theme");
  await page.getByRole("button", { name: "切换明暗主题" }).click();
  await expect(page.locator("html")).toHaveAttribute(
    "data-theme",
    before === "dark" ? "light" : "dark"
  );
});

test("technical pages have working local links and no viewport overflow", async ({ page, request }) => {
  const paths = [
    "/",
    "/tech/",
    "/tech/appointment-api-testing.html",
    "/tech/pytest-api-tests.html",
    "/tech/ai-application-testing.html",
    "/tech/playwright-ui-tests.html",
    "/tech/sql-state-check.html",
  ];
  for (const width of [390, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    for (const pathname of paths) {
      await page.goto(pathname);
      expect(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)).toBe(false);
      if (width !== 390) continue;
      for (const href of await page.locator("a[href]").evaluateAll((links) => links.map((link) => link.href))) {
        const target = new URL(href);
        if (target.origin !== new URL(page.url()).origin) continue;
        const response = await request.get(target.pathname);
        expect(response.status(), `Broken link from ${pathname}: ${href}`).toBe(200);
        if (target.hash && target.pathname === pathname) {
          const anchor = await page.locator(target.hash).count();
          expect(anchor, `Missing anchor from ${pathname}: ${href}`).toBeGreaterThan(0);
        }
      }
    }
  }
});
