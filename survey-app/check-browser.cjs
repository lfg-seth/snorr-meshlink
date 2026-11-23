/* Optional acceptance check. A fresh loopback simulator and disposable Chromium profile. */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
const assert = require("node:assert/strict");
const fs = require("node:fs/promises");
const path = require("node:path");
const readline = require("node:readline");
const { spawn, execFileSync } = require("node:child_process");
const { once } = require("node:events");

async function main() {
  const root = path.dirname(__dirname),
    dataParent = path.join(root, "local-data", "survey-qa");
  await fs.mkdir(dataParent, { recursive: true });
  const dir = await fs.mkdtemp(path.join(dataParent, "run-"));
  const area = path.join(
    root,
    "local-data",
    "direct-hop-survey",
    "map",
    "area.json",
  );
  let hasArea = false;
  try {
    await fs.mkdir(path.join(dir, "map"));
    await fs.copyFile(area, path.join(dir, "map", "area.json"));
    hasArea = true;
  } catch (e) {
    if (e.code !== "ENOENT") throw e;
  }
  execFileSync(
    process.env.PYTHON || "python",
    [path.join(__dirname, "test_survey.py"), "--browser-fixture", dir],
    { windowsHide: true },
  );
  const proc = spawn(
    process.env.PYTHON || "python",
    [
      path.join(__dirname, "server.py"),
      "--source",
      "simulation",
      "--port",
      "0",
      "--data-dir",
      dir,
    ],
    { cwd: root, windowsHide: true, stdio: ["ignore", "pipe", "inherit"] },
  );
  const exited = once(proc, "exit");
  let browser;
  try {
    const lines = readline.createInterface({ input: proc.stdout });
    const [line] = await Promise.race([
      once(lines, "line"),
      exited.then(() => {
        throw Error("QA host exited before startup");
      }),
    ]);
    const url = line.match(/http:\/\/127\.0\.0\.1:\d+/)[0];
    browser = await chromium.launch({
      headless: true,
      executablePath: process.env.CHROMIUM_PATH || undefined,
    });
    const ctx = await browser.newContext({
      viewport: { width: 382, height: 580 },
      hasTouch: true,
    });
    let page = await ctx.newPage(),
      errors = [];
    const attach = () => {
      page.on("pageerror", (e) => errors.push(e.message));
      page.on("console", (m) => {
        if (m.type() === "error" && !m.text().includes("404"))
          errors.push(m.text());
      });
    };
    attach();
    const state = async () => (await fetch(url + "/api/state")).json();
    const textIs = (selector, value) =>
      page.waitForFunction(
        ([s, v]) => document.querySelector(s)?.textContent === v,
        [selector, value],
        { timeout: 10000 },
      );
    const check = async (name, fn) => {
      await fn();
      console.log("PASS " + name);
    };
    await page.goto(url);
    await textIs("#source", "Simulation");
    if (hasArea) await textIs("#mapready", "Offline area");
    await check("Simulator starts through the mobile UI", async () => {
      await page.locator("#go").click();
      await textIs("#run", "running");
      assert.equal((await state()).state.mode, "survey");
    });
    for (const [width, height] of [
      [382, 580],
      [382, 618],
      [594, 368],
      [594, 406],
      [669, 867],
      [669, 902],
      [951, 585],
      [951, 620],
      [385, 571],
      [385, 609],
      [320, 620],
      [744, 1024],
      [1133, 744],
      [1440, 900],
    ]) {
      await page.setViewportSize({ width, height });
      await page.evaluate(() => window.scrollTo(0, 0));
      const layout = await page.evaluate(() => ({
        overflow: document.documentElement.scrollWidth - innerWidth,
        width: document.querySelector("#map").clientWidth,
        buttons: ["#go", "#stop"].map((s) => {
          const b = document.querySelector(s).getBoundingClientRect();
          return [b.left, b.right, b.height];
        }),
      }));
      assert.ok(
        layout.overflow <= 1,
        "Overflow " + width + " " + JSON.stringify(layout),
      );
      assert.ok(layout.width > 200);
      for (const [l, r, h] of layout.buttons)
        assert.ok(l >= 0 && r <= width + 1 && h >= 44);
      assert.equal(await page.locator("#run").textContent(), "running");
      if ([382, 951, 1440].includes(width))
        await page.screenshot({
          path: path.join(dir, "viewport-" + width + "-" + height + ".png"),
        });
    }
    console.log("PASS 14 Duo, Split View, iPad and desktop viewport sizes");
    await check(
      "Full-page map, trusted touch pan and anchored two-finger pinch",
      async () => {
        await page.setViewportSize({ width: 382, height: 580 });
        await page.locator("#openMap").click();
        await page.locator("#mapdialog[open]").waitFor();
        const canvas = page.locator("#map"),
          box = await canvas.boundingBox();
        assert.equal(Math.round(box.width), 382);
        assert.equal(Math.round(box.height), 580);
        const cdp = await ctx.newCDPSession(page);
        const touch = (type, points) =>
          cdp.send("Input.dispatchTouchEvent", {
            type,
            touchPoints: points.map(([id, x, y]) => ({ id, x, y })),
          });
        const gesture = async (points) => {
          await touch("touchStart", points[0]);
          for (const pts of points.slice(1)) await touch("touchMove", pts);
          await touch("touchEnd", []);
        };
        await gesture([[[1, 140, 240]], [[1, 140, 285]], [[1, 165, 305]]]);
        assert.equal(
          await page.locator("#follow").getAttribute("aria-pressed"),
          "false",
        );
        await gesture([
          [
            [1, 120, 250],
            [2, 200, 250],
          ],
          [
            [1, 100, 250],
            [2, 220, 250],
          ],
          [
            [1, 80, 250],
            [2, 240, 250],
          ],
        ]);
        await page.waitForFunction(() =>
          document.querySelector("#scale").textContent.startsWith("z15"),
        );
        await gesture([
          [
            [1, 80, 250],
            [2, 240, 250],
          ],
          [
            [1, 100, 250],
            [2, 220, 250],
          ],
          [
            [1, 120, 250],
            [2, 200, 250],
          ],
        ]);
        await page.waitForFunction(() =>
          document.querySelector("#scale").textContent.startsWith("z14"),
        );
        await page.screenshot({ path: path.join(dir, "full-map-382.png") });
        await page.setViewportSize({ width: 594, height: 368 });
        assert.equal(Math.round((await canvas.boundingBox()).height), 368);
        await page.locator("#maplayers summary").click();
        await page.locator("#direction").selectOption("downlink");
        await page.locator("#maplayers summary").click();
        await page.locator("#closeMap").click();
        assert.equal(await page.locator("#mapdialog").isVisible(), false);
        assert.equal((await state()).state.run_state, "running");
        await cdp.detach();
        await page.setViewportSize({ width: 1440, height: 900 });
      },
    );
    await check("Map zoom, follow and signal selection", async () => {
      await page.locator("#zoomIn").click();
      await page.waitForFunction(() =>
        document.querySelector("#scale").textContent.startsWith("z15"),
      );
      await page.locator("#follow").click();
      assert.equal(
        await page.locator("#follow").getAttribute("aria-pressed"),
        "true",
      );
      await page.locator("#direction").selectOption("downlink");
      await page.locator("#metric").selectOption("rssi_dbm");
      await textIs("#range", "−135 to −70 dBm");
    });
    await check(
      "Target framing, sample filter and repeater coordinates",
      async () => {
        await page.setViewportSize({ width: 382, height: 580 });
        await page.locator("#openMap").click();
        await textIs("#mapTargetId", "SIM-R01");
        await textIs("#siteOrigin", "Simulator coordinates");
        await page.locator("#maplayers summary").click();
        await page.locator("#filter").selectOption("SIM-R02");
        await page.locator("#maplayers summary").click();
        await page.locator("#locateTarget").click();
        assert.equal((await state()).state.target_id, "SIM-R01");
        await page.waitForFunction(() => {
          const canvas = document.querySelector("#map");
          const pixels = canvas
            .getContext("2d")
            .getImageData(0, 0, canvas.width, canvas.height).data;
          for (let i = 0; i < pixels.length; i += 4) {
            if (
              pixels[i] === 255 &&
              pixels[i + 1] === 215 &&
              pixels[i + 2] === 126
            )
              return true;
          }
          return false;
        });
        await page.screenshot({
          path: path.join(dir, "selected-repeater-382.png"),
        });
        await page.locator("#closeMap").click();
        await page.setViewportSize({ width: 1440, height: 900 });
        await page.locator("#scenario").selectOption("Timeouts");
        await page.waitForFunction(
          () =>
            document
              .querySelector("#mapReply")
              .textContent.startsWith("Timed out"),
          null,
          { timeout: 16000 },
        );
        await page.locator("#scenario").selectOption("Strong link");
        await page.waitForFunction(
          () =>
            document
              .querySelector("#mapReply")
              .textContent.startsWith("Replied"),
          null,
          { timeout: 16000 },
        );
        const missing = await ctx.newPage();
        try {
          await missing.route("**/api/state", async (route) => {
            const response = await route.fetch(),
              snapshot = await response.json();
            delete snapshot.sites[snapshot.state.target_id];
            await route.fulfill({ response, json: snapshot });
          });
          await missing.goto(url);
          await missing
            .getByText("Site position unknown", { exact: true })
            .waitFor();
          assert.ok(await missing.locator("#locateTarget").isDisabled());
        } finally {
          await missing.close();
        }
      },
    );
    await check(
      "Basemap outage leaves commands and recording available",
      async () => {
        await page.locator("#scenario").selectOption("Map outage");
        await textIs("#mapready", "Outage · grid");
        assert.ok((await state()).recording);
        await page.locator("#scenario").selectOption("Strong link");
      },
    );
    await check("Browser closed while host continues attempts", async () => {
      const a = (await state()).state.counts.attempts;
      await page.close();
      await new Promise((r) => setTimeout(r, 6600));
      assert.ok((await state()).state.counts.attempts > a);
      page = await ctx.newPage();
      attach();
      await page.goto(url);
      await textIs("#run", "running");
      await page.locator("#control").click();
      await page.waitForFunction(
        () => document.querySelector("#control").hidden,
      );
    });
    await check("GPS fault and explicit resume", async () => {
      await page.locator('[data-view="readout"]').click();
      await page.locator("#scenario").selectOption("No GPS");
      await textIs("#run", "paused");
      await page.locator("#scenario").selectOption("Strong link");
      await page.waitForFunction(() =>
        document.querySelector("#facts").textContent.includes("Fix ·"),
      );
      assert.equal((await state()).state.run_state, "paused");
      await page.locator("#go").click();
      await textIs("#run", "running");
      await page.locator("#go").click();
      await textIs("#run", "paused");
    });
    await check(
      "Short keyboard viewport; applied numeric settings and target",
      async () => {
        await page.setViewportSize({ width: 382, height: 330 });
        await page.locator('[data-view="setup"]').click();
        const field = page.locator('[name="min_interval_ms"]');
        await field.fill("2200");
        await field.focus();
        await field.scrollIntoViewIfNeeded();
        assert.equal(await field.inputValue(), "2200");
        await page.locator("#settings button").click();
        await page.waitForFunction(() =>
          document
            .querySelector("#alert")
            .textContent.includes("Settings applied"),
        );
        assert.equal((await state()).state.settings.min_interval_ms, 2200);
        await page.locator("#target").selectOption("SIM-R02");
        await page.waitForFunction(() =>
          document.querySelector("#facts").textContent.includes("SIM-R02"),
        );
        await textIs("#mapTargetId", "SIM-R02");
        await textIs("#mapReply", "No result this segment");
      },
    );
    await check("Replay, export and immutable history", async () => {
      await page.locator("#stop").click();
      await textIs("#run", "stopped");
      await page.locator("#testName").fill("Simulator drive test");
      await page.locator("#testNoteInput").fill("Example field notes");
      await page.locator('#finishTest button[type="submit"]').click();
      await page.locator("#finishDialog").waitFor({ state: "hidden" });
      await page.locator('[data-view="journal"]').click();
      await textIs("#testNotes p", "Example field notes");
      await page.locator("#events button").first().click();
      assert.ok(
        (await page.locator("#detail").innerText()).includes("received_ms"),
      );
      const csv = await (
        await fetch(
          new URL(await page.locator("#csv").getAttribute("href"), url),
        )
      ).text();
      assert.ok(csv.includes("uplink_snr_db") && csv.includes("SIM-R01"));
      const raw = await (
        await fetch(
          new URL(await page.locator("#raw").getAttribute("href"), url),
        )
      ).text();
      assert.ok(
        raw
          .trim()
          .split("\n")
          .map(JSON.parse)
          .some((r) => r.event.name === "result"),
      );
      await page.locator("#replay").click();
      await page.locator("#step").click();
      await page.locator("#play").click();
      await textIs("#play", "Pause playback");
      await page.locator("#exitReplay").click();
      assert.equal((await state()).state.run_state, "stopped");
    });
    await check(
      "Long recording paginates without accumulating DOM rows",
      async () => {
        await page.locator('[data-view="journal"]').click();
        await page.locator("#refreshSessions").click();
        const records = await (await fetch(url + "/api/sessions")).json();
        await page
          .locator("#session")
          .selectOption(records.find((s) => s.events >= 10000).id);
        await page.waitForFunction(
          () => document.querySelectorAll("#events button").length === 60,
        );
        const first = await page.locator("#windowInfo").innerText();
        await page.locator("#older").click();
        await page.waitForFunction(
          (v) => document.querySelector("#windowInfo").textContent !== v,
          first,
        );
        assert.equal(await page.locator("#events button").count(), 60);
      },
    );
    await check(
      "Bench without GPS; simulated USB loss requires explicit resume",
      async () => {
        await page.setViewportSize({ width: 951, height: 585 });
        await page.locator('[data-view="field"]').click();
        await page.locator("#scenario").selectOption("No GPS");
        await page.waitForFunction(() =>
          document.querySelector("#facts").textContent.includes("No fresh fix"),
        );
        await page.locator("#mode").selectOption("bench");
        await page.locator("#go").click();
        await textIs("#run", "running");
        await page.locator("#scenario").selectOption("USB loss");
        await textIs("#run", "paused");
        await page.locator("#scenario").selectOption("No GPS");
        await textIs("#connection", "Host connected");
        assert.equal((await state()).state.run_state, "paused");
        await page.locator("#go").click();
        await textIs("#run", "running");
      },
    );
    if (process.env.SURVEY_PRIVATE_URL) {
      await check("Private TLS preview, read only", async () => {
        await page.goto(process.env.SURVEY_PRIVATE_URL);
        await textIs("#source", "Simulation");
        await textIs("#mapready", "Offline area");
        assert.equal(await page.evaluate(() => window.isSecureContext), true);
      });
    }
    assert.deepEqual(errors, []);
    console.log("Private QA artifacts: " + dir);
  } finally {
    if (browser) await browser.close();
    await fs
      .writeFile(path.join(dir, "simulation", "stop-" + proc.pid), "stop")
      .catch(() => {});
    const timer = setTimeout(() => proc.kill(), 5000);
    await exited;
    clearTimeout(timer);
  }
}
main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
