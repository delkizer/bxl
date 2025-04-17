import fs from 'fs/promises';
import path from 'path';
import MarkdownIt from 'markdown-it';
import puppeteer from 'puppeteer';

const mdPath  = path.resolve('USER_GUIDE.md');
const htmlOut = path.resolve('dist/user-guide.html');
const pngOut  = path.resolve('dist/user-guide.png');

// 1. Markdown → HTML
const md = await fs.readFile(mdPath, 'utf8');
const html = /* html */`
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<title>BXL USER GUIDE</title>
<style>
 body{font-family:system-ui, sans-serif;padding:2rem;background:#f8fafc;color:#111;}
 table{border-collapse:collapse;width:100%;font-size:14px;}
 th,td{border:1px solid #d1d5db;padding:.5rem;text-align:left;}
 th{background:#e5e7eb;}
 code{background:#f3f4f6;padding:.1rem .3rem;border-radius:4px;}
</style>
</head><body>
${new MarkdownIt({html:true,linkify:true}).render(md)}
</body></html>`;
await fs.mkdir(path.dirname(htmlOut), { recursive:true });
await fs.writeFile(htmlOut, html, 'utf8');
console.log('✅ user-guide.html 완료');

// 2. HTML → PNG (전체 페이지 캡처)
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto('file://' + htmlOut, { waitUntil:'networkidle0' });
await page.screenshot({ path: pngOut, fullPage:true });
await browser.close();
console.log('🖼️  user-guide.png 완료');
