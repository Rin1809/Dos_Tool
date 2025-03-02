@echo off

:: Tên môi trường ảo (bạn có thể thay đổi)
set VENV_NAME=moitruongao

:: Kiểm tra xem môi trường ảo đã tồn tại chưa
IF EXIST "%VENV_NAME%\Scripts\activate" (
    echo Dang khoi dong moi truong ao...
    call "%VENV_NAME%\Scripts\activate"
) ELSE (
    echo Khong tim thay moi truong ao. Tu dong tao...
    python -m venv %VENV_NAME%
    call "%VENV_NAME%\Scripts\activate"
    echo Dang Tai Thu Vien...
    pip install -r requirements.txt
)

:: Chạy ứng dụng
echo Dang Chay Ung Dung...
python Tool.py

:: Tạm dừng để xem kết quả (nếu cần)
pause
