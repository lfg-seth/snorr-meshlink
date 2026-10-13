# Portal development

React + TypeScript + Vite. This is a runnable development baseline with synthetic freshness states, not the completed four-page portal. PocketBase, the Python worker, authentication and a live radio feed are not installed yet.

## Run on the Dell or desktop WSL

Use Node **22.23.1**, recorded in the root `.nvmrc`. If you already use nvm, run `nvm install` and `nvm use` from the repository root. Then:

```sh
cd portal
npm ci
npm run dev
```

Open the localhost address Vite prints. Stop with Ctrl+C. The dev server binds to localhost; no VM, Docker, broker or tunnel is required. To verify before committing:

```sh
npm run check
```

This runs the measurement-age tests, TypeScript checking and a production build into ignored `dist/`. `npm run preview` serves that build locally for review, not as the production server. `npm ci` installs the exact lockfile; use `npm install` only when intentionally changing dependencies and commit the resulting lockfile.

## TypeScript, kept simple

`.ts` contains ordinary JavaScript plus types; `.tsx` also contains React markup. Types describe expected data and disappear from the production JavaScript. They do not validate network input.

For example, `measuredAt: string | null` means a measurement timestamp can be a string or explicitly unknown. `type Position = { ... }` names a record shape so callers cannot accidentally omit its fields. `import type` brings in a type without adding runtime code. See `src/position.ts` for a small example.

Prefer plain record types, functions and components, inferred types where obvious, and comments explaining domain rules. Avoid advanced generics, type puzzles and broad `any` shortcuts. Keep strict checking enabled to catch timestamp/null mistakes early. The built-in Node test runner keeps the initial test setup small; tests use only TypeScript syntax Node can strip.

## Environments and delivery

See [the environment plan](../docs/research/portal-build-environment.md). GitHub Actions runs the same `npm ci` / `npm run check` commands for portal changes. A successful main push uploads a seven-day static build artifact named with its commit SHA. There is no deployment workflow or external preview hosting yet.

The future authenticated portal must validate incoming records and enforce access/assignment rules on the server. Never put credentials in frontend configuration: browser-visible build variables are public. Real data, secrets and backups remain in ignored `private/` or `local-data/`; generated output and dependencies stay out of Git.
