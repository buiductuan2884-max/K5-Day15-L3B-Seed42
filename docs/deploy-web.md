# Đưa web demo lên Streamlit Community Cloud

Web chạy trên máy chủ của Streamlit, người khác mở bằng link, không cần máy của nhóm.

1. Mở https://share.streamlit.io, đăng nhập bằng GitHub của chủ repo.
2. **Create app** → Deploy a public app from GitHub.
3. Repository `buiductuan2884-max/K5-Day15-L3B-Seed42` · Branch: nhánh có `codebase/web.py` · Main file path `codebase/web.py`.
4. **Advanced settings** → Python 3.12 → ô **Secrets**, dán và thay giá trị:

```toml
MODEL_PROVIDER = "gemini"
MODEL_NAME = "gemini-3.5-flash-lite"
API_KEY = "key của nhóm"
APP_PASSCODE = "mã nhóm tự đặt"
STAFF_PASSCODE = "mã riêng cho màn nhà xe"
MAX_CALLS = "200"
```

5. **Deploy**. Mở link bằng cửa sổ ẩn danh, nhập mã truy cập, hỏi thử một câu.

Lưu ý:
- Key chỉ nhập ở ô Secrets, không đưa vào file nào trong repo.
- Có `APP_PASSCODE` để người lạ không tiêu tiền của key. `MAX_CALLS` giới hạn số lượt hỏi của máy chủ cho đến khi khởi động lại; nên đặt thêm hạn mức ở trang cấp key.
- Có `APP_PASSCODE` mà thiếu `STAFF_PASSCODE` thì màn "Nhà xe" bị khoá, để người dùng thử không đọc được phiếu của nhau. Đặt hai mã khác nhau.
- Phiếu gửi trên web nằm trong bộ nhớ máy chủ: mất khi app khởi động lại hoặc ngủ dậy.
- App lâu không ai mở sẽ ngủ; mở link và bấm đánh thức vài phút trước giờ demo.
- Câu khách gõ được gửi tới nhà cung cấp model. Chỉ gõ dữ liệu giả.
