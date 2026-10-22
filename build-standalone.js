/* Gộp aptis-memorizer.html + glossary.js thành MỘT file duy nhất: index.html
   - index.html là file GitHub Pages phục vụ ở địa chỉ gốc của site
   - cũng chính là file bạn gửi cho người khác (mở bằng Chrome/Edge là chạy)
   Chạy:  node build-standalone.js      (trong thư mục tool)                   */
const fs = require('fs');
const path = require('path');

const dir = __dirname;
let out = fs.readFileSync(path.join(dir, 'aptis-memorizer.html'), 'utf8');

// nhúng glossary và dữ liệu Speaking vào thẳng file
[['glossary.js', 'glossary.js'], ['data/part1.js', 'data/part1.js'],
 ['data/part2.js', 'data/part2.js'], ['data/part3.js', 'data/part3.js']]
  .forEach(([tagPath, file]) => {
    const tag = '<script src="' + tagPath + '"></script>';
    if (!out.includes(tag)) {
      console.error('Không tìm thấy thẻ nạp ' + tagPath + ' — dừng lại.');
      process.exit(1);
    }
    const code = fs.readFileSync(path.join(dir, file), 'utf8');
    out = out.replace(tag, '<script>\n/* ' + file + ' nhúng sẵn */\n' + code + '\n</script>');
  });
fs.writeFileSync(path.join(dir, 'index.html'), out, 'utf8');
console.log('Đã tạo index.html —', (out.length / 1024).toFixed(0), 'KB');
