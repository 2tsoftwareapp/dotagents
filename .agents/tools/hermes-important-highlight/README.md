# Hermes Desktop important highlight

Plugin mã nguồn cho Hermes Desktop, đăng ký directive `::important{...}` để hiển thị một ý chính nổi bật trong phản hồi assistant.

## Cài đặt

Sao chép `plugin.js` vào `$HERMES_HOME/desktop-plugins/important-highlight/plugin.js` (thường là `~/.hermes/desktop-plugins/important-highlight/plugin.js`). Giữ tên thư mục trùng `id` của plugin. Nếu thư mục đích đã tồn tại, không ghi đè; hãy xem xét và hợp nhất thủ công.

Desktop sẽ tự nạp plugin sau vài giây. Nếu chưa thấy, dùng ⌘K → **Reload desktop plugins**. Plugin cần được bật trong Capabilities → Plugins.

Để agent sử dụng cú pháp trong project hiện tại, sao chép `SKILL.md` đi kèm vào `<project>/.agents/skills/hermes-important-highlight/SKILL.md` và đánh dấu repository là tin cậy bằng cơ chế Skills của Hermes nếu cần. Hermes chỉ nạp project skills từ repository tin cậy.

## Dùng thử

```markdown
::important{text="Sao lưu cơ sở dữ liệu trước khi chạy migration."}
```

Directive có thể nằm trong đoạn văn; plugin sẽ render một khối riêng tại vị trí đó. Nếu directive chưa được đăng ký, Hermes giữ nguyên nội dung thành văn bản thông thường.
