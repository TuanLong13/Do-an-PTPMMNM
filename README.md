[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
# Hex Game

Ứng dụng hỗ trò chơi trò chơi Hex trên 2 PC khác nhau sử dụng thư viện pygame và socket

## Giới thiệu

Hex là một trò chơi bàn cờ chiến lược trừu tượng dành cho hai người chơi, trong đó người chơi cố gắng nối các mặt đối diện của một bảng hình thoi làm bằng các ô lục giác.
Người chơi nào kết nối các ô thành 1 đường nối 1 viền có màu tương ứng với ô đến viền đối diện là người chiến thắng. Trò chơi không có kết quả hoà(xem thêm tại [Wikipedia](https://en.wikipedia.org/wiki/Hex_(board_game)))

![image](https://github.com/TuanLong13/Do-an-PTPMMNM/assets/117003006/f990bfb0-f0f5-446c-be58-8408c599f0f1)
## Hướng dẫn thực hiện

### Yêu cầu

* 2 máy khác nhau

### Cài đặt
* Cài đặt python3.12.3
  
Truy cập đường dẫn [python.org](https://www.python.org/downloads/release/python-3123/) và download phiên bản tương ứng với OS của từng máy

* Cài đặt pygame
```
pip install pygame
```
* Clone repository
```
git clone https://github.com/TuanLong13/Do-an-PTPMMNM.git
```
hoặc download file zip về và giải nén
### Thực thi

#### Config IP của máy chạy server
Ở máy chạy server thực hiện:
* Windows
1. Mở cửa sổ Terminal dưới quyền admin
2. Nhập lệnh: ```netsh interface ipv4 show config``` để hiển thị toàn bô thông tin IP:
![image](https://static1.howtogeekimages.com/wordpress/wp-content/uploads/2023/09/netsh-showing-ipv45-wifi.png)
3. Nhập lệnh: ```netsh interface ipv4 set address name="InterfaceName" static 192.168.2.14 255.255.255.0 DefaultGateway```
   
    ** InterfaceName: có thể là "Wi-Fi" hoặc "Ethernet"
   
    ** DefaultGateway: cùng chỉ số Default Gateway ở vị trí như hình trên
* MACOS
1. Mở cửa sổ Terminal và thực hiện lệnh sau:
```
sudo ipconfig set en1 INFORM 192.168.2.14
```
* Linux
1. Mở cửa số Terminal và thực hiện lệnh: ```ifconfig -a``` để hiển thị toàn bô thông tin IP
2. Nhập lệnh: ```sudo ifconfig interface down``` với interface là ten interface đã chọn
![image](https://linuxier.com/wp-content/uploads/2023/06/disabling-network-interface-1024x697.jpg)
3. Nhập lệnh:
```
sudo ifconfig interface 192.168.2.14 netmask 255.255.255.0 up
```

#### Đối với máy thứ nhất(máy này sẽ host server)
  1. Mở cửa sổ Terminal
  2. Chạy lệnh sau để host server
```
python3 room_server.py
```
  3. Khi server đã chạy, mở thêm 1 cửa số terminal mới
  4. Chạy lệnh sau để hiển thị giao diện(
```
python3 Do-an-PTPMMNM/client1.py
```

#### Đối với máy thứ 2
  1. Mở cửa sổ Terminal.
  2. Chạy lệnh sau để hiển thị giao diện
```
python3 Do-an-PTPMMNM/client2.py
```
#### Nhấn vào nút "Bắt đầu chơi" trên giao diện ở cả 2 máy để mở cửa sổ chat chuẩn bị vào chơi
  
**Lưu ý: nếu nhấn nút "Bắt đầu chơi" trong khi server không chạy sẽ gây đứng ứng dụng. Khi xảy thì chỉ cần force quit ứng dụng và thực hiện lại từ đầu**

## License

This project is licensed under the MIT License
