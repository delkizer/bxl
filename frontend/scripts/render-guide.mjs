import fs from 'fs/promises';
import path from 'path';

const htmlOut = path.resolve('dist/user-guide.html');

// 1. Markdown → HTML
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
</body></html>`;
await fs.mkdir(path.dirname(htmlOut), { recursive:true });
await fs.writeFile(htmlOut, html, 'utf8');
console.log('✅ user-guide.html 완료');
