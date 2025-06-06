# 🤖 Gemini Chat với Files

Ứng dụng Streamlit cho phép upload PDF/CSV và trò chuyện về nội dung với Gemini AI.

## ✨ Tính năng

- 📁 **Upload Files**: Hỗ trợ PDF, CSV, TXT, JSON, Excel, Word
- 💬 **Chat AI**: Trò chuyện về nội dung file với Gemini
- 🎯 **Context Selection**: Chọn files cụ thể cho cuộc trò chuyện
- 📊 **File Management**: Quản lý, xóa files đã upload
- 💾 **Chat History**: Lưu và xuất lịch sử chat
- 📈 **Statistics**: Thống kê sử dụng

## 🚀 Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd streamlit
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng
```bash
streamlit run app.py
```

## 📖 Hướng dẫn sử dụng

### Bước 1: Upload Files
- Trong sidebar, tìm section "📁 Upload Files"
- Click "Browse files" hoặc kéo thả file
- Hỗ trợ các định dạng:
  - **PDF**: Tài liệu PDF
  - **CSV**: Dữ liệu bảng tính
  - **TXT**: File văn bản thuần túy

### Bước 2: Chọn Files cho Context
- Trong sidebar "🎯 Chọn files cho context"
- Tick chọn files muốn sử dụng trong cuộc trò chuyện
- Có thể chọn nhiều files cùng lúc

### Bước 3: Bắt đầu Chat
- Nhập câu hỏi trong ô chat
- AI sẽ phân tích nội dung files đã chọn
- Trả lời dựa trên context của files

## 🏗️ Cấu trúc Project

```
streamlit/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── gemini_client.py   # Gemini API wrapper
│   ├── file_manager.py    # File upload/management
│   └── chat_manager.py    # Chat logic & history
└── README.md             # This file
```

## 🔧 Cấu hình

### Cấu hình API
- **API Key**: Đã được cấu hình sẵn trong ứng dụng
- **Model**: gemini-2.0-flash

### API Limits
- **File size**: Tối đa 2GB per file
- **Storage**: Tối đa 20GB total
- **Retention**: Files tự động xóa sau 48 giờ
- **Supported formats**: PDF, CSV, TXT

### Models
- **Default**: `gemini-2.0-flash`
- **Temperature**: 0.7
- **Max tokens**: 2048

## 📚 API Documentation

### Gemini Files API
- [Files API Guide](https://ai.google.dev/gemini-api/docs/files)
- [Document Processing](https://ai.google.dev/gemini-api/docs/document-processing)
- [Generate Content API](https://ai.google.dev/api/generate-content)

### Key Features Used
- **File Upload**: Upload files lên Gemini Files API
- **Content Generation**: Tạo nội dung với file context
- **Document Processing**: Xử lý PDF với native vision
- **Chat Interface**: Duy trì cuộc hội thoại

## 🛠️ Development

### Cấu trúc Code

#### `utils/gemini_client.py`
- Wrapper cho Gemini API
- Upload/delete files
- Generate content với file context
- Streaming responses

#### `utils/file_manager.py`
- Quản lý files trong session state
- Validation & formatting
- File type detection
- Context selection

#### `utils/chat_manager.py`
- Quản lý lịch sử chat
- Export chat history
- Conversation grouping
- Search functionality

#### `app.py`
- Main Streamlit interface
- UI components
- Event handling
- State management

### Thêm tính năng mới

1. **Thêm file type mới**:
   - Cập nhật `get_mime_type()` trong `gemini_client.py`
   - Thêm validation trong `file_manager.py`

2. **Thêm model mới**:
   - Cập nhật `generate_content()` method
   - Thêm model selection UI

3. **Thêm export format**:
   - Cập nhật `export_chat_history()` method
   - Thêm format options

## 🐛 Troubleshooting

### Lỗi kết nối API
```
❌ Lỗi kết nối Gemini API
```
**Giải pháp**: Thử lại sau hoặc kiểm tra kết nối internet

### Lỗi Upload File
```
File quá lớn. Kích thước tối đa là 2GB
```
**Giải pháp**: Giảm kích thước file hoặc chia nhỏ file

### Lỗi Generate Content
```
Xin lỗi, tôi không thể tạo phản hồi
```
**Giải pháp**: 
- Kiểm tra file đã upload thành công
- Thử lại với câu hỏi khác
- Kiểm tra API quota

### File không hiển thị
**Giải pháp**:
- Refresh trang
- Kiểm tra file đã upload thành công
- Xóa và upload lại

## 📝 Examples

### Chat với PDF
```
User: "Tóm tắt nội dung chính của tài liệu này"
AI: "Dựa trên PDF bạn đã upload, tài liệu này nói về..."
```

### Chat với CSV
```
User: "Phân tích dữ liệu trong file CSV này"
AI: "File CSV chứa X hàng và Y cột. Các insights chính là..."
```

### Multi-file Context
```
User: "So sánh dữ liệu giữa 2 files này"
AI: "Dựa trên file PDF và CSV bạn chọn, sự khác biệt chính là..."
```

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - xem file LICENSE để biết chi tiết.

## 🆘 Support

- **Issues**: Tạo issue trên GitHub
- **Documentation**: Xem Gemini API docs
- **Community**: Streamlit community forum

---

**Made with ❤️ using Streamlit & Gemini AI**