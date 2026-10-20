/* Gộp aptis-memorizer.html + glossary.js thành MỘT file duy nhất: index.html
   - index.html là file GitHub Pages phục vụ ở địa chỉ gốc của site
   - cũng chính là file bạn gửi cho người khác (mở bằng Chrome/Edge là chạy)
   Chạy:  node build-standalone.js      (trong thư mục tool)                   */
const fs = require('fs');
const path = require('path');

const dir = __dirname;
const html = fs.readFileSync(path.join(dir, 'aptis-memorizer.html'), 'utf8');
const gloss = fs.readFileSync(path.join(dir, 'glossary.js'), 'utf8');

const tag = '<script src="glossary.js"></script>';
if (!html.includes(tag)) {
  console.error('Không tìm thấy thẻ nạp glossary.js trong aptis-memorizer.html — dừng lại.');
  process.exit(1);
}
const out = html.replace(tag, '<script>\n/* glossary.js được nhúng sẵn */\n' + gloss + '\n</script>');
fs.writeFileSync(path.join(dir, 'index.html'), out, 'utf8');
console.log('Đã tạo index.html —', (out.length / 1024).toFixed(0), 'KB');
