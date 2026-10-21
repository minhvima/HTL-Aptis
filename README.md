# Memorization support - Aptis

Công cụ hỗ trợ học thuộc lòng bài viết tiếng Anh ngắn — dành cho phần Speaking Part 4 của kỳ thi Aptis.
Sản phẩm tự phát triển cho riêng nhu cầu cá nhân của **Phạm Trung Minh** – ĐHHHVN.

**Dùng ngay:** https://minhvima.github.io/HTL-Aptis/

Một trang web tĩnh, không máy chủ, không tài khoản: mọi bài học, tiến độ và ghi âm đều nằm trong trình duyệt của bạn.

### Có gì bên trong

| Tab | Phương pháp |
|---|---|
| Đọc & Nghe | mã hoá kép (dual coding), shadowing, bấm từ để tra nghĩa + phát âm |
| Khung ý | từ khoá, chữ cái đầu câu, bài xếp lại trật tự |
| Sơ đồ | mindmap 3 cấp: tên bài → đoạn → câu |
| Xoá dần | 4 mức xoá tăng dần (method of vanishing cues) |
| Gõ lại | hiệu ứng kiểm tra, chấm từng từ; gõ từng câu, cả đoạn hoặc cả bài |
| Đọc lại | chấm phát âm bằng micro: trình duyệt / OpenAI API / Whisper chạy trên máy |
| Ôn tập | giãn cách 1′ → 6′ → 20′ rồi 1 → 3 → 7 → 16 → 35 ngày |

### Các file trong repo

| File | Vai trò |
|---|---|
| `index.html` | bản chạy được, gộp sẵn mọi thứ — chính là trang web ở trên, cũng là file gửi cho người khác |
| `aptis-memorizer.html` | mã nguồn (nạp `glossary.js` riêng) — sửa ở đây |
| `glossary.js` | từ điển tra nhanh: nghĩa tiếng Việt + phiên âm, thêm bao nhiêu tuỳ ý |
| `build-standalone.js` | `node build-standalone.js` để gộp hai file trên thành `index.html` |

Repo không chứa bài học nào. Bạn tự mở file `.txt` của mình, hoặc dán nội dung vào ô ở màn hình đầu.

### Định dạng file `.txt`

```
Topic 19: Describe a time when you received a gift.
Topic 20: Describe a time when you visited an old building.
----------------------------------------------------------------
A few months ago, I went on a long hiking trip with my friends…

At the beginning of the trip, we were excited to explore the forest…
```

Phần trên dòng gạch ngang là các chủ đề áp dụng được, phần dưới là bài mẫu, mỗi đoạn một dòng.

---

## Mở công cụ

- **Trên máy tính (đầy đủ chức năng, có micro):** mở `aptis-memorizer.html` hoặc `index.html` bằng **Chrome** hoặc **Edge**, hoặc vào thẳng https://minhvima.github.io/HTL-Aptis/
- **Trên điện thoại:** mở link ở trên; dán nội dung bài vào ô ở màn hình đầu nếu không có sẵn file.

Bấm **Mở file .txt** rồi chọn file bài của bạn. Công cụ tự:
- tách phần chủ đề (ở trên dòng `------`) và phần bài tiếng Anh (ở dưới),
- chia bài thành đoạn → câu, mỗi câu là một thẻ học,
- tạo lịch ôn riêng cho từng câu, lưu trong trình duyệt theo nội dung file (đổi file → tiến độ riêng, mở lại file cũ → tiến độ cũ vẫn còn).

File không có dòng `------` vẫn dùng được: toàn bộ nội dung được coi là bài học.

## Dữ liệu được lưu thế nào

- Mỗi file bạn mở được lưu lại thành một mục trong **Bài đã lưu** (kèm nguyên văn bài và toàn bộ tiến độ). Mở file mới **không** xoá bài cũ.
- Bài được nhận diện theo **nội dung**, không theo tên file: đổi tên file, chép sang thư mục khác, mở lại vẫn ra đúng tiến độ cũ. Sửa nội dung bài thì nó được coi là bài mới.
- Danh sách này nằm ở màn hình đầu và ở cuối thanh bên; bấm tên bài để học tiếp, bấm **Xoá** để bỏ hẳn bài đó.
- Tab **Tiến độ → Sao lưu & khôi phục**: xuất ra file `.json` (hoặc đoạn chữ để chép) chứa tất cả bài + tiến độ + từ khó. Dùng để chuyển giữa máy tính và điện thoại, hoặc phòng khi xoá cache trình duyệt. Nhập vào máy khác bằng **Nhập file sao lưu**.
- Nếu trình duyệt chặn bộ nhớ cục bộ (chế độ ẩn danh, Safari), công cụ hiện cảnh báo cam ngay đầu trang — khi đó hãy xuất sao lưu trước khi đóng.

## Lộ trình 1 bài (~35 phút, nhớ được nhiều ngày)

| # | Tab | Làm gì | Thời gian |
|---|-----|--------|-----------|
| 1 | Đọc & Nghe | Nghe 2 lượt, bấm vào cụm từ lạ để xem nghĩa + phát âm, đánh dấu từ khó. Bật **Shadowing** để đọc theo. | 5' |
| 2 | Khung ý | Học từ khoá + chữ cái đầu mỗi câu; làm bài **Xếp lại trật tự**. | 8' |
| 2b | Sơ đồ | Nhìn cây: tên bài → từng đoạn → từng câu. Chuyển sang **Chữ cái đầu** rồi tự đọc lại cả bài theo sơ đồ. | 4' |
| 3 | Xoá dần | Chạy mức 1 → 2 → 3 → 4. Tự điền trong đầu, bấm ô trống để kiểm tra. | 10' |
| 4 | Gõ lại | Gõ lại từng câu từ trí nhớ, nhắm trên 90%. | 8' |
| 5 | Đọc lại (mic) | Đọc cả đoạn rồi cả bài, máy chấm từng từ. | 4' |
| 6 | Ôn tập | Hôm sau trở đi: chỉ làm các câu **đến hạn**. | 5'/ngày |

Sau mỗi lần kiểm tra, chấm thật thà: **Quên rồi / Khó / Ổn / Dễ**. Chấm càng đúng, lịch ôn càng khớp với thời điểm bạn sắp quên.

## Cơ sở khoa học của từng chức năng

- **Chunking** — chia bài thành câu, mỗi câu là một đơn vị trí nhớ làm việc, thay vì nuốt cả bài.
- **Dual coding** — đọc + nghe + nói cùng một nội dung tạo nhiều đường truy xuất.
- **Generation / testing effect** — tab Gõ lại và Đọc lại bắt bạn **tự tạo lại** câu; tự tạo lại nhớ lâu hơn đọc lại nhiều lần.
- **Method of vanishing cues** — Khung ý → Xoá dần mức 1→4 rút gợi ý từ từ, không rơi tự do.
- **Expanding retrieval / spacing** — lịch ôn 1 phút → 6 phút → 20 phút (trong buổi), rồi 1 → 3 → 7 → 16 → 35 ngày; chấm "Quên rồi" đưa câu về đầu hàng đợi.
- **Serial order learning** — bài Xếp lại trật tự rèn đúng thứ tự ý, phần hay vỡ nhất khi nói.
- **Production practice** — chấm bằng micro ép bạn phát âm thành tiếng, giống điều kiện thi nói.

## Chọn bộ nhận dạng giọng nói (tab Đọc lại)

Thanh **Bộ nhận dạng** ở đầu tab cho chọn 1 trong 3:

| Engine | Chất lượng | Chi phí | Cần gì |
|---|---|---|---|
| **Trình duyệt** (mặc định) | trung bình, hay nghe nhầm câu dài / giọng không bản ngữ | miễn phí | Chrome hoặc Edge, có mạng |
| **OpenAI API** | tốt nhất (`gpt-4o-transcribe`, cùng loại ChatGPT dùng) | ~0,006 USD/phút ghi âm | API key của bạn |
| **Whisper trên máy** | tốt, kém OpenAI một chút | miễn phí | tải mô hình 75MB (base.en) hoặc 250MB (small.en) lần đầu |

### Trình duyệt hỏi quyền micro mỗi lần?

Khi mở file trực tiếp từ ổ đĩa (`file://`), Chrome coi trang là nguồn không xác định nên **không nhớ được quyền micro** — mỗi lần tải lại trang nó hỏi lại. Công cụ giữ micro mở trong suốt phiên học nên chỉ hỏi một lần cho mỗi lần tải trang (nút **Tắt micro** để trả lại sớm).

Muốn không bị hỏi nữa, chạy qua localhost — mở PowerShell tại thư mục repo và chạy:

```bash
python -m http.server 8777
```

rồi mở `http://localhost:8777/aptis-memorizer.html`. Ở địa chỉ này Chrome nhớ quyền vĩnh viễn, và `localStorage` cũng ổn định hơn.

Lưu ý: tiến độ lưu ở `file://` và ở `localhost` là **hai kho riêng**. Lần đầu chuyển sang localhost, hãy vào Tiến độ → **Xuất file sao lưu** ở bản cũ rồi **Nhập** ở bản mới.

**Dùng OpenAI:** lấy key ở platform.openai.com/api-keys → dán vào ô → **Lưu key**. Key chỉ nằm trong trình duyệt máy này, chỉ gửi tới `api.openai.com`, và **không** nằm trong file sao lưu. Chọn `gpt-4o-mini-transcribe` nếu muốn rẻ hơn.

### Trang báo "Page Unresponsive" khi nhận dạng

Chỉ xảy ra với engine **Whisper trên máy**: mô hình chạy bằng WASM, nếu chạy chung luồng với giao diện thì Chrome tưởng trang bị treo. Công cụ nay đẩy phần nhận dạng sang **Web Worker** nên giao diện vẫn mượt, có đồng hồ đếm giây và nút **Dừng nhận dạng**.

Nếu vẫn gặp hộp thoại đó: trình duyệt không tạo được worker (hay gặp ở `file://`). Khi đó hãy chạy công cụ qua `http://localhost` theo hướng dẫn ở trên, hoặc dùng **OpenAI API** cho những bản ghi dài. Bấm **Wait** chứ đừng **Exit page** — nó vẫn đang chạy, chỉ là chậm.

Thời gian tham khảo: base.en mất 10–20 giây cho mỗi 30 giây ghi âm; small.en chậm gấp 2–3 lần. Đọc cả bài (trên 1 phút) thì OpenAI API nhanh hơn nhiều.

**Dùng Whisper trên máy:** chọn model rồi bấm ghi âm — lần đầu máy tải mô hình (hiện % tải), các lần sau dùng cache, chạy được cả khi mất mạng, tiếng nói không rời khỏi máy.

Với hai engine sau, công cụ ghi âm trước rồi mới chấm, nên bạn còn **nghe lại chính giọng mình** ngay dưới nút ghi — rất hữu ích để nghe lỗi phát âm.

Cả ba đều **không** được mớm trước nội dung bài, nên điểm phản ánh đúng những gì bạn đọc ra.

## Phím tắt & cỡ chữ

- `Ctrl+Enter` — kiểm tra câu đang gõ
- `Alt+P` — nghe phần đang chọn · `Alt+S` — dừng đọc
- Nút **A− / A+** trên thanh công cụ đổi cỡ chữ toàn app từ 80% đến 180% (áp dụng cho cả sơ đồ), và ghi nhớ lựa chọn.
- Nút **Khổ rộng / Khổ hẹp** đổi bề ngang khung nội dung: rộng 1240px (mặc định, ít phải cuộn) hoặc hẹp 800px (dòng ngắn, dễ đọc văn xuôi hơn). Tab Sơ đồ luôn dùng tới 1680px. Trên điện thoại cả hai đều tự co về vừa màn hình.

## Từ khó được xác định thế nào

Công cụ **không** dựa vào một danh sách cố định. Mỗi từ trong bài được chấm điểm khó ngay trên máy, không cần mạng:

| Tín hiệu | Ảnh hưởng |
|---|---|
| Số âm tiết | mỗi âm tiết thêm 1,3 điểm |
| Không nằm trong ~900 từ phổ thông | +1,8 |
| Mẫu chính tả dễ đọc sai (`-tion`, `-ough`, `kn-`, `-ture`, cụm 3 phụ âm…) | +1,1 mỗi mẫu |
| Dài từ 10 ký tự | +0,8 |
| **Bạn từng đọc sai khi chấm mic** | +1,2 mỗi lần (tối đa +3) |
| **Bạn từng bấm tra từ này** | +0,5 mỗi lần (tối đa +1,6) |
| **Bạn bấm “Đã biết từ này”** | loại bỏ vĩnh viễn, ở mọi bài |

Từ đạt 3,4 điểm trở lên được gạch chân — khoảng 20–25% số từ của bài.

| Kiểu gạch chân | Nghĩa |
|---|---|
| Gạch liền vàng | khó **và** đã có nghĩa (glossary, nghĩa bạn gõ, hoặc do OpenAI tạo) |
| Gạch nét đứt xám | máy thấy khó nhưng **chưa có nghĩa** — bấm vào để tự gõ hoặc tạo tự động |
| Nền vàng, viền cam | bạn tự bấm “Đánh dấu khó” |
| Không gạch | từ phổ thông, hoặc bạn đã bảo là biết rồi |

Danh sách **Từ khó của bài** nằm cuối thanh bên, xếp theo điểm. Tab **Tiến độ → Từ vựng của bạn** quản lý ba kho: đã biết, từng đọc sai, nghĩa đã lưu — dùng chung cho mọi bài và đi theo file sao lưu.

### Tạo nghĩa hàng loạt (tuỳ chọn, cần OpenAI key)

Nút **Tạo nghĩa cho cả bài (n)** ở thanh bên gửi các từ khó chưa có nghĩa kèm nguyên văn bài tới `gpt-4o-mini`, nhận về nghĩa tiếng Việt **đúng ngữ cảnh** và phiên âm IPA, lưu vĩnh viễn trên máy. Mỗi từ chỉ tốn tiền một lần, cả bài khoảng vài chục đồng. Dùng chung key bạn đã nhập ở tab Đọc lại.

Không có key vẫn dùng được bình thường: gạch chân và chấm độ khó chạy offline, bạn tự gõ nghĩa cho từ nào cần.

### Tra từ tự động, không cần key

Từ nào chưa có trong `glossary.js`, bấm vào là công cụ tự tra:

| Nguồn | Cho ra | Dùng khi |
|---|---|---|
| **[dict.minhqnd.com](https://dict.minhqnd.com)** | phiên âm IPA + **nghĩa tiếng Việt** + từ loại | mặc định, ~100ms |
| **Wiktionary** (Wikimedia) | IPA + định nghĩa tiếng Anh ngắn | khi từ điển Anh-Việt không có: cụm từ, thành ngữ |

Đây là từ điển thật, không phải máy dịch: *breathtaking* → "Hấp dẫn, ngoạn mục."; *humorous* → "Khôi hài, hài hước; hóm hỉnh."

Từ ở dạng biến đổi (*participated*, *responsibilities*, *classmates*) hoặc viết theo lối Anh-Anh (*organised*) được tra tiếp sang từ gốc, tối đa hai bước, và ghi rõ *"dạng của …"*. Phiên âm cụt bị loại và thay bằng phiên âm của Wiktionary.

Dữ liệu từ điển Anh-Việt thuộc dự án [minhqnd/dictionary](https://github.com/minhqnd/dictionary), giấy phép CC BY 4.0 — công cụ ghi nguồn ngay trong ô tra từ.

Mọi kết quả tra được lưu vĩnh viễn trong trình duyệt, nên mỗi từ chỉ gọi mạng một lần và lần sau tra được cả khi offline.

### Hai kho dữ liệu, và cách đưa từ mới vào kho chung

| | Kho cá nhân | Kho chung (`glossary.js`) |
|---|---|---|
| Ở đâu | `localStorage` trình duyệt của từng người | file trong repo, nằm trong `index.html` |
| Ai thấy | chỉ mình người đó | mọi người mở link |
| Lớn lên khi nào | bạn gõ nghĩa, bấm *Tạo nghĩa cho cả bài*, đánh dấu *Đã biết*, hoặc đọc sai khi chấm mic | chỉ khi có người sửa file rồi push |

Trang web là **tĩnh**: nó không thể tự ghi ngược dữ liệu lên repo. Từ mới bạn học ở máy mình sẽ **không** tự xuất hiện với người khác.

Muốn đưa lên kho chung, có đường dẫn sẵn: **Tiến độ → Từ vựng của bạn → “Xuất n từ mới sang glossary.js”**. Nút này in ra đúng khối mã cần dán:

```js
  "environmental": { vi: "thuộc về môi trường", ipa: "/ɪnˌvaɪrənˈmentl/" },
  "presentation": { vi: "bài thuyết trình", ipa: "/ˌpreznˈteɪʃn/" },
```

Dán vào trong ngoặc của `glossary.js`, chạy `node build-standalone.js`, rồi commit và push. Khoảng một phút sau mọi người mở link đều có các nghĩa đó.

## Thêm nghĩa cho từ mới

Bấm vào một từ → gõ nghĩa tiếng Việt → Enter (lưu riêng trong trình duyệt). Muốn nghĩa dùng chung cho mọi bài, thêm vào `glossary.js`:

```js
"suspension bridge": { vi: "cầu treo", ipa: "/səˈspenʃn brɪdʒ/", note: "ghi chú tuỳ chọn" },
```

Cụm nhiều từ sẽ tự được gạch chân trong bài. Nếu máy có mạng, từ chưa có trong glossary vẫn tra được phiên âm + định nghĩa tiếng Anh tự động (chỉ ở bản chạy trên máy).

## Chia sẻ cho người khác

**Cách 1 — gửi link (tốt nhất).** https://minhvima.github.io/HTL-Aptis/ — ai có link là dùng được, luôn là bản mới nhất. Vì là địa chỉ `https://` nên Chrome **nhớ quyền micro vĩnh viễn** và Whisper chạy trong Web Worker ổn định, tốt hơn hẳn mở file bằng `file://`.

**Cách 2 — gửi 1 file, dùng offline.** Gửi `index.html` (~100KB, đã nhúng sẵn glossary) qua Zalo/email/USB. Người nhận lưu về máy, bấm đúp mở bằng Chrome hoặc Edge là chạy, không cần cài gì, không cần mạng (trừ tra từ online và engine OpenAI).

Sau khi sửa `aptis-memorizer.html` hay `glossary.js`, tạo lại `index.html` bằng:

```bash
node build-standalone.js
```

rồi commit và push — GitHub Pages tự cập nhật sau khoảng một phút.

**Những thứ KHÔNG đi kèm khi chia sẻ:**

- *API key OpenAI của bạn* — key nằm trong bộ nhớ trình duyệt máy bạn, không nằm trong file. Người nhận muốn dùng engine OpenAI phải tự tạo key của họ, và chi phí tính vào tài khoản của họ.
- *Tiến độ học và danh sách bài* — mỗi người có kho riêng. Muốn gửi kèm bài, vào **Tiến độ → Xuất file sao lưu**, gửi file `.json` đó để họ **Nhập**; họ sẽ có đúng các bài của bạn (tiến độ cũng đi theo, có thể bảo họ bấm *Đặt lại tiến độ bài này* nếu muốn học từ đầu).
- *Các file .txt gốc* — gửi thêm nếu muốn họ tự mở bài khác.

## Giấy phép

Dùng tự do cho mục đích học tập.
