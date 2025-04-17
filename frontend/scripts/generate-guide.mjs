/* eslint-disable no-console */
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { parse } from '@vue/compiler-sfc';
import { load } from 'cheerio';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SRC_DIR   = path.join(__dirname, '..', 'src');
const OUT_FILE  = path.join(__dirname, '..', 'USER_GUIDE.md');

const vueFiles = await getVueFiles(SRC_DIR);
const items    = [];

for (const file of vueFiles) {
  const code   = await fs.readFile(file, 'utf8');
  const { descriptor } = parse(code);        // SFC 파싱
  if (!descriptor.template) continue;

  const $ = load(descriptor.template.content);

  $('[data-guide]').each((_, el) => {
    const step  = $(el).attr('data-step')  ?? '';
    const guide = $(el).attr('data-guide')?.trim() ?? '';
    const tag   = el.tagName;
    const cls   = ($(el).attr('class') || '').trim().replace(/\s+/g, '.');
    items.push({
      step, guide,
      cssSel: cls ? `${tag}.${cls}` : tag,
      file: path.relative(SRC_DIR, file)
    });
  });
}

items.sort((a, b) => a.step - b.step);

const md = [
  '| 단계 | 위치(CSS) | 설명 | 파일 |',
  '| --- | --- | --- | --- |',
  ...items.map(i => `| ${i.step} | \`${i.cssSel}\` | ${i.guide} | \`${i.file}\` |`)
].join('\n');

await fs.writeFile(OUT_FILE, md);
console.log(`✅  USER_GUIDE.md 생성 (항목 ${items.length}개)`);

/* ───────────── util: src 하위 모든 .vue 탐색 ───────────── */
async function getVueFiles(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files   = await Promise.all(entries.map(entry => {
    const res = path.resolve(dir, entry.name);
    return entry.isDirectory() ? getVueFiles(res) :
           entry.name.endsWith('.vue') ? res : [];
  }));
  return files.flat();
}
