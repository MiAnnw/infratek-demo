"""
Streamlit Chat App with Gemini Files API Integration
Upload PDF/CSV files and chat about their content with Gemini AI
"""
import streamlit as st
from google import genai
from google.genai import types
import io
import time
from datetime import datetime

# Hardcoded API key for demo
GEMINI_API_KEY = "AIzaSyBjtfQgo5liFcfwKOHvnQRamVlRnGINyEY"

def initialize_session_state():
    """Initialize session state variables"""
    if 'client' not in st.session_state:
        try:
            st.session_state.client = genai.Client(api_key=GEMINI_API_KEY)
            st.session_state.api_connected = True
        except Exception as e:
            st.session_state.client = None
            st.session_state.api_connected = False
            st.error(f"Lỗi kết nối Gemini API: {str(e)}")
    
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'selected_files' not in st.session_state:
        st.session_state.selected_files = []

def get_mime_type(filename: str) -> str:
    """Get MIME type based on file extension"""
    extension = filename.lower().split('.')[-1]
    
    mime_types = {
        'pdf': 'application/pdf',
        'csv': 'text/csv',
        'txt': 'text/plain'
    }
    
    return mime_types.get(extension, 'application/octet-stream')

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def get_file_icon(mime_type: str) -> str:
    """Get emoji icon for file type"""
    if mime_type.startswith('application/pdf'):
        return "📄"
    elif mime_type.startswith('text/csv'):
        return "📊"
    elif mime_type.startswith('text/'):
        return "📝"
    elif 'spreadsheet' in mime_type or 'excel' in mime_type:
        return "📈"
    elif 'document' in mime_type or 'word' in mime_type:
        return "📄"
    else:
        return "📁"

def setup_page():
    """Setup page configuration and styling"""
    st.set_page_config(
        page_title="Đối thoại và tìm kiếm dữ liệu trong file",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .file-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render application header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Tìm kiếm và trò chuyện với dữ liệu</h1>
        <p>Upload PDF/CSV và trò chuyện về nội dung với AI</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar with file upload and management"""
    st.sidebar.header("Trạng thái")
    if st.session_state.api_connected:
        st.sidebar.success("✅ Ready!")
        st.sidebar.info("⏰ Files tự động xóa sau 48 giờ")
    else:
        st.sidebar.error("❌ Lỗi kết nối API")
        return
    
    # File upload section
    st.sidebar.header("📁 Upload Files")
    
    uploaded_files = st.sidebar.file_uploader(
        "Chọn files để upload:",
        type=['pdf', 'csv', 'txt'],
        accept_multiple_files=True,
        help="Hỗ trợ PDF, CSV, TXT"
    )
    
    # Process uploaded files
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Check if file already processed
            file_exists = any(f['name'] == uploaded_file.name for f in st.session_state.uploaded_files)
            
            if not file_exists:
                # Validate file size (max 2GB)
                if uploaded_file.size > 2 * 1024 * 1024 * 1024:
                    st.sidebar.error(f"File {uploaded_file.name} quá lớn (max 2GB)")
                    continue
                
                with st.spinner(f"Đang upload {uploaded_file.name}..."):
                    try:
                        # Read file content
                        file_content = uploaded_file.read()
                        file_io = io.BytesIO(file_content)
                        mime_type = get_mime_type(uploaded_file.name)
                        
                        # Upload to Gemini Files API
                        gemini_file = st.session_state.client.files.upload(
                            file=file_io,
                            config=dict(
                                mime_type=mime_type,
                                display_name=uploaded_file.name
                            )
                        )
                        
                        # Store file info
                        file_info = {
                            'name': uploaded_file.name,
                            'size': uploaded_file.size,
                            'mime_type': mime_type,
                            'gemini_file': gemini_file,
                            'upload_time': datetime.now().strftime("%H:%M:%S")
                        }
                        
                        st.session_state.uploaded_files.append(file_info)
                        st.sidebar.success(f"✅ Upload thành công: {uploaded_file.name}")
                        
                    except Exception as e:
                        st.sidebar.error(f"❌ Upload thất bại {uploaded_file.name}: {str(e)}")
    
    # Display uploaded files
    if st.session_state.uploaded_files:
        st.sidebar.header("📁 Files đã upload")
        
        for i, file_info in enumerate(st.session_state.uploaded_files):
            with st.sidebar.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    icon = get_file_icon(file_info['mime_type'])
                    size = format_file_size(file_info['size'])
                    st.write(f"{icon} **{file_info['name']}**")
                    st.caption(f"Size: {size} | {file_info['upload_time']}")
                
                with col2:
                    if st.button("🗑️", key=f"delete_{i}", help="Xóa file"):
                        try:
                            # Delete from Gemini API - just remove from session state
                            # Files will auto-delete after 48 hours according to API
                            st.session_state.uploaded_files.pop(i)
                            st.sidebar.success(f"✅ Đã xóa {file_info['name']}")
                            st.rerun()
                        except Exception as e:
                            st.sidebar.error(f"Lỗi xóa file: {str(e)}")
        
        # File selection for context
        st.sidebar.header("🎯 Chọn files cho context")
        selected_files = []
        
        for i, file_info in enumerate(st.session_state.uploaded_files):
            icon = get_file_icon(file_info['mime_type'])
            
            if st.sidebar.checkbox(
                f"{icon} {file_info['name']}", 
                key=f"select_{i}",
                help="Sử dụng file này trong chat"
            ):
                selected_files.append(file_info)
        
        st.session_state.selected_files = selected_files
        
        # Clear all files button
        if st.sidebar.button("🗑️ Xóa tất cả files"):
            try:
                # Just clear from session state
                # Files will auto-delete after 48 hours according to API
                st.session_state.uploaded_files = []
                st.session_state.selected_files = []
                st.sidebar.success("✅ Đã xóa tất cả files!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Lỗi xóa files: {str(e)}")
    
    # Statistics
    if st.session_state.uploaded_files or st.session_state.chat_messages:
        st.sidebar.header("📊 Thống kê")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Files", len(st.session_state.uploaded_files))
        with col2:
            st.metric("Messages", len(st.session_state.chat_messages))

def render_chat():
    """Render main chat interface"""
    if not st.session_state.api_connected:
        st.error("❌ Lỗi kết nối Gemini API")
        return
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message.get("files_used"):
                with st.expander("📎 Files được sử dụng"):
                    for file_name in message["files_used"]:
                        st.caption(f"• {file_name}")
    
    # Chat input
    if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
        # Add user message
        files_used = [f['name'] for f in st.session_state.selected_files]
        
        st.session_state.chat_messages.append({
            "role": "user", 
            "content": prompt,
            "files_used": files_used
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
            if files_used:
                with st.expander("📎 Files được sử dụng"):
                    for file_name in files_used:
                        st.caption(f"• {file_name}")
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Đang suy nghĩ..."):
                try:
                    # Prepare content parts
                    content_parts = [prompt]
                    
                    # Add selected files to context
                    for file_info in st.session_state.selected_files:
                        content_parts.append(file_info['gemini_file'])
                    
                    # Generate response
                    response = st.session_state.client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=content_parts,
                        config=types.GenerateContentConfig(
                            system_instruction="""Bạn là một trợ lý AI thông minh chuyên phân tích và trò chuyện về nội dung tài liệu thuộc công ty Infratek.

Vai trò của bạn:
- Phân tích chi tiết nội dung các file PDF, CSV, TXT được người dùng upload
- Trả lời câu hỏi dựa trên thông tin có trong tài liệu
- Cung cấp thông tin chính xác, có căn cứ từ nội dung file
- Giải thích rõ ràng, dễ hiểu bằng tiếng Việt

Nguyên tắc làm việc:
1. Luôn trả lời bằng tiếng Việt
2. Dựa vào nội dung file được cung cấp để trả lời
3. Nếu thông tin không có trong file, hãy nói rõ điều đó
4. Trình bày câu trả lời có cấu trúc, dễ đọc
5. Sử dụng bullet points, số thứ tự khi cần thiết
6. Trích dẫn thông tin cụ thể từ file khi có thể
7. Đưa ra phân tích sâu sắc và insights hữu ích

Khi làm việc với:
- PDF: Đọc và phân tích toàn bộ nội dung văn bản, bảng biểu, cấu trúc
- CSV: Phân tích dữ liệu, thống kê, xu hướng, mối quan hệ giữa các cột
- TXT: Đọc hiểu nội dung văn bản, tóm tắt, phân tích ý chính

Hãy luôn thân thiện, hữu ích và chuyên nghiệp trong mọi phản hồi.""",
                            temperature=0.3,
                            max_output_tokens=2048
                        )
                    )
                    
                    response_text = response.text
                    st.write(response_text)
                    
                    # Add assistant message
                    st.session_state.chat_messages.append({
                        "role": "assistant", 
                        "content": response_text,
                        "files_used": files_used
                    })
                    
                except Exception as e:
                    error_msg = f"Lỗi tạo phản hồi: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })

def render_controls():
    """Render chat control buttons"""
    if not st.session_state.api_connected:
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🆕 Cuộc trò chuyện mới"):
            st.session_state.chat_messages = []
            st.rerun()
    
    with col2:
        if st.button("🗑️ Xóa lịch sử chat"):
            st.session_state.chat_messages = []
            st.rerun()
    
    with col3:
        if st.session_state.chat_messages:
            # Export chat history
            chat_export = "\n".join([
                f"{msg['role'].upper()}: {msg['content']}" 
                for msg in st.session_state.chat_messages
            ])
            
            st.download_button(
                label="📥 Xuất lịch sử chat",
                data=chat_export,
                file_name=f"chat_history_{int(time.time())}.txt",
                mime="text/plain"
            )

def main():
    """Main application function"""
    # Setup
    setup_page()
    initialize_session_state()
    
    # Render components
    render_header()
    render_sidebar()
    render_chat()
    render_controls()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "💡 **Hướng dẫn:** Upload files → Chọn files cho context → Bắt đầu chat!"
    )

if __name__ == "__main__":
    main()