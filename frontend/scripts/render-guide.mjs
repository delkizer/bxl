/* scripts/render-guide-html.mjs */
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import MarkdownIt from 'markdown-it';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const mdPath  = path.resolve(__dirname, '..', 'USER_GUIDE.md');
const outDir  = path.resolve(__dirname, '..', 'dist');
const htmlOut = path.join(outDir, 'user-guide.html');

/* 1) MD → HTML */
const md  = await fs.readFile(mdPath, 'utf8');
const md2html = new MarkdownIt({ html:true, linkify:true }).render(md);

/* 2) 틀 + CSS */
const html = /* html */`
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>BXL 사용자 가이드</title>
<style>
 body{font-family:system-ui,sans-serif;padding:2rem;background:#f8fafc;color:#111;}
 table{border-collapse:collapse;width:100%;font-size:14px;}
 th,td{border:1px solid #d1d5db;padding:.5rem;text-align:left;}
 th{background:#e5e7eb;}
 code{background:#f3f4f6;padding:.1rem .3rem;border-radius:4px;}
</style>
</head>
<body>
<h1 style="margin-bottom:1rem;font-size:1.8rem;">BXL 사용자 가이드</h1>
${md2html}
</body></html>`;

await fs.mkdir(outDir, { recursive:true });
await fs.writeFile(htmlOut, html, 'utf8');
console.log('✅  user-guide.html 생성 완료');
