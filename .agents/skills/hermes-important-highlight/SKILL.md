---
name: hermes-important-highlight
description: "Dùng khi phản hồi trong Hermes Desktop cần làm nổi bật một kết luận hoặc cảnh báo then chốt bằng directive inline. Chỉ đánh dấu tối đa một ý chính; nếu directive không khả dụng, dùng Markdown in đậm."
---

# Làm nổi bật ý quan trọng trong Hermes Desktop

Khi phản hồi có một kết luận, cảnh báo hoặc hành động quan trọng mà người dùng cần nhận ra ngay, hãy đặt đúng **một ý quan trọng nhất** vào directive riêng:

```markdown
::important{text="Nội dung ngắn, tự đủ nghĩa, tối đa 1000 ký tự."}
```

## Quy tắc

- Chỉ dùng cho ý có tác động thực tế: kết luận trả lời câu hỏi, cảnh báo cần hành động, quyết định hoặc blocker. Không tô nổi bật lời dẫn, trạng thái thường lệ hay từng bullet.
- Chọn tối đa một directive trong mỗi phản hồi; giữ các chi tiết hỗ trợ ở phần văn bản thường.
- Viết nguyên câu dễ hiểu độc lập. Dùng cú pháp attribute có dấu ngoặc kép; escape dấu `"` bên trong nếu có.
- Đặt directive gần phần giải thích liên quan, thường ở đầu hoặc cuối câu trả lời.
- Nếu giao diện không hỗ trợ directive, viết ý đó bằng `**in đậm**`; không lặp cả hai cách khi directive đã render thành khối.
- Directive xuất hiện dạng chữ inline, không có khung/nền. Khi assistant hoàn tất phản hồi, ý chính chỉ đổi sang màu nhấn và có quầng sáng nhẹ; không scale chữ. Các phần chữ khác trong cùng phản hồi mờ còn 18% độ rõ trong 1,8 giây, rồi tự trở lại bình thường. `prefers-reduced-motion` tắt chuyển động.

Ví dụ:

```markdown
::important{text="Dữ liệu hiện tại chưa được sao lưu; hãy tạo bản sao trước khi chạy migration."}

Migration có thể rollback bằng lệnh `db rollback` nếu bước xác minh thất bại.
```
