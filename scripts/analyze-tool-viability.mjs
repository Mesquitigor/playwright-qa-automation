#!/usr/bin/env node
/**
 * Analyzes an automation project to estimate whether Playwright,
 * a lighter HTTP runner, or a headless-browser alternative (e.g. Lightpanda)
 * is the best fit for time and RAM usage.
 *
 * Usage:
 *   node scripts/analyze-tool-viability.mjs
 *   node scripts/analyze-tool-viability.mjs --benchmark
 *   node scripts/analyze-tool-viability.mjs --benchmark --run-tests
 */

import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const args = new Set(process.argv.slice(2));
const WITH_BENCHMARK = args.has('--benchmark');
const RUN_TESTS = args.has('--run-tests');
const QUIET = args.has('--quiet');

const TEST_DIR_CANDIDATES = ['tests', 'test', 'e2e', 'spec', '__tests__'];
const TEST_FILE_PATTERN = /\.(spec|test)\.(t|j)sx?$/i;
const CONFIG_CANDIDATES = [
  'playwright.config.ts',
  'playwright.config.js',
  'playwright.config.mjs',
];

const log = (...messages) => {
  if (!QUIET) console.log(messages.join(' '));
};

const readText = (filePath) => {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch {
    return null;
  }
};

const walkFiles = (dir, acc = []) => {
  if (!fs.existsSync(dir)) return acc;

  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.') || entry.name === 'node_modules') continue;

    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkFiles(fullPath, acc);
    } else if (TEST_FILE_PATTERN.test(entry.name)) {
      acc.push(fullPath);
    }
  }

  return acc;
};

const findTestFiles = () => {
  const files = new Set();

  for (const dirName of TEST_DIR_CANDIDATES) {
    walkFiles(path.join(ROOT, dirName), []).forEach((file) => files.add(file));
  }

  walkFiles(ROOT, []).forEach((file) => {
    if (TEST_FILE_PATTERN.test(file) && !file.includes(`${path.sep}node_modules${path.sep}`)) {
      files.add(file);
    }
  });

  return [...files].sort();
};

const findPlaywrightConfig = () =>
  CONFIG_CANDIDATES.map((name) => path.join(ROOT, name)).find((file) => fs.existsSync(file)) ?? null;

const parseNumber = (source, regex, fallback = null) => {
  const match = source.match(regex);
  return match ? Number(match[1]) : fallback;
};

const parsePlaywrightConfig = (configPath) => {
  const source = readText(configPath) ?? '';

  const workers = parseNumber(source, /workers:\s*(\d+)/, null);
  const fullyParallel = /fullyParallel:\s*true/.test(source);
  const projectNames = [...source.matchAll(/name:\s*['"]([^'"]+)['"]/g)].map((m) => m[1]);
  const hasChromium = /chromium|Desktop Chrome|channel:\s*['"]chrome['"]/i.test(source);
  const hasFirefox = /firefox|Desktop Firefox/i.test(source);
  const hasWebkit = /webkit|Desktop Safari/i.test(source);
  const hasMobile = /Mobile Chrome|Mobile Safari|Pixel|iPhone/i.test(source);

  return {
    workers,
    fullyParallel,
    projectNames,
    browsers: {
      chromium: hasChromium,
      firefox: hasFirefox,
      webkit: hasWebkit,
      mobile: hasMobile,
    },
  };
};

const analyzeTestFile = (filePath) => {
  const source = readText(filePath) ?? '';
  const relativePath = path.relative(ROOT, filePath);

  const counts = {
    total: (source.match(/\btest(?:\.(?:only|skip|fixme))?\s*\(/g) ?? []).length,
    skipped: (source.match(/\btest\.skip\s*\(/g) ?? []).length,
    focused: (source.match(/\btest\.only\s*\(/g) ?? []).length,
  };

  const signals = {
    usesRequestFixture: /\{\s*request\s*\}/.test(source) || /\brequest\.(get|post|put|patch|delete|fetch)\b/.test(source),
    usesPageFixture: /\{\s*page\s*\}/.test(source) || /\bpage\.(goto|click|fill|locator)\b/.test(source),
    usesBrowserFixture: /\{\s*browser\s*\}/.test(source) || /\bbrowser\.newContext\b/.test(source),
    usesApiTestingLibrary: /@playwright\/test/.test(source),
    importsPostman: /newman|postman-collection/i.test(source),
    importsPuppeteer: /puppeteer/i.test(source),
    importsLightpanda: /lightpanda|@lightpanda/i.test(source),
  };

  let profile = 'unknown';
  if (signals.usesPageFixture || signals.usesBrowserFixture) {
    profile = 'ui';
  } else if (signals.usesRequestFixture) {
    profile = 'api-playwright';
  } else if (/fetch\(|axios|got\(|supertest|http\.request/i.test(source)) {
    profile = 'api-native';
  }

  return { relativePath, counts, signals, profile };
};

const summarizeTests = (files) => {
  const summary = {
    files: files.length,
    totalTests: 0,
    skippedTests: 0,
    focusedTests: 0,
    profiles: {
      ui: 0,
      'api-playwright': 0,
      'api-native': 0,
      unknown: 0,
    },
    apiFiles: 0,
    uiFiles: 0,
  };

  const details = files.map((file) => {
    const analysis = analyzeTestFile(file);
    summary.totalTests += analysis.counts.total;
    summary.skippedTests += analysis.counts.skipped;
    summary.focusedTests += analysis.counts.focused;
    summary.profiles[analysis.profile] += 1;

    if (analysis.profile === 'ui') summary.uiFiles += 1;
    if (analysis.profile.startsWith('api')) summary.apiFiles += 1;

    return analysis;
  });

  return { summary, details };
};

const readPackageMeta = () => {
  const pkgPath = path.join(ROOT, 'package.json');
  if (!fs.existsSync(pkgPath)) return { dependencies: {}, devDependencies: {} };

  const pkg = JSON.parse(readText(pkgPath));
  return {
    name: pkg.name,
    dependencies: pkg.dependencies ?? {},
    devDependencies: pkg.devDependencies ?? {},
    scripts: pkg.scripts ?? {},
  };
};

const formatMb = (bytes) => `${(bytes / 1024 / 1024).toFixed(1)} MB`;

const getProcessRss = (pid) => {
  try {
    const status = readText(`/proc/${pid}/status`);
    const match = status?.match(/^VmRSS:\s+(\d+)\s+kB/m);
    return match ? Number(match[1]) * 1024 : null;
  } catch {
    return null;
  }
};

const monitorChild = (child) =>
  new Promise((resolve, reject) => {
    let peakRss = 0;
    let intervalId = null;

    if (process.platform === 'linux' && child.pid) {
      intervalId = setInterval(() => {
        const rss = getProcessRss(child.pid);
        if (rss && rss > peakRss) peakRss = rss;
      }, 200);
    }

    child.on('error', reject);
    child.on('close', (code) => {
      if (intervalId) clearInterval(intervalId);
      resolve({ code: code ?? 1, peakRss });
    });
  });

const runCommand = async (command, commandArgs, options = {}) => {
  const startedAt = Date.now();
  const child = spawn(command, commandArgs, {
    cwd: ROOT,
    stdio: ['ignore', 'pipe', 'pipe'],
    env: { ...process.env, ...options.env },
  });

  let stdout = '';
  let stderr = '';

  child.stdout.on('data', (chunk) => {
    stdout += chunk.toString();
  });
  child.stderr.on('data', (chunk) => {
    stderr += chunk.toString();
  });

  const { code, peakRss } = await monitorChild(child);
  const durationMs = Date.now() - startedAt;

  return { code, stdout, stderr, durationMs, peakRss };
};

const benchmarkNativeFetch = async (iterations = 30) => {
  const url = 'https://dummyjson.com/products?limit=5';
  const startedAt = Date.now();
  let okCount = 0;

  for (let i = 0; i < iterations; i += 1) {
    const response = await fetch(url);
    if (response.ok) okCount += 1;
  }

  const durationMs = Date.now() - startedAt;
  const memory = process.memoryUsage();

  return {
    tool: 'native-fetch',
    iterations,
    okCount,
    durationMs,
    avgMs: Number((durationMs / iterations).toFixed(1)),
    rss: memory.rss,
    heapUsed: memory.heapUsed,
  };
};

const benchmarkPlaywrightApi = async () => {
  const sampleFiles = [
    'tests/getSingleProduct.spec.ts',
    'tests/searchProducts.spec.ts',
    'tests/getAllProducts.spec.ts',
  ].filter((file) => fs.existsSync(path.join(ROOT, file)));

  const sampleFile = sampleFiles[0];
  if (!sampleFile) {
    return { skipped: true, reason: 'Nenhum arquivo de teste encontrado para benchmark.' };
  }

  const result = await runCommand(
    'npx',
    ['playwright', 'test', sampleFile, '--workers=1', '--reporter=line'],
    { env: { CI: '1' } },
  );

  return {
    tool: 'playwright-api-suite-sample',
    sampleFile,
    command: `npx playwright test ${sampleFile} --workers=1`,
    exitCode: result.code,
    durationMs: result.durationMs,
    peakRss: result.peakRss,
    passed: /(\d+) passed/.exec(result.stdout)?.[1] ?? null,
    failed: /(\d+) failed/.exec(result.stdout)?.[1] ?? null,
    stdoutTail: result.stdout.split('\n').slice(-8).join('\n'),
    stderrTail: result.stderr.split('\n').slice(-8).join('\n'),
  };
};

const scoreRecommendation = ({ testSummary, config, packageMeta, benchmarks }) => {
  const apiRatio = testSummary.totalTests
    ? testSummary.profiles['api-playwright'] / Math.max(testSummary.files, 1)
    : 0;
  const uiRatio = testSummary.profiles.ui / Math.max(testSummary.files, 1);

  const hasPlaywright = Boolean(packageMeta.devDependencies['@playwright/test']);
  const configuredBrowsers = config
    ? Object.entries(config.browsers).filter(([, enabled]) => enabled).map(([name]) => name)
    : [];

  const options = [
    {
      name: 'Manter Playwright (API request fixture)',
      fit: 0,
      pros: [],
      cons: [],
      actions: [],
    },
    {
      name: 'Otimizar Playwright atual (sem trocar ferramenta)',
      fit: 0,
      pros: [],
      cons: [],
      actions: [],
    },
    {
      name: 'Migrar API para runner HTTP leve (fetch/axios + Vitest/Jest)',
      fit: 0,
      pros: [],
      cons: [],
      actions: [],
    },
    {
      name: 'Avaliar navegador headless alternativo (ex.: Lightpanda) para UI',
      fit: 0,
      pros: [],
      cons: [],
      actions: [],
    },
  ];

  const [keepPlaywright, optimizePlaywright, migrateApi, evaluateLightpanda] = options;

  if (testSummary.profiles['api-playwright'] > 0 && testSummary.profiles.ui === 0) {
    keepPlaywright.fit += 2;
    keepPlaywright.pros.push('Projeto já usa Playwright apenas para API via request fixture.');
    migrateApi.fit += 4;
    migrateApi.pros.push('Testes são 100% API; runner HTTP nativo tende a usar menos RAM.');
    migrateApi.pros.push('Menos overhead de worker/browser do Playwright Test.');
    evaluateLightpanda.fit -= 5;
    evaluateLightpanda.cons.push('Lightpanda foca automação de browser; pouco ganho em suite só API.');
  }

  if (testSummary.profiles.ui > 0) {
    keepPlaywright.fit += 3;
    optimizePlaywright.fit += 3;
    evaluateLightpanda.fit += 3;
    evaluateLightpanda.pros.push('Há testes de UI; alternativas headless podem reduzir RAM em escala.');
    migrateApi.fit += 1;
    migrateApi.cons.push('UI ainda exigirá ferramenta de browser; migração parcial apenas para API.');
  }

  if (config?.browsers.chromium && testSummary.profiles.ui === 0) {
    optimizePlaywright.fit += 4;
    optimizePlaywright.pros.push('Chromium está configurado, mas os testes parecem ser só API.');
    optimizePlaywright.actions.push('Remover project chromium ou usar config dedicada só API.');
    optimizePlaywright.actions.push('Executar com --project=api se separar projetos.');
  }

  if ((config?.workers ?? 1) >= 4 && testSummary.profiles['api-playwright'] > 0) {
    optimizePlaywright.fit += 2;
    optimizePlaywright.actions.push(`Reduzir workers de ${config.workers} para 1-2 em suites API locais.`);
  }

  if (benchmarks?.playwrightApi?.peakRss && benchmarks?.nativeFetch?.rss) {
    const playwrightMb = benchmarks.playwrightApi.peakRss / 1024 / 1024;
    const nativeMb = benchmarks.nativeFetch.rss / 1024 / 1024;
    if (playwrightMb > nativeMb * 2) {
      migrateApi.fit += 2;
      migrateApi.pros.push(
        `Benchmark local: Playwright ~${playwrightMb.toFixed(1)} MB vs fetch ~${nativeMb.toFixed(1)} MB.`,
      );
    }
  }

  if (!hasPlaywright) {
    keepPlaywright.fit -= 3;
    migrateApi.fit += 2;
  }

  options.sort((a, b) => b.fit - a.fit);

  return {
    ranked: options,
    primary: options[0],
    configuredBrowsers,
    suggestedPlaywrightApiConfig:
      testSummary.profiles.ui === 0
        ? [
            'Crie um project "api" sem browser:',
            'projects: [{ name: "api", testMatch: /.*\\.spec\\.ts/ }]',
            'Remova projects chromium/firefox/webkit se a suite for 100% API.',
            'Use workers: 1-2 localmente e 2-4 no CI para suites HTTP.',
          ]
        : [],
    notes: [
      testSummary.profiles.ui === 0
        ? 'Suite detectada como predominantemente API.'
        : 'Suite mista ou UI detectada.',
      configuredBrowsers.length
        ? `Browsers configurados no Playwright: ${configuredBrowsers.join(', ')}`
        : 'Nenhum browser detectado na configuração.',
    ],
  };
};

const renderMarkdownReport = (report) => {
  const lines = [
    '# Relatório de viabilidade de ferramentas de teste',
    '',
    `Gerado em: ${report.generatedAt}`,
    '',
    '## Resumo do projeto',
    '',
    `- Arquivos de teste: **${report.tests.summary.files}**`,
    `- Casos de teste: **${report.tests.summary.totalTests}** (${report.tests.summary.skippedTests} skip)`,
    `- Perfil API (Playwright request): **${report.tests.summary.profiles['api-playwright']} arquivos**`,
    `- Perfil UI (page/browser): **${report.tests.summary.profiles.ui} arquivos**`,
    '',
    '## Recomendação principal',
    '',
    `**${report.recommendation.primary.name}**`,
    '',
    '### Prós',
    ...report.recommendation.primary.pros.map((item) => `- ${item}`),
    '',
    '### Contras',
    ...(report.recommendation.primary.cons.length
      ? report.recommendation.primary.cons.map((item) => `- ${item}`)
      : ['- Nenhum ponto crítico identificado automaticamente.']),
    '',
    '### Ações sugeridas',
    ...(report.recommendation.primary.actions.length
      ? report.recommendation.primary.actions.map((item) => `- ${item}`)
      : ['- Manter stack atual e monitorar tempo/RAM no CI.']),
    '',
    '## Ranking de opções',
    '',
    ...report.recommendation.ranked.map(
      (option, index) => `${index + 1}. ${option.name} (score ${option.fit})`,
    ),
    '',
  ];

  if (report.recommendation.suggestedPlaywrightApiConfig?.length) {
    lines.push('## Ajuste sugerido no Playwright (suite API)', '');
    lines.push(
      ...report.recommendation.suggestedPlaywrightApiConfig.map((item) => `- ${item}`),
    );
    lines.push('');
  }

  if (report.benchmarks) {
    lines.push('## Benchmarks', '');
    if (report.benchmarks.nativeFetch) {
      lines.push(
        `- native fetch: ${report.benchmarks.nativeFetch.iterations} reqs em ${report.benchmarks.nativeFetch.durationMs} ms, RSS ${formatMb(report.benchmarks.nativeFetch.rss)}`,
      );
    }
    if (report.benchmarks.playwrightApi) {
      lines.push(
        `- playwright sample: ${report.benchmarks.playwrightApi.durationMs} ms, pico RSS ${formatMb(report.benchmarks.playwrightApi.peakRss || 0)}, exit ${report.benchmarks.playwrightApi.exitCode}`,
      );
    }
    lines.push('');
  }

  lines.push('## Detalhes por arquivo', '');
  for (const file of report.tests.details) {
    lines.push(`- \`${file.relativePath}\` → ${file.profile} (${file.counts.total} tests)`);
  }

  return `${lines.join('\n')}\n`;
};

const ensureReportsDir = () => {
  const dir = path.join(ROOT, 'reports');
  fs.mkdirSync(dir, { recursive: true });
  return dir;
};

const main = async () => {
  log('Analisando viabilidade de ferramentas de teste...\n');

  const packageMeta = readPackageMeta();
  const configPath = findPlaywrightConfig();
  const config = configPath ? parsePlaywrightConfig(configPath) : null;
  const testFiles = findTestFiles();
  const tests = summarizeTests(testFiles);

  const benchmarks = {};

  if (WITH_BENCHMARK) {
    log('Executando benchmark HTTP nativo...');
    benchmarks.nativeFetch = await benchmarkNativeFetch();

    if (RUN_TESTS && fs.existsSync(path.join(ROOT, 'node_modules', '@playwright', 'test'))) {
      log('Executando amostra Playwright (1 arquivo spec)...');
      benchmarks.playwrightApi = await benchmarkPlaywrightApi();
    } else if (RUN_TESTS) {
      benchmarks.playwrightApi = {
        skipped: true,
        reason: 'Dependências não instaladas. Rode npm install antes.',
      };
    }
  }

  const recommendation = scoreRecommendation({
    testSummary: tests.summary,
    config,
    packageMeta,
    benchmarks,
  });

  const report = {
    generatedAt: new Date().toISOString(),
    project: {
      root: ROOT,
      name: packageMeta.name ?? path.basename(ROOT),
      playwrightConfig: configPath ? path.relative(ROOT, configPath) : null,
      playwright: config,
      dependencies: {
        playwright: packageMeta.devDependencies['@playwright/test'] ?? null,
      },
    },
    tests,
    benchmarks: Object.keys(benchmarks).length ? benchmarks : null,
    recommendation,
  };

  const reportsDir = ensureReportsDir();
  const jsonPath = path.join(reportsDir, 'tool-viability-report.json');
  const mdPath = path.join(reportsDir, 'tool-viability-report.md');

  fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);
  fs.writeFileSync(mdPath, renderMarkdownReport(report));

  log('Resumo');
  log('------');
  log(`Projeto: ${report.project.name}`);
  log(`Testes: ${tests.summary.totalTests} casos em ${tests.summary.files} arquivos`);
  log(`API/Playwright: ${tests.summary.profiles['api-playwright']} | UI: ${tests.summary.profiles.ui}`);
  log(`Recomendação: ${recommendation.primary.name}`);
  log('');
  log(`Relatório JSON: ${path.relative(ROOT, jsonPath)}`);
  log(`Relatório Markdown: ${path.relative(ROOT, mdPath)}`);

  if (!WITH_BENCHMARK) {
    log('');
    log('Dica: rode com --benchmark --run-tests para medir tempo e RAM.');
  }
};

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
