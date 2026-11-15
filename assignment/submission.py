"""Mẫu bài nộp Wikispeedia — Python 3.10 trở lên.

Hoàn thiện các hàm có TODO; giữ tên hàm, tham số và kiểu đầu ra.
main() đã có phần điều phối và ghi bốn tệp CSV theo đề bài.
Mẫu chưa hoàn thiện sẽ báo NotImplementedError, không sinh đáp án giả.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import hashlib
import re
from pathlib import Path


def load_graph(
    articles_path: Path, links_path: Path
) -> tuple[list[str], list[list[int]]]:
    """Đọc tập đỉnh và danh sách cạnh từ hai tệp TSV UTF-8.

    Bỏ dòng trống/dòng bắt đầu bằng #. Giữ ID mã hóa phần trăm.
    Trả (ids, out_neighbors): ids là danh sách ID phân biệt sắp theo byte
    UTF-8; out_neighbors[j] chứa các chỉ số đích của đỉnh ids[j].
    Gộp cạnh trùng, giữ cạnh tự nối và mọi đỉnh trong articles.tsv.
    Nút cụt có danh sách đích rỗng. Không gắn cứng số đỉnh/cạnh.
    Báo ValueError nếu đồ thị rỗng hoặc cạnh chứa ID ngoài tập đỉnh.
    """
    # TODO: Sinh viên cài đặt.
    raise NotImplementedError("Chưa cài đặt load_graph")


def pagerank(
    ids: list[str],
    out_neighbors: list[list[int]],
    beta: float,
    tol: float,
    max_iter: int,
    teleport: list[float] | None = None,
) -> list[float]:
    """Tính PageRank toàn cục hoặc theo phân phối dịch chuyển cho trước.

    ids và out_neighbors dùng cùng chỉ số như kết quả load_graph.
    beta thuộc (0, 1), tol > 0, max_iter là số nguyên >= 1.
    teleport=None dùng phân phối đều; nếu có, teleport phải dài len(ids),
    hữu hạn, không âm và có tổng lệch 1 không quá 1e-12.
    Khởi tạo bằng phân phối dịch chuyển; bù nút cụt luôn đều trên mọi đỉnh.
    Cập nhật đồng thời bằng số thực 64 bit. Dừng khi sai khác L1 giữa hai
    vòng <= tol hoặc đã thực hiện max_iter vòng; không chuẩn hóa lại.
    Trả vector mới nhất theo thứ tự ids, không trả thống kê phụ.
    Báo ValueError nếu tham số hoặc phân phối dịch chuyển không hợp lệ.
    """
    # ---- (1) KIỂM TRA ĐẦU VÀO ----
    n = len(ids)
    if n == 0 or len(out_neighbors) != n:
        raise ValueError("ids rỗng hoặc out_neighbors không cùng độ dài với ids")
    if not (isinstance(beta, (int, float)) and 0 < beta < 1):
        raise ValueError("beta phải thuộc (0, 1)")
    if not (isinstance(tol, (int, float)) and tol > 0):
        raise ValueError("tol phải > 0")
    if not (isinstance(max_iter, int) and not isinstance(max_iter, bool) and max_iter >= 1):
        raise ValueError("max_iter phải là số nguyên >= 1")
    if teleport is None:
        v = [1.0 / n] * n
    else:
        if len(teleport) != n:
            raise ValueError("teleport sai kích thước")
        if any((not math.isfinite(x)) or x < 0 for x in teleport):
            raise ValueError("teleport có giá trị không hữu hạn hoặc âm")
        if abs(sum(teleport) - 1.0) > 1e-12:
            raise ValueError("tổng teleport lệch 1 quá 1e-12")
        v = [float(x) for x in teleport]

    # ---- (2) MỘT VÒNG CẬP NHẬT ----
    def one_step(r: list[float]) -> list[float]:
        new = [0.0] * n
        dangling = 0.0                      
        for j in range(n):
            targets = out_neighbors[j]
            if targets:
                share = r[j] / len(targets)  
                for i in targets:
                    new[i] += share
            else:
                dangling += r[j]
        base = beta * dangling / n           
        for i in range(n):
            new[i] = beta * new[i] + base + (1.0 - beta) * v[i]
        return new

    # ---- (3) VÒNG LẶP + ĐIỀU KIỆN DỪNG ----
    r = v[:]                                 
    for _ in range(max_iter):
        r_new = one_step(r)
        diff = sum(abs(a - b) for a, b in zip(r_new, r))
        r = r_new
        if diff <= tol:
            break
    return r
    

def topic_distribution(
    ids: list[str], categories_path: Path, prefix: str
) -> list[float]:
    """Tạo phân phối dịch chuyển đều trên tập trang thuộc một chủ đề.

    Đọc categories.tsv UTF-8, bỏ dòng trống/dòng bắt đầu bằng #.
    Chọn nhãn bằng prefix hoặc bắt đầu bằng prefix + '.'. Một ID chỉ
    được đếm một lần trong tập chủ đề, dù có nhiều nhãn phù hợp.
    Trả vector dài len(ids), theo thứ tự ids: trang thuộc tập nhận 1/|S|,
    trang còn lại nhận 0. Báo ValueError nếu tập chủ đề rỗng hoặc dữ liệu
    nhãn tham chiếu ID ngoài ids. Không dùng nội dung bài để suy ra nhãn.
    """
    # TODO: Sinh viên cài đặt.
    raise NotImplementedError("Chưa cài đặt topic_distribution")


def mix_pageranks(
    topic_scores: list[list[float]], weights: list[float]
) -> list[float]:
    """Ghép các vector PageRank bằng tổng có trọng số theo từng tọa độ.

    topic_scores gồm các vector cùng độ dài, cùng thứ tự đỉnh.
    weights có một trọng số cho mỗi vector, hữu hạn, không âm và có
    tổng lệch 1 không quá 1e-12. Trả một vector có cùng độ dài.
    Cấu hình chính thức dùng thứ tự Science, History, Geography và trọng
    số 0.5, 0.3, 0.2. Không chạy lại PageRank hoặc làm tròn điểm ở đây.
    Báo ValueError nếu danh sách rỗng, kích thước hoặc trọng số không hợp lệ.
    """
    # TODO: Sinh viên cài đặt.
    raise NotImplementedError("Chưa cài đặt mix_pageranks")


_ASCII_UPPER_TO_LOWER = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmnopqrstuvwxyz",
)
_ASCII_WHITESPACE_RE = re.compile(r"[ \t\n\r\v\f]+")

def normalize_text(text: str) -> str:
    r"""Chuẩn hóa chuỗi Unicode theo đúng quy tắc của phần C.

    Chỉ đổi ASCII A–Z thành a–z. Gộp mỗi dãy ký tự thuộc tập dấu cách
    ASCII, \t, \n, \r, \v, \f thành một dấu cách ASCII; bỏ dấu cách ASCII
    ở hai đầu. Giữ nguyên các ký tự khác, dấu câu và toàn bộ nội dung.
    Không chuẩn hóa Unicode, bỏ dấu hoặc gọi lower() cho toàn bộ Unicode.
    Trả chuỗi đã chuẩn hóa; chuỗi rỗng hoặc chỉ có khoảng trắng trên trả ''.
    """
    # TODO: Sinh viên cài đặt.
    lowered = text.translate(_ASCII_UPPER_TO_LOWER)
    return _ASCII_WHITESPACE_RE.sub(" ", lowered).strip(" ")


def shingles(text: str, k: int) -> set[str]:
    """Tạo tập k-shingle từ chuỗi ĐÃ được normalize_text xử lý.

    Mỗi shingle là k code point Unicode liên tiếp, không phải k byte/từ.
    Trả tập chuỗi phân biệt; không lưu số lần xuất hiện hoặc vị trí.
    Chuỗi ngắn hơn k trả tập rỗng. Báo ValueError nếu k không phải số
    nguyên dương. Không chuẩn hóa văn bản thêm lần nữa trong hàm này.
    """
    # TODO: Sinh viên cài đặt.
    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k phải là số nguyên dương")
    if len(text) < k:
        return set()
    return {text[i : i + k] for i in range(len(text) - k + 1)}

def shingle_id(shingle: str, p: int) -> int:
    """Ánh xạ một shingle thành số nguyên trong [0, p-1].

    Băm byte UTF-8 bằng SHA-256, lấy 4 byte đầu, đọc số nguyên không dấu
    big-endian rồi lấy modulo p. Không dùng hash() mặc định của Python.
    Trả int tất định giữa các lần chạy. Báo ValueError nếu p <= 1.
    """
    # TODO: Sinh viên cài đặt.
    if not isinstance(p, int) or isinstance(p, bool) or p <= 1:
        raise ValueError("p phải là số nguyên lớn hơn 1")
    digest = hashlib.sha256(shingle.encode("utf-8")).digest()
    value = int.from_bytes(digest[:4], byteorder="big", signed=False)
    return value % p


def minhash(shingle_ids: set[int], hash_params: dict) -> list[int]:
    """Tính chữ ký từ tập mã shingle và bộ hàm băm dùng chung.

    hash_params có p và hash_functions là danh sách {'a': int, 'b': int}
    theo thứ tự tọa độ. Mỗi tọa độ là min((a*x+b) % p) trên shingle_ids.
    Tập rỗng trả toàn giá trị p. Trả list[int] dài bằng số hàm băm;
    không gắn cứng 128 vì bộ chấm có thể dùng bộ hệ số nhỏ khác.
    Mã đầu vào thuộc [0, p-1]; phép nhân/cộng/modulo dùng số nguyên chính
    xác. Không sinh hệ số mới, không trả ID phần tử đạt min.
    """
    # TODO: Sinh viên cài đặt.
    p = int(hash_params["p"])
    hash_functions = hash_params["hash_functions"]
    if not shingle_ids:
        return [p] * len(hash_functions)
    return [
        min([(fn["a"] * x + fn["b"]) % p for x in shingle_ids])
        for fn in hash_functions
    ]


def jaccard(set_a: set[str], set_b: set[str]) -> float:
    """Tính Jaccard chính xác trên hai tập CHUỖI shingle trước bước băm.

    Trả kích thước giao chia kích thước hợp. Theo quy ước bài tập, hai tập
    rỗng trả 1.0; chỉ một tập rỗng trả 0.0. Không dùng tập mã băm thay thế.
    """
    # TODO: Sinh viên cài đặt.
    raise NotImplementedError("Chưa cài đặt jaccard")


def signature_similarity(
    sig_a: list[int], sig_b: list[int], empty_a: bool, empty_b: bool
) -> float:
    """Ước lượng Jaccard bằng tỷ lệ tọa độ chữ ký trùng nhau.

    Hai chữ ký phải cùng độ dài dương, dùng cùng bộ hàm băm và thứ tự.
    empty_a/empty_b cho biết tập shingle gốc có rỗng hay không.
    Hai tập rỗng trả 1.0; chỉ một tập rỗng trả 0.0. Các trường hợp còn
    lại trả số tọa độ bằng nhau chia độ dài chữ ký. Không chuyển chữ ký
    thành tập. Báo ValueError nếu độ dài không hợp lệ.
    """
    # TODO: Sinh viên cài đặt.
    if len(sig_a) == 0 or len(sig_a) != len(sig_b):
        raise ValueError("Hai chữ ký phải có cùng độ dài dương")
    if empty_a and empty_b:
        return 1.0
    if empty_a or empty_b:
        return 0.0
    matches = sum(1 for a, b in zip(sig_a, sig_b) if a == b)
    return matches / len(sig_a)


def main() -> None:
    """Đọc tham số, gọi các hàm sinh viên và ghi bốn tệp kết quả CSV.

    Chạy từ thư mục gốc bài tập sau khi giải nén dữ liệu vào data/.
    Dùng --help để xem tùy chọn. Import tệp không tự chạy xử lý dữ liệu.
    Khi các hàm TODO đã hoàn thiện, main tạo pagerank.csv,
    topic_pagerank.csv, minhash.csv và similarities.csv trong --output-dir.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument(
        "--hash-params", type=Path, default=Path("assignment/minhash_params.json")
    )
    parser.add_argument(
        "--pairs", type=Path, default=Path("data/pairs.csv"),
        help="CSV có header article_id_a,article_id_b; mặc định dùng bộ cặp Wikispeedia chính thức.",
    )
    parser.add_argument("--beta", type=float, default=0.85)
    parser.add_argument("--tol", type=float, default=1e-10)
    parser.add_argument("--max-iter", type=int, default=1000)
    args = parser.parse_args()

    graph_dir = args.data_dir / "wikispeedia_paths-and-graph"
    text_dir = args.data_dir / "plaintext_articles"
    with args.hash_params.open(encoding="utf-8") as handle:
        hash_params = json.load(handle)
    with args.pairs.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["article_id_a", "article_id_b"]:
            raise ValueError("Tệp cặp cần header article_id_a,article_id_b")
        pairs = [(row["article_id_a"], row["article_id_b"]) for row in reader]

    ids, out_neighbors = load_graph(
        graph_dir / "articles.tsv", graph_dir / "links.tsv"
    )
    required_ids = {article for pair in pairs for article in pair}
    if not required_ids.issubset(set(ids)):
        raise ValueError("Tệp cặp chứa ID không có trong articles.tsv")

    # A. Điểm PageRank toàn cục.
    scores = pagerank(ids, out_neighbors, args.beta, args.tol, args.max_iter)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "pagerank.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["article_id", "score"])
        for i, article in enumerate(ids):
            writer.writerow([article, format(scores[i], ".17g")])

    # B. Ba chủ đề và r_mix trong cùng một tệp.
    topics = ["Science", "History", "Geography"]
    topic_scores = []
    for topic in topics:
        teleport = topic_distribution(
            ids, graph_dir / "categories.tsv", "subject." + topic
        )
        topic_scores.append(
            pagerank(ids, out_neighbors, args.beta, args.tol, args.max_iter, teleport)
        )
    mixed_scores = mix_pageranks(topic_scores, [0.5, 0.3, 0.2])
    with (args.output_dir / "topic_pagerank.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["topic", "article_id", "score"])
        for topic, vector in zip(topics + ["r_mix"], topic_scores + [mixed_scores]):
            for i, article in enumerate(ids):
                writer.writerow([topic, article, format(vector[i], ".17g")])

    # C. Chữ ký cho mọi bài; chỉ giữ tập chuỗi cho các cặp cần so sánh.
    signatures = {}
    pair_shingles = {}
    with (args.output_dir / "minhash.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        length = len(hash_params["hash_functions"])
        writer.writerow(
            ["article_id", "shingle_count"] + [f"h{j:03d}" for j in range(length)]
        )
        for article in ids:
            text = (text_dir / (article + ".txt")).read_text(encoding="utf-8")
            parts = shingles(normalize_text(text), hash_params["shingle_length"])
            codes = {shingle_id(part, hash_params["p"]) for part in parts}
            signature = minhash(codes, hash_params)
            signatures[article] = signature
            if article in required_ids:
                pair_shingles[article] = parts
            writer.writerow([article, len(parts), *signature])

    with (args.output_dir / "similarities.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["article_id_a", "article_id_b", "jaccard_exact", "jaccard_estimate"]
        )
        for article_a, article_b in pairs:
            set_a, set_b = pair_shingles[article_a], pair_shingles[article_b]
            exact = jaccard(set_a, set_b)
            estimate = signature_similarity(
                signatures[article_a], signatures[article_b], not set_a, not set_b
            )
            writer.writerow(
                [article_a, article_b, format(exact, ".17g"), format(estimate, ".17g")]
            )

    print(f"Đã ghi bốn tệp kết quả vào {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
