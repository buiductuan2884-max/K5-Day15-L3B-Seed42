// Dán vào https://script.google.com (Dự án mới), chọn hàm taoForm rồi bấm Chạy.
// Link trả lời và link sửa form hiện ở Nhật ký thực thi.
function taoForm() {
  var f = FormApp.create('Khảo sát: lần gần nhất bạn đặt vé xe khách');
  f.setDescription('2 phút, hỏi về chuyện đã xảy ra với bạn. Không hỏi tên, email, số điện thoại. ' +
    'Đừng ghi mã vé, số thẻ hay thông tin cá nhân vào ô trả lời. Kết quả chỉ dùng cho bài hackathon của nhóm Seed42.');
  f.setCollectEmail(false);

  function chon(title, choices, other) {
    var q = f.addMultipleChoiceItem().setTitle(title).setRequired(true);
    q.setChoiceValues(choices);
    if (other) q.showOtherOption(true);
    return q;
  }
  function nhieu(title, choices) {
    f.addCheckboxItem().setTitle(title).setChoiceValues(choices).showOtherOption(true).setRequired(true);
  }

  var loc = f.addMultipleChoiceItem().setRequired(true)
    .setTitle('1. Trong 6 tháng qua, bạn có đặt vé xe khách (qua app, web, điện thoại hoặc tại bến) không?');
  f.addPageBreakItem().setTitle('Lần gần nhất');
  loc.setChoices([
    loc.createChoice('Có', FormApp.PageNavigationType.CONTINUE),
    loc.createChoice('Không', FormApp.PageNavigationType.SUBMIT)
  ]);

  chon('2. Lần gần nhất bạn đặt vé là khi nào?', ['Trong 1 tuần qua', 'Trong 1 tháng qua', '1 đến 3 tháng trước', 'Lâu hơn 3 tháng']);
  chon('3. Lần đó bạn đặt bằng cách nào?', ['App đặt vé', 'Web hoặc app của nhà xe', 'Gọi điện', 'Mua tại bến'], true);
  nhieu('4. Lần đó bạn cần tìm hiểu hoặc xử lý việc gì ngoài chuyện đặt vé?', [
    'Giờ chạy', 'Giá vé', 'Điểm đón, trả', 'Quy định (hành lý, trẻ em, thú cưng...)',
    'Đổi hoặc huỷ vé', 'Hoàn tiền hoặc bị trừ tiền sai', 'Nhà xe đổi giờ, huỷ chuyến, không giữ chỗ', 'Không cần gì thêm']);
  nhieu('5. Bạn đã làm thế nào để xong việc đó?', [
    'Tự tìm trong app hoặc web', 'Gọi tổng đài hoặc nhà xe', 'Nhắn tin, email, fanpage', 'Hỏi người quen', 'Bỏ qua', 'Không cần làm gì']);
  chon('6. Việc đó mất tổng cộng khoảng bao lâu (tính cả chờ trả lời)?', [
    'Không có việc gì phải xử lý', 'Dưới 5 phút', '5 đến 15 phút', '15 đến 30 phút', '30 phút đến 1 ngày', 'Hơn 1 ngày']);
  chon('7. Cuối cùng việc đó có xong không?', ['Xong', 'Xong một phần', 'Không xong', 'Không có việc gì phải xử lý']);
  chon('8. Trong 3 tháng qua, bạn phải hỏi hoặc xử lý những việc như vậy mấy lần?', ['0', '1', '2 đến 3', '4 lần trở lên']);
  f.addParagraphTextItem().setTitle('9. Kể ngắn điều khó chịu nhất ở lần gần nhất (không ghi tên, mã vé, số điện thoại).');

  try { f.setPublished(true); } catch (e) {}
  Logger.log('Link gửi người trả lời: ' + f.getPublishedUrl());
  Logger.log('Link sửa form: ' + f.getEditUrl());
}
