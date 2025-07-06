document.addEventListener('DOMContentLoaded', () => {
    const player = document.querySelector('.player');
    const monster = document.querySelector('.monster'); // Nếu muốn tương tác với quái vật
    const moveLeftBtn = document.querySelector('.move-left');
    const moveRightBtn = document.querySelector('.move-right');
    const jumpBtn = document.querySelector('.jump-button');
    const attackBtn = document.querySelector('.attack-button');

    let playerPosition = 100; // Vị trí ban đầu của người chơi từ trái (khớp với CSS)
    let playerSpeed = 5; // Tốc độ di chuyển (pixels)
    let isJumping = false; // Trạng thái nhảy

    // Hàm di chuyển nhân vật
    function movePlayer(direction) {
        if (direction === 'left') {
            playerPosition -= playerSpeed;
        } else if (direction === 'right') {
            playerPosition += playerSpeed;
        }
        // Giới hạn vị trí người chơi trong khung game
        // 960 = game-container width, 70 = player width
        playerPosition = Math.max(0, Math.min(playerPosition, 960 - 70));
        player.style.left = playerPosition + 'px';
    }

    // Hàm nhảy cơ bản (rất đơn giản, không mô phỏng trọng lực thực tế)
    function playerJump() {
        if (isJumping) return; // Không nhảy nếu đang nhảy
        isJumping = true;
        player.style.transition = 'bottom 0.3s ease-out'; // Hiệu ứng nhảy lên
        player.style.bottom = '200px'; // Nhảy lên cao hơn

        setTimeout(() => {
            player.style.transition = 'bottom 0.3s ease-in'; // Hiệu ứng rơi xuống
            player.style.bottom = '80px'; // Rơi về vị trí mặt đất (khớp với CSS)
            setTimeout(() => {
                isJumping = false;
                player.style.transition = 'none'; // Xóa transition sau khi hạ cánh để di chuyển không bị chậm
            }, 300);
        }, 300);
    }

    // Hàm tấn công cơ bản (chỉ phản hồi hình ảnh)
    function playerAttack() {
        console.log('Player attacks!');
        // Thêm một class tạm thời cho hiệu ứng tấn công
        player.classList.add('attacking');
        setTimeout(() => {
            player.classList.remove('attacking');
        }, 300); // Xóa class sau 300ms
    }

    // Gán sự kiện cho các nút điều khiển ảo
    moveLeftBtn.addEventListener('click', () => movePlayer('left'));
    moveRightBtn.addEventListener('click', () => movePlayer('right'));
    jumpBtn.addEventListener('click', playerJump);
    attackBtn.addEventListener('click', playerAttack);

    // Tùy chọn: Điều khiển bằng bàn phím cho máy tính để bàn
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            movePlayer('left');
        } else if (e.key === 'ArrowRight') {
            movePlayer('right');
        } else if (e.key === 'ArrowUp' || e.key === ' ') { // Mũi tên lên hoặc phím cách để nhảy
            playerJump();
        } else if (e.key === 'x' || e.key === 'X') { // Phím 'x' để tấn công
            playerAttack();
        }
    });

    // Thiết lập vị trí ban đầu của người chơi khi tải trang
    player.style.left = playerPosition + 'px';
});