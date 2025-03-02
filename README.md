# Dos Tool ᓚᘏᗢ



<details>
<summary> 🇻🇳  Tiếng Việt</summary>

## Mô tả

**Dos Tool** là một công cụ mã nguồn mở được viết bằng Python, cho phép bạn thực hiện các cuộc tấn công DoS (Từ chối Dịch vụ) vào các máy chủ web. Công cụ này hỗ trợ nhiều phương thức tấn công khác nhau, bao gồm:

*   **GET Flood:** Gửi một lượng lớn các yêu cầu GET đến máy chủ mục tiêu.
*   **POST Flood:** Gửi một lượng lớn các yêu cầu POST với dữ liệu ngẫu nhiên đến máy chủ mục tiêu.
*   **Mixed HTTP Methods:**  Kết hợp các phương thức HTTP khác nhau (GET, POST, PUT, DELETE) để tấn công.
*   **Slowloris:** Duy trì nhiều kết nối HTTP đến máy chủ mục tiêu, nhưng chỉ gửi các header không hoàn chỉnh, làm cạn kiệt tài nguyên của máy chủ.
*   **R.U.D.Y (R-U-Dead-Yet):** Gửi các yêu cầu POST với trường `Content-Length` rất lớn, nhưng sau đó gửi dữ liệu thực tế rất chậm, từng byte một, làm máy chủ phải chờ đợi trong thời gian dài.
*  **Search Engine Attack:**  Gửi requests đến trang tìm kiếm (ví dụ như: /search?=...).

Công cụ cũng cho phép bạn tùy chỉnh các tham số như số lượng luồng, thời gian tấn công, User-Agent, cookie, và nhiều tham số khác.

## ⚠️ Cảnh báo ⚠️

*   **Trách nhiệm pháp lý:** Việc sử dụng công cụ này để tấn công các hệ thống mà bạn không có quyền truy cập là **bất hợp pháp** và có thể dẫn đến hậu quả pháp lý nghiêm trọng.  Chỉ sử dụng công cụ này trên các hệ thống mà bạn có quyền kiểm thử.
*   **Ảnh hưởng đến hệ thống:** Các cuộc tấn công DoS có thể làm gián đoạn hoặc ngừng hoạt động của các dịch vụ trực tuyến. Hãy cân nhắc kỹ lưỡng trước khi thực hiện tấn công.
*   **Mục đích giáo dục:** Công cụ này được thiết kế cho mục đích giáo dục và nghiên cứu bảo mật. Tác giả không chịu trách nhiệm cho bất kỳ hành vi sử dụng sai mục đích nào.

## Các tính năng chính

*   **Đa luồng:** Tấn công đồng thời bằng nhiều luồng, tăng hiệu quả tấn công.
*   **Tùy biến cao:**  Cho phép tùy chỉnh nhiều tham số như:
    *   Số lượng luồng.
    *   Thời gian tấn công.
    *   User-Agent (từ file hoặc thủ công).
    *   Cookie.
    *   Headers tùy chỉnh (cho Slowloris và R.U.D.Y).
    *   Tốc độ làm mới (cập nhật thông tin).
*   **Hỗ trợ nhiều phương thức tấn công:** GET, POST, PUT, DELETE, Slowloris, R.U.D.Y, và Search Engine Attack.
*   **Giao diện trực quan:** Sử dụng thư viện `rich` để hiển thị thông tin trạng thái tấn công một cách đẹp mắt và dễ theo dõi.
*   **Logging:** Ghi lại log của cuộc tấn công vào file (tùy chọn).
*   **Tự động tạo User-Agent, Request:** Nếu bạn chọn.

## Cài đặt

1.  **Cài đặt Python:** Đảm bảo bạn đã cài đặt Python 3.7 trở lên.
2.  **Clone repository (hoặc tải xuống):**
    ```bash
    git clone https://github.com/Rin1809/Dos_Tool.git
    cd Dos-Tool
    ```
3.   **(Tùy chọn) Tạo và kích hoạt môi trường ảo:**  Điều này được khuyến nghị để tránh xung đột thư viện.
    ```bash
     python -m venv moitruongao
    ```

    * Trên window:
        ```
        moitruongao\Scripts\activate
        ```

    * Trên (Linux/macOS):
         ```
         source moitruongao/bin/activate
         ```
4.  **Cài đặt các thư viện cần thiết:**  `requirements.txt` đã được tạo sẵn (nằm trong folder).
    *Nếu chưa có `requirements.txt` hãy tạo thủ công (với nội dung liệt kê các thư viện sau):
        ```
        requests
        aiohttp
        rich
        ```
     ```bash
     pip install -r requirements.txt
     ```

## Cách sử dụng

1.  **Chạy file `run.bat`:** File này sẽ tự động kiểm tra và cài đặt môi trường ảo (nếu chưa có), cài đặt các thư viện cần thiết, và sau đó chạy công cụ.

2.  **Nhập các tham số:**  Công cụ sẽ yêu cầu bạn nhập các thông tin sau:
    *   **Chế độ tấn công:**  Chọn một trong các chế độ:
        *   **1:** Tấn công GET đơn giản (mặc định).
        *   **2:** Tấn công TÙY CHỈNH (cho phép chọn nhiều phương thức HTTP).
        *   **3:** Tấn công Slowloris.
        *   **4:** Tấn công R.U.D.Y.
        *   **5:**  Tấn công SEARCH
    *   **URL mục tiêu:**
        *   **Từ file:**  Nhập tên file chứa danh sách các URL (mỗi URL một dòng). Ví dụ: `urls.txt`.
        *   **Thủ công:** Nhập trực tiếp URL, ví dụ: `https://example.com`.
        *  Với Search engine, bạn nhập URL có dạng: `https://yurineko.my/search?query=` (Nếu thủ công), và làm theo hướng dẫn.
    *   **Số lượng luồng:**  Số lượng kết nối đồng thời (ví dụ: 100).
    *   **Tốc độ làm mới (refresh rate):**  Thời gian cập nhật thông tin trạng thái (ví dụ: 0.5 giây).
    *   **Thời gian tấn công:**  Thời gian tấn công (giây). Nhập `0` để tấn công vĩnh viễn (không khuyến khích).
    *   **Tùy chọn phương thức HTTP (nếu chọn chế độ TÙY CHỈNH):**  Nhập các phương thức tấn công, cách nhau bởi dấu phẩy, ví dụ: `GET, POST, PUT`.  Hoặc nhập `ALL` để chọn tất cả.
    *   **Tùy chọn cookie:**  Nếu muốn thêm cookie, nhập `y` và nhập giá trị cookie. Nếu không, nhập `n`.
    *   **Tùy chọn User-Agent:**
        *   **Từ file:**  Nhập tên file chứa danh sách User-Agent (mỗi User-Agent một dòng). Ví dụ: `user_agents.txt`.
        *   **Thủ công:** Nhập User-Agent trực tiếp.
    * **(Chỉ với SLOWLORIS) Ports**  chọn: `80` (HTTP), `443` (HTTPS), hoặc cả hai (`3`).
    * **(Chỉ với SLOWLORIS và R.U.D.Y)**  Chọn lấy header `tự động` hay `thủ công`.
    *   **Lưu log:**  Nếu muốn lưu log, nhập `y`. Nếu không, nhập `n`.

3.  **Theo dõi tiến trình:** Công cụ sẽ hiển thị bảng trạng thái tấn công, bao gồm các thông tin:
    *   Tổng số luồng.
    *   Tổng số yêu cầu.
    *   Số yêu cầu thành công.
    *   Số yêu cầu thất bại.
    *   Thời gian đã trôi qua.
    *   Tiến trình chi tiết cho từng URL (đã hoàn thành / tổng số, phần trăm, tốc độ).
    *   Log các hoạt động gần đây (10 hoạt động cuối).

4.  **Dừng tấn công:**  Nhấn `Ctrl + C` để dừng tấn công.

## Ví dụ chi tiết (rất chi tiết, từng option 1)

**Ví dụ 1: Tấn công GET đơn giản vào một URL**

1.  Chạy `run.bat`.
2.  Chọn chế độ tấn công: `1` (GET).
3.  Chọn cách nhập URL: `2` (thủ công).
4.  Nhập URL: `https://example.com`.
5.  Nhập số luồng: `50`.
6.  Nhập tốc độ làm mới: `0.5`.
7.  Nhập thời gian tấn công: `60` (tấn công trong 60 giây).
8.  Thêm cookie?: `n`.
9.  Chọn User-Agent: `2` (thủ công).
10. Nhập User-Agent: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36`.
11. Lưu log?: `y`.

**Ví dụ 2: Tấn công tùy chỉnh với nhiều phương thức HTTP vào nhiều URL từ file**

1.  Tạo một file `urls.txt` với nội dung sau (mỗi URL một dòng):

    ```
    https://example.com
    https://example.net
    https://example.org
    ```
2.  Chạy `run.bat`.
3.  Chọn chế độ tấn công: `2` (TÙY CHỈNH).
4.  Chọn cách nhập URL: `1` (từ file).
5.  Nhập tên file: `urls.txt`.
6.  Nhập số luồng: `100`.
7.  Nhập tốc độ làm mới: `1`.
8.  Nhập thời gian tấn công: `0` (tấn công vĩnh viễn - *không khuyến khích*, hãy cẩn thận!).
9.  Chọn các phương thức HTTP: `GET, POST`.
10. Thêm cookie?: `y`.
11. Nhập giá trị cookie: `sessionid=abcdef123456; csrftoken=xyz789`.
12. Chọn User-Agent: `1` (từ file).
13. Nhập tên file chứa User-Agent: `user_agents.txt` (bạn cần tạo file này, mỗi dòng một User-Agent).
14. Lưu log?: `n`.

**Ví dụ 3: Tấn công Slowloris**

1.  Chạy `run.bat`
2.  Chọn chế độ tấn công: `3` (Slowloris).
3.  Chọn cách nhập URL: `2` (Nhập thủ công)
4. Nhập URL: `http://example.com`
5. Nhập số lượng: `200`.
6.  Nhập tốc độ làm mới: `0.5`.
7. Nhập thời gian tấn công `30`.
8. Thêm cookie: `n`.
9. Chọn cách lấy headers: `1` (tự động) (Với Slowloris thì nên tự động)
10. Chọn cổng tấn công `3` (Cả hai 80 và 443)
11. Lưu log: `n`

**Ví dụ 4: Tấn công R.U.D.Y.**
Tương tự như trên, nhưng:
 *  Chọn chế độ tấn công `4`.
 * Nên chọn lấy Headers `tự động`.

**Ví dụ 5: Tấn công Search engine**
1.  Chạy `run.bat`
2.  Chọn chế độ tấn công: `5`.
3.  Chọn cách nhập URL: `2` (thủ công)
4. Nhập url search: `https://example.com/search?q=`.
5. Chọn `Có` muốn thêm từ khóa tìm kiếm không?: `y`
6. Nhập từ khóa: `dos,attack,python`.
7.  Và nhập các thông tin khác (threads, time,...)

**Lưu ý quan trọng về Slowloris và R.U.D.Y:**

*   Hai phương thức tấn công này khai thác các lỗ hổng ở tầng ứng dụng (Layer 7), không phải tầng mạng (Layer 3/4 như SYN Flood).
*   Chúng hoạt động bằng cách làm cho máy chủ web "bận rộn" với các kết nối dở dang, thay vì làm quá tải băng thông.
*   Cần điều chỉnh các tham số (như số lượng luồng, thời gian chờ) cho phù hợp với từng mục tiêu.

</details>

<details>
<summary> 🇬🇧 English</summary>

## Description

**Dos Tool** is an open-source tool written in Python that allows you to perform DoS (Denial of Service) attacks on web servers.  This tool supports various attack methods, including:

*   **GET Flood:** Sends a large number of GET requests to the target server.
*   **POST Flood:** Sends a large number of POST requests with random data to the target server.
*   **Mixed HTTP Methods:** Combines different HTTP methods (GET, POST, PUT, DELETE) to attack.
*   **Slowloris:** Maintains multiple HTTP connections to the target server, but only sends incomplete headers, exhausting the server's resources.
*   **R.U.D.Y (R-U-Dead-Yet):** Sends POST requests with a very large `Content-Length` field, but then sends the actual data very slowly, byte by byte, forcing the server to wait for a long time.
* **Search Engine Attack:** Sends requests to a search page (eg: /search?=...).

The tool also allows you to customize parameters such as the number of threads, attack duration, User-Agent, cookies, and more.

## ⚠️ Warning ⚠️

*   **Legal Responsibility:** Using this tool to attack systems that you do not have access to is **illegal** and can lead to serious legal consequences. Only use this tool on systems that you have permission to test.
*   **System Impact:** DoS attacks can disrupt or shut down online services. Consider carefully before carrying out an attack.
*   **Educational Purpose:** This tool is designed for educational and security research purposes. The author is not responsible for any misuse.

## Key Features

*   **Multi-threaded:** Attack simultaneously with multiple threads, increasing attack effectiveness.
*   **Highly Customizable:**  Allows you to customize many parameters such as:
    *   Number of threads.
    *   Attack duration.
    *   User-Agent (from file or manually).
    *   Cookies.
    *   Custom Headers (for Slowloris and R.U.D.Y).
    * Refresh Rate.
*   **Supports multiple attack methods:** GET, POST, PUT, DELETE, Slowloris, R.U.D.Y, and Search Engine Attack.
*   **Intuitive Interface:** Uses the `rich` library to display attack status information in a beautiful and easy-to-follow way.
*   **Logging:**  Logs the attack to a file (optional).
* **Auto generate User-Agent, Requests headers** (If you choose)

## Installation

1.  **Install Python:** Make sure you have Python 3.7 or later installed.
2.  **Clone the repository (or download):**
    ```bash
    git clone https://github.com/Rin1809/Dos_Tool.git)
    cd Dos-Tool
    ```
3.  **(Optional) Create and activate a virtual environment:**  This is recommended to avoid library conflicts.
     ```bash
     python -m venv venv
     ```
     * On Windows:
        ```
        venv\Scripts\activate
        ```
     * On Linux/macOS:
        ```
         source venv/bin/activate
        ```

4.  **Install the required libraries:** `requirements.txt` is included in the folder.
      *If `requirements.txt` is missing, create one manually (list these libs):
        ```
        requests
        aiohttp
        rich
        ```
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the `run.bat` file:** This file will automatically check and install the virtual environment (if it doesn't exist), install the necessary libraries, and then run the tool.

2.  **Enter the parameters:** The tool will ask you to enter the following information:
    *   **Attack Mode:**  Choose one of the following modes:
        *   **1:** Simple GET attack (default).
        *   **2:** CUSTOM attack (allows you to select multiple HTTP methods).
        *   **3:** Slowloris attack.
        *   **4:** R.U.D.Y attack.
        * **5:** Search Attack.
    *   **Target URL:**
        *   **From file:** Enter the name of the file containing the list of URLs (one URL per line).  Example: `urls.txt`.
        *   **Manually:** Enter the URL directly, for example: `https://example.com`.
        * With search engines, use URLs like: `https://yurineko.my/search?query=` (Manually), follow instructions.
    *   **Number of threads:**  The number of concurrent connections (e.g., 100).
    *   **Refresh rate:** The time to update the status information (e.g., 0.5 seconds).
    *   **Attack time:**  The duration of the attack (seconds). Enter `0` for a perpetual attack (not recommended).
    *   **HTTP method options (if CUSTOM mode is selected):** Enter the attack methods, separated by commas, for example: `GET, POST, PUT`. Or enter `ALL` to select all.
    *   **Cookie options:** If you want to add a cookie, enter `y` and enter the cookie value.  Otherwise, enter `n`.
    *   **User-Agent options:**
        *   **From file:**  Enter the name of the file containing the User-Agent list (one User-Agent per line). Example: `user_agents.txt`.
        *   **Manually:** Enter the User-Agent directly.
    * **(SLOWLORIS only)**:  Select ports `80` (HTTP), `443` (HTTPS), or both (`3`).
    * **(SLOWLORIS and R.U.D.Y only):** Select headers are generated `automatically` or `manually`.
    *   **Save log:**  If you want to save the log, enter `y`.  Otherwise, enter `n`.

3.  **Monitor progress:**  The tool will display an attack status table, including information:
    *   Total number of threads.
    *   Total number of requests.
    *   Number of successful requests.
    *   Number of failed requests.
    *   Elapsed time.
    *   Detailed progress for each URL (completed / total, percentage, speed).
    *   Log of recent activity (last 10 activities).

4.  **Stop attack:** Press `Ctrl + C` to stop the attack.

## Detailed Examples

**Example 1: Simple GET attack on a single URL**

1.  Run `run.bat`.
2.  Choose attack mode: `1` (GET).
3.  Choose how to enter the URL: `2` (manually).
4.  Enter URL: `https://example.com`.
5.  Enter the number of threads: `50`.
6.  Enter refresh rate: `0.5`.
7.  Enter attack time: `60` (attack for 60 seconds).
8.  Add cookie?: `n`.
9.  Choose User-Agent: `2` (manually).
10. Enter User-Agent: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36`.
11. Save log?: `y`.

**Example 2: Custom attack with multiple HTTP methods on multiple URLs from a file**

1.  Create a `urls.txt` file with the following content (one URL per line):

    ```
    https://example.com
    https://example.net
    https://example.org
    ```

2.  Run `run.bat`.
3.  Choose attack mode: `2` (CUSTOM).
4.  Choose how to enter the URL: `1` (from file).
5.  Enter file name: `urls.txt`.
6.  Enter number of threads: `100`.
7.  Enter refresh rate: `1`.
8.  Enter attack time: `0` (perpetual attack - *not recommended*, be careful!).
9.  Choose HTTP methods: `GET, POST`.
10. Add cookie?: `y`.
11. Enter cookie value: `sessionid=abcdef123456; csrftoken=xyz789`.
12. Choose User-Agent: `1` (from file).
13. Enter the name of the User-Agent file: `user_agents.txt` (you need to create this file, one User-Agent per line).
14. Save log?: `n`.

**Example 3: Slowloris Attack**

1.  Run `run.bat`
2.  Choose attack mode: `3` (Slowloris)
3. Choose how to input url: `2` (Manually)
4. Enter url `http://example.com`.
5. Enter threads: `200`
6. Enter refresh rate `0.5`.
7. Enter attack time: `30`
8. Add cookie: `n`
9. Choose headers method: `1` (automatically)
10. Choose attack ports: `3` (both 80 and 443).
11. Save log?: `n`

**Example 4: R.U.D.Y. Attack**
Similar, but:
   * Select mode `4`.
   * Recommend to get headers `automatically`.

**Example 5: Search Engine Attack**
1. Run `run.bat`.
2. Choose attack mode: `5` (Search).
3. Choose url input `2` (Manually).
4. Enter url `https://example.com/search?q=`.
5.  Select `y` to input keywords.
6. Input: `dos,attack,python`
7. And input others infomations (threads, time,...)

**Important notes about Slowloris and R.U.D.Y.:**

*   These two attack methods exploit vulnerabilities in the application layer (Layer 7), not the network layer (Layer 3/4 like SYN Flood).
*   They work by keeping web servers "busy" with dangling connections, rather than overloading bandwidth.
*   Parameters (such as number of threads, timeouts) need to be adjusted for each target.
</details>

<details>
<summary> 🇯🇵 日本語</summary>

## 説明

**Dos Tool** は、Python で書かれたオープンソースのツールで、Web サーバーに対して DoS (Denial of Service) 攻撃を実行できます。このツールは、次のようなさまざまな攻撃方法をサポートしています。

*   **GET Flood:** 大量のリクエストをターゲット サーバーに送信します。
*   **POST Flood:** ランダムなデータを含む大量の POST リクエストをターゲット サーバーに送信します。
*   **Mixed HTTP Methods:** さまざまな HTTP メソッド (GET、POST、PUT、DELETE) を組み合わせて攻撃します。
*   **Slowloris:** ターゲット サーバーへの複数の HTTP 接続を維持しますが、不完全なヘッダーのみを送信し、サーバーのリソースを使い果たします。
*   **R.U.D.Y (R-U-Dead-Yet):** 非常に大きな `Content-Length` フィールドを持つ POST リクエストを送信しますが、実際のデータを非常にゆっくりと (1 バイトずつ) 送信し、サーバーを長時間待機させます。
*   **検索エンジンの攻撃:** 検索ページへのリクエストを送信します (例: /search?=...)。

このツールでは、スレッド数、攻撃時間、User-Agent、Cookie などのパラメーターをカスタマイズすることもできます。

## ⚠️ 警告 ⚠️

*   **法的責任:** このツールを使用してアクセス権のないシステムを攻撃することは**違法**であり、深刻な法的結果を招く可能性があります。 このツールは、テストする権限があるシステムでのみ使用してください。
*   **システムへの影響:** DoS 攻撃は、オンライン サービスを中断またはシャットダウンする可能性があります。 攻撃を実行する前に、慎重に検討してください。
*   **教育目的:** このツールは、教育およびセキュリティ研究を目的として設計されています。 著者は、誤用について責任を負いません。

## 主な機能

*   **マルチスレッド:** 複数のスレッドで同時に攻撃し、攻撃効果を高めます。
*   **高度なカスタマイズ性:** 次のような多くのパラメーターをカスタマイズできます。
    *   スレッド数。
    *   攻撃時間。
    *   User-Agent (ファイルから、または手動で)。
    *   Cookie。
    *   カスタム ヘッダー (Slowloris および R.U.D.Y 用)。
    * 更新頻度
*   **複数の攻撃方法をサポート:** GET、POST、PUT、DELETE、Slowloris、R.U.D.Y、および検索エンジンの攻撃。
*   **直感的なインターフェース:** `rich` ライブラリを使用して、攻撃ステータス情報を美しく、わかりやすく表示します。
*   **ログ:** 攻撃のログをファイルに記録します (オプション)。
* **User-Agent、リクエストヘッダーを自動生成します** (選択した場合)。

## インストール

1.  **Python のインストール:** Python 3.7 以降がインストールされていることを確認してください。
2.  **リポジトリのクローン (またはダウンロード):**
    ```bash
    git clone https://github.com/Rin1809/Dos_Tool.git
    cd Dos-Tool
    ```
3.  **(オプション) 仮想環境を作成してアクティブ化する:** ライブラリの競合を避けるために、これをお勧めします。
     ```bash
     python -m venv venv
     ```

      * Windowsの場合:
         ```
         venv\Scripts\activate
         ```

     * Linux/macOS の場合:
         ```
         source venv/bin/activate
         ```
4.  **必要なライブラリをインストールします:** `requirements.txt`はフォルダーに含まれています。
   * `requirements.txt` がない場合は、手動で作成します (次のライブラリをリストします)。
    ```
    requests
    aiohttp
    rich
    ```
    ```bash
    pip install -r requirements.txt
    ```

## 使用方法

1.  **`run.bat` ファイルを実行します:** このファイルは、仮想環境を自動的にチェックしてインストールし (存在しない場合)、必要なライブラリをインストールしてから、ツールを実行します。

2.  **パラメーターを入力します:** ツールは、次の情報を入力するように求めます。
    *   **攻撃モード:** 次のいずれかのモードを選択します。
        *   **1:** 単純な GET 攻撃 (デフォルト)。
        *   **2:** カスタム攻撃 (複数の HTTP メソッドを選択できます)。
        *   **3:** Slowloris 攻撃。
        *   **4:** R.U.D.Y 攻撃。
        * **5:** 検索エンジンの攻撃。
    *   **ターゲット URL:**
        *   **ファイルから:** URL のリスト (1 行に 1 つの URL) を含むファイルの名前を入力します。 例: `urls.txt`.
        *   **手動:** URL を直接入力します。例: `https://example.com`.
        * 検索エンジンの場合は、次のようなURLを使用します: `https://yurineko.my/search?query=` (手動で)、指示に従います。
    *   **スレッド数:** 同時接続数 (例: 100)。
    *   **更新頻度:** ステータス情報を更新する時間 (例: 0.5 秒)。
    *   **攻撃時間:** 攻撃時間 (秒)。 永続的な攻撃の場合は `0` を入力します (推奨しません)。
    *   **HTTP メソッド オプション (カスタム モードが選択されている場合):** 攻撃メソッドをコンマで区切って入力します。例: `GET, POST, PUT`.  または、すべてを選択するには `ALL` と入力します。
    *   **Cookie オプション:** Cookie を追加する場合は、`y` を入力して Cookie 値を入力します。 それ以外の場合は、`n` を入力します。
    *   **User-Agent オプション:**
        *   **ファイルから:** User-Agent リスト (1 行に 1 つの User-Agent) を含むファイルの名前を入力します。例: `user_agents.txt`.
        *   **手動:** User-Agent を直接入力します。
    * **(SLOWLORIS のみ):** ポート `80` (HTTP)、`443` (HTTPS)、または両方 (`3`) を選択します。
    *   **(SLOWLORIS および R.U.D.Y のみ):** ヘッダーを`自動的`に生成するか、`手動`で生成するかを選択します。
    *   **ログを保存:** ログを保存する場合は、`y` を入力します。 それ以外の場合は、`n` を入力します。

3.  **進行状況の監視:** ツールは、攻撃ステータス テーブルを表示します。これには次の情報が含まれます。
    *   スレッドの総数。
    *   リクエストの総数。
    *   成功したリクエストの数。
    *   失敗したリクエストの数。
    *   経過時間。
    *   各 URL の詳細な進行状況 (完了 / 合計、パーセンテージ、速度)。
    *   最近のアクティビティのログ (最後のアクティビティ 10 件)。

4.  **攻撃を停止:** `Ctrl + C` を押して攻撃を停止します。

## 詳細な例

**例 1: 単一の URL に対する単純な GET 攻撃**

1.  `run.bat` を実行します。
2.  攻撃モードを選択します: `1` (GET)。
3.  URL の入力方法を選択します: `2` (手動)。
4.  URL を入力します: `https://example.com`.
5.  スレッド数を入力します: `50`.
6.  更新頻度を入力します: `0.5`.
7.  攻撃時間を入力します: `60` (60 秒間攻撃)。
8.  Cookie を追加しますか?: `n`.
9.  User-Agent を選択します: `2` (手動)。
10. User-Agent を入力します: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36`.
11. ログを保存しますか?: `y`.

**例 2: ファイルから複数の URL に対して複数の HTTP メソッドを使用したカスタム攻撃**

1.  次の内容の `urls.txt` ファイルを作成します (1 行に 1 つの URL)。

    ```
    https://example.com
    https://example.net
    https://example.org
    ```

2.  `run.bat` を実行します。
3.  攻撃モードを選択します: `2` (カスタム)。
4.  URL の入力方法を選択します: `1` (ファイルから)。
5.  ファイル名を入力します: `urls.txt`.
6.  スレッド数を入力します: `100`.
7.  更新頻度を入力します: `1`.
8.  攻撃時間を入力します: `0` (永続的な攻撃 - *推奨しません*、注意してください!)。
9.  HTTP メソッドを選択します: `GET, POST`.
10. Cookie を追加しますか?: `y`.
11. Cookie 値を入力します: `sessionid=abcdef123456; csrftoken=xyz789`.
12. User-Agent を選択します: `1` (ファイルから)。
13. User-Agent ファイルの名前を入力します: `user_agents.txt` (このファイルを作成する必要があります。1 行に 1 つの User-Agent)。
14. ログを保存しますか?: `n`.

**例 3: Slowloris 攻撃**

1.  `run.bat` を実行する
2.  攻撃モードを選択: `3` (Slowloris)
3.  URL の入力方法: `2` (手動)
4.  URLを入力: `http://example.com`
5. スレッド数を入力: `200`
6. 更新頻度を入力: `0.5`
7.  攻撃時間入力: `30`
8.  Cookie を追加: `n`
9.  ヘッダーの取得方法を選択: `1` (自動)。
10. 攻撃ポートを選択: `3` (80 と 443 の両方)。
11. ログを保存しますか: `n`

**例 4: R.U.D.Y. 攻撃**

これも同様ですが：
   * モード`4`を選択してください
   * ヘッダーを`自動的に`取得することをお勧めします。

**例 5: 検索エンジンの攻撃**

1. `run.bat` を実行する。
2.  攻撃モードを選択: `5` (検索)。
3.  URL の入力方法: `2` (手動)。
4.  URLを入力: `https://example.com/search?q=`.
5. キーワードを入力するには、`y` を選択します。
6. 入力: `dos,attack,python`.
7. その他の情報 (スレッド、時間など) を入力します。

**Slowloris と R.U.D.Y. に関する重要な注意事項:**

*   これらの 2 つの攻撃方法は、(SYN Flood のようなネットワーク層 (レイヤー 3/4) ではなく) アプリケーション層 (レイヤー 7) の脆弱性を悪用します。
*   これらは、帯域幅を過負荷にするのではなく、接続を切断した状態で Web サーバーを「ビジー」状態にすることで機能します。
*   パラメーター (スレッド数、タイムアウトなど) は、各ターゲットに合わせて調整する必要があります。

</details>
