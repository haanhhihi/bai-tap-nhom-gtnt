# Bài tập Wikispeedia — gói dành cho sinh viên

Bắt đầu bằng [đề bài](bai-tap-wikispeedia.md). Gói này đã có đủ dữ liệu và công cụ tự chấm; không cần tải thêm dữ liệu hoặc lời giải mẫu.

## Thành phần

- `bai-tap-wikispeedia.md`: đề bài, quy cách đầu ra và bảng điểm.
- `assignment/submission_template.py`: template có docstring; sinh viên cài đặt các hàm TODO.
- `assignment/minhash_params.json`: 128 hàm băm cố định.
- `data/`: hai tệp dữ liệu nén Wikispeedia và bộ 100 cặp chính thức `pairs.csv`.
- `assignment/pairs_sample.csv`: bộ 4 cặp nhỏ để thử riêng; không thay cho bộ chính thức.
- `autograder.py`: tự chấm các hàm và đầu ra, tối đa 100 điểm.
- `SHA256SUMS.txt`: mã kiểm tra tính toàn vẹn các tệp trong gói.

## 1. Chuẩn bị

Giải nén ZIP này, mở terminal tại thư mục `wikispeedia-student-package` (thư mục chứa README này). Dùng Python 3.10 trở lên; kiểm tra bằng:

```bash
python3 --version
```

Template và grader chỉ cần thư viện chuẩn Python. Nếu bài làm của bạn sử dụng NumPy/SciPy, tự cài thư viện trong môi trường đang dùng và ghi phiên bản trong docstring đầu bài làm theo đề.

Sao chép template một lần, rồi giải nén hai bộ dữ liệu:

```bash
cp assignment/submission_template.py submission.py
tar -xzf data/wikispeedia_paths-and-graph.tar.gz -C data
tar -xzf data/wikispeedia_articles_plaintext.tar.gz -C data
```

Sau đó sửa `submission.py`; không chạy lại lệnh sao chép đè lên bài đang làm. Nếu dùng Windows, có thể sao chép tệp bằng trình quản lý tệp và dùng `python` thay `python3` khi đó là Python 3.10 trở lên.

## 2. Làm bài và chạy

Đọc docstring, hoàn thiện các hàm có TODO, giữ giao diện và phần gọi `main()` cuối tệp. Khi các hàm đã hoàn thiện:

```bash
python3 submission.py
```

Chương trình mặc định dùng `data/pairs.csv` và tạo bốn tệp trong `output/`:

- `pagerank.csv`: 4604 dòng dữ liệu.
- `topic_pagerank.csv`: 18416 dòng, gồm Science, History, Geography và r_mix.
- `minhash.csv`: 4604 dòng.
- `similarities.csv`: 100 dòng theo đúng thứ tự bộ cặp chính thức.

Các số dòng trên không tính header. Không tự sửa các tệp đầu vào, bộ cặp hoặc bộ hàm băm.

## 3. Tự chấm

Có thể tự chấm cả khi bài làm còn chưa hoàn thiện:

```bash
python3 autograder.py submission.py --report grading_reports/self_check.json
```

Bộ chấm báo điểm từng nhóm và tổng điểm trên màn hình; JSON có lỗi chi tiết. Bản template chưa làm sẽ nhận 0/100 và báo `NotImplementedError`; đây là kết quả bình thường. Lỗi ở một nhóm không ngăn các nhóm khác được chấm.

Mỗi nhóm có timeout mặc định 180 giây. Dùng `python3 autograder.py --help` để xem tùy chọn. Bộ chấm đọc được các tệp nén, nhưng chạy `submission.py` để xuất kết quả vẫn cần dữ liệu đã giải nén.

Sau khi sửa bài, tự chấm lại rồi chạy lại `submission.py` để tạo kết quả mới nhất. Bộ chấm tự tạo đầu ra kiểm thử trong thư mục tạm, không tự cập nhật thư mục `output/` của bạn.

## 4. Nộp bài

Nộp `submission.py` cùng bốn CSV trong `output/`, theo hướng dẫn của giảng viên. Không cần nộp lại dữ liệu, template gốc hoặc grader.
