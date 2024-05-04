# Hex Game

Ứng dụng hỗ trò chơi trò chơi Hex trên 2 PC khác nhau sử dụng thư viện pygame và socket

## Giới thiệu

Hex là một trò chơi bàn cờ chiến lược trừu tượng dành cho hai người chơi, trong đó người chơi cố gắng nối các mặt đối diện của một bảng hình thoi làm bằng các ô lục giác.
Người chơi nào kết nối các ô thành 1 đường nối 1 viền có màu tương ứng với ô đến viền đối diện là người chiến thắng. Trò chơi không có kết quả hoà(xem thêm tại [Wikipedia](https://en.wikipedia.org/wiki/Hex_(board_game)))

![image](https://github.com/TuanLong13/Do-an-PTPMMNM/assets/117003006/f990bfb0-f0f5-446c-be58-8408c599f0f1)
## Hướng dẫn thực hiện

### Yêu cầu

* Chạy được trên các hệ điều hành Windows, MacOS, Linux...(Đối với hệ điều hành Windows đôi khi phải được firewall cho phép mới có thể chạy)
* Đã cài đặt Python3 và thư viện pygame
* 2 máy riêng biệt(có thể sử dụng máy ảo)

### Cài đặt

* Clone repository
```
git clone https://github.com/TuanLong13/Do-an-PTPMMNM.git
```
hoặc download file zip về và giải nén
### Thự thi

#### Lưu ý trước khi thực thi: 
* Các lệnh thực hiện dưới đây chỉ là ví dụ
* Thư mục chứa python3 có thể khác nhau ở mỗi máy và đường dẫn đến thư mục của ứng dụng phụ thuộc vào vị trí cài đặt

#### Các bước thực hiện
* Đối với máy thứ nhất(máy này sẽ host server)
  1. Mở cửa sổ Terminal.
  2. Chạy lệnh sau để host server
```
/usr/local/bin/python3 ~/Downloads/Do-an-PTPMMNM/room_server.py
```
  3. Khi server đã chạy, mở thêm 1 cửa số terminal mới
  4. Chạy lệnh sau để hiển thị giao diện(
```
/usr/local/bin/python3 ~/Downloads/Do-an-PTPMMNM/client1.py
```

* Đối với máy thứ 2
  1. Mở cửa sổ Terminal.
  2. Chạy lệnh sau để hiển thị giao diện
```
/usr/local/bin/python3 ~/Downloads/Do-an-PTPMMNM/client2.py
```
* Nhấn vào nút "Bắt đầu chơi" trên giao diện ở cả 2 máy để mở cửa sổ chat chuẩn bị vào chơi
  
**Lưu ý: nếu nhấn nút "Bắt đầu chơi" trong khi server không chạy sẽ gây đứng ứng dụng. Khi xảy thì chỉ cần force quit ứng dụng và thực hiện lại từ đầu**


