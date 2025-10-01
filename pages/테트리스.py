import streamlit as st

st.set_page_config(page_title="블록 낙하 게임", layout="wide", page_icon="🎮")

st.title("🎮 블록 낙하 게임 (Tetr.io 스타일)")

game_html = r"""





"""

# Streamlit에서 렌더링
st.components.v1.html(game_html, height=900, scrolling=True)





import streamlit as st

st.set_page_config(page_title="블록 낙하 게임", layout="wide", page_icon="🎮")

st.title("🎮 블록 낙하 게임 (Tetr.io 스타일)")

game_html = r"""
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tetris-스타일 블록 게임</title>
    <!-- Tailwind CSS CDN 로드 -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* 커스텀 CSS (게임 영역) */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #1a202c; /* 다크 모드 배경 */
            color: #e2e8f0;
        }
        #game-board {
            border: 4px solid #4a5568;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            background-color: #0d1117; /* 어두운 게임 배경 */
            margin-bottom: 20px;
        }
        .info-panel {
            background-color: #2d3748;
            padding: 1rem;
            border-radius: 0.75rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        /* 버튼 스타일링 */
        button {
            transition: all 0.15s ease-in-out;
        }
        button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        button:active {
            transform: translateY(0);
            box-shadow: none;
        }

        /* 모바일 환경을 위한 조정 */
        @media (max-width: 768px) {
            .game-container {
                flex-direction: column;
                align-items: center;
            }
            #game-board {
                width: 90vw; /* 뷰포트 너비의 90% */
                max-width: 300px; /* 최대 크기 제한 */
                height: auto;
            }
        }
    </style>
</head>
<body class="p-4 flex flex-col items-center justify-center min-h-screen">

    <h1 class="text-4xl font-extrabold mb-8 text-indigo-400">블록 낙하 게임 (Tetr.io 스타일)</h1>

    <div class="game-container flex flex-col md:flex-row gap-8 items-start">
        
        <!-- 게임 보드 -->
        <canvas id="game-board"></canvas>

        <!-- 정보 및 조작 패널 -->
        <div class="info-panel w-full md:w-64 space-y-4">
            
            <div id="status-display" class="text-center font-bold text-lg h-6">게임을 시작하세요!</div>
            
            <div class="flex flex-col space-y-2">
                <div class="flex justify-between p-2 bg-gray-700 rounded-lg">
                    <span class="font-semibold text-gray-300">점수:</span>
                    <span id="score" class="font-mono text-xl text-yellow-400">0</span>
                </div>
                <div class="flex justify-between p-2 bg-gray-700 rounded-lg">
                    <span class="font-semibold text-gray-300">레벨:</span>
                    <span id="level" class="font-mono text-xl text-green-400">1</span>
                </div>
            </div>

            <!-- 다음 블록 표시 -->
            <div>
                <h2 class="text-xl font-bold mb-2 text-center text-indigo-300">다음 블록</h2>
                <canvas id="next-piece-canvas" class="bg-gray-800 rounded-lg mx-auto" width="120" height="80"></canvas>
            </div>

            <!-- 컨트롤 버튼 (모바일용 및 시작/일시정지) -->
            <div class="flex space-x-2">
                <button id="startButton" class="w-1/2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg shadow-md">
                    시작
                </button>
                <button id="pauseButton" class="w-1/2 px-4 py-2 bg-yellow-600 hover:bg-yellow-700 text-white font-bold rounded-lg shadow-md" disabled>
                    일시정지
                </button>
            </div>
            
            <!-- 조작 안내 -->
            <div class="p-3 bg-gray-800 rounded-lg">
                <h3 class="text-lg font-semibold mb-2 text-indigo-400">조작법</h3>
                <ul class="text-sm space-y-1">
                    <li><kbd class="bg-gray-600 p-1 rounded">←</kbd> / <kbd class="bg-gray-600 p-1 rounded">→</kbd>: 좌우 이동</li>
                    <li><kbd class="bg-gray-600 p-1 rounded">↓</kbd>: 소프트 드롭 (빨리 내리기)</li>
                    <li><kbd class="bg-gray-600 p-1 rounded">↑</kbd> / <kbd class="bg-gray-600 p-1 rounded">Z</kbd>: 회전 (시계방향 / 반시계방향)</li>
                    <li><kbd class="bg-gray-600 p-1 rounded">Space</kbd>: 하드 드롭 (즉시 내리기)</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- JavaScript 게임 로직 -->
    <script>
        const canvas = document.getElementById('game-board');
        const ctx = canvas.getContext('2d');
        const nextCanvas = document.getElementById('next-piece-canvas');
        const nextCtx = nextCanvas.getContext('2d');
        const scoreElement = document.getElementById('score');
        const levelElement = document.getElementById('level');
        const statusDisplay = document.getElementById('status-display');
        const startButton = document.getElementById('startButton');
        const pauseButton = document.getElementById('pauseButton');

        // 게임 설정
        const GRID_WIDTH = 10;
        const GRID_HEIGHT = 20;
        const BLOCK_SIZE = 30; // 30px
        const NEXT_BLOCK_SIZE = 20; // 다음 블록 크기

        canvas.width = GRID_WIDTH * BLOCK_SIZE;
        canvas.height = GRID_HEIGHT * BLOCK_SIZE;

        // Tetrominoes (모양 및 색상)
        const TETROMINOES = {
            'I': { shape: [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]], color: '#4dc2f5' }, // Cyan
            'J': { shape: [[1, 0, 0], [1, 1, 1], [0, 0, 0]], color: '#3873ec' }, // Blue
            'L': { shape: [[0, 0, 1], [1, 1, 1], [0, 0, 0]], color: '#ff9600' }, // Orange
            'O': { shape: [[1, 1], [1, 1]], color: '#f5ee4d' }, // Yellow
            'S': { shape: [[0, 1, 1], [1, 1, 0], [0, 0, 0]], color: '#7cf54d' }, // Green
            'Z': { shape: [[1, 1, 0], [0, 1, 1], [0, 0, 0]], color: '#ff4d4d' }, // Red
            'T': { shape: [[0, 1, 0], [1, 1, 1], [0, 0, 0]], color: '#b94df5' }  // Purple
        };
        const PIECES = Object.keys(TETROMINOES);

        // 게임 상태 변수
        let board;
        let currentPiece;
        let nextPiece;
        let score;
        let level;
        let dropInterval;
        let dropCounter;
        let lastTime;
        let isPaused;
        let isGameOver;

        // --- 유틸리티 함수 ---

        /**
         * 2D 배열을 생성하고 0으로 초기화합니다.
         */
        function createBoard(w, h) {
            const arr = [];
            while (h--) {
                arr.push(new Array(w).fill(0));
            }
            return arr;
        }

        /**
         * 지정된 위치와 색상으로 하나의 블록을 그립니다.
         */
        function drawBlock(context, x, y, color, size = BLOCK_SIZE) {
            context.fillStyle = color;
            context.fillRect(x * size, y * size, size, size);
            
            // 블록 테두리 (입체감 추가)
            context.strokeStyle = '#000';
            context.lineWidth = 1;
            context.strokeRect(x * size, y * size, size, size);
        }

        /**
         * 보드 전체를 그립니다.
         */
        function drawBoard() {
            // 배경 지우기
            ctx.fillStyle = '#0d1117';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // ⚠️ 수정: 'board'가 정의되지 않았을 경우 그리기를 건너뜁니다.
            if (!board) return;

            // 보드에 고정된 블록 그리기
            for (let y = 0; y < GRID_HEIGHT; y++) {
                for (let x = 0; x < GRID_WIDTH; x++) {
                    if (board[y][x]) {
                        drawBlock(ctx, x, y, board[y][x]);
                    }
                }
            }
        }

        /**
         * 현재 조작 중인 블록을 그립니다.
         */
        function drawPiece(piece, context, xOffset = 0, yOffset = 0, size = BLOCK_SIZE) {
            if (!piece) return;

            piece.shape.forEach((row, y) => {
                row.forEach((value, x) => {
                    if (value) {
                        drawBlock(context, piece.pos.x + x + xOffset, piece.pos.y + y + yOffset, piece.color, size);
                    }
                });
            });
        }

        /**
         * 다음 블록 창을 그립니다.
         */
        function drawNextPiece() {
            // 배경 지우기
            nextCtx.fillStyle = '#2d3748';
            nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
            
            if (nextPiece) {
                // 다음 블록을 중앙에 가깝게 그립니다.
                const pieceWidth = nextPiece.shape[0].length;
                const pieceHeight = nextPiece.shape.length;
                
                // 캔버스 크기 (120x80). 중앙에 위치시키기 위한 오프셋 계산
                const xOffset = (nextCanvas.width / 2 / NEXT_BLOCK_SIZE) - (pieceWidth / 2);
                const yOffset = (nextCanvas.height / 2 / NEXT_BLOCK_SIZE) - (pieceHeight / 2);

                drawPiece(
                    { shape: nextPiece.shape, pos: { x: 0, y: 0 }, color: nextPiece.color },
                    nextCtx,
                    xOffset, 
                    yOffset,
                    NEXT_BLOCK_SIZE
                );
            }
        }

        /**
         * 새로운 블록을 스폰합니다.
         */
        function spawnPiece() {
            // 현재 블록이 없으면 다음 블록을 가져와서 사용
            if (!currentPiece) {
                const type = PIECES[Math.floor(Math.random() * PIECES.length)];
                const tetromino = TETROMINOES[type];
                currentPiece = {
                    shape: tetromino.shape,
                    color: tetromino.color,
                    pos: { x: Math.floor(GRID_WIDTH / 2) - Math.floor(tetromino.shape[0].length / 2), y: 0 },
                    type: type
                };
            } else {
                currentPiece = nextPiece;
            }

            // 새로운 다음 블록 생성
            const nextType = PIECES[Math.floor(Math.random() * PIECES.length)];
            const nextTetromino = TETROMINOES[nextType];
            nextPiece = {
                shape: nextTetromino.shape,
                color: nextTetromino.color,
                pos: { x: 0, y: 0 },
                type: nextType
            };

            drawNextPiece();

            // 스폰 위치에서 충돌 검사 (게임 오버 조건)
            if (!isValidMove(0, 0, currentPiece.shape)) {
                gameOver();
                return false;
            }
            return true;
        }
        
        /**
         * 현재 위치와 모양에서 유효성(충돌)을 검사합니다.
         */
        function isValidMove(offsetX, offsetY, shape) {
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const newX = currentPiece.pos.x + x + offsetX;
                        const newY = currentPiece.pos.y + y + offsetY;

                        // 1. 보드 경계를 벗어나는지 확인 (좌, 우, 하)
                        if (newX < 0 || newX >= GRID_WIDTH || newY >= GRID_HEIGHT) {
                            return false;
                        }
                        // 2. 보드 경계를 벗어나는지 확인 (상단은 무시, 블록이 튀어나갈 수 있으므로)
                        if (newY < 0) {
                            continue;
                        }

                        // 3. 이미 고정된 블록과 충돌하는지 확인
                        if (board[newY] && board[newY][newX]) {
                            return false;
                        }
                    }
                }
            }
            return true;
        }

        /**
         * 블록을 보드에 고정시킵니다.
         */
        function lockPiece() {
            currentPiece.shape.forEach((row, y) => {
                row.forEach((value, x) => {
                    if (value) {
                        const boardX = currentPiece.pos.x + x;
                        const boardY = currentPiece.pos.y + y;
                        if (boardY >= 0) {
                            board[boardY][boardX] = currentPiece.color;
                        }
                    }
                });
            });

            clearLines();
            spawnPiece();
        }

        /**
         * 회전 로직 (간단한 버전)
         */
        function rotateMatrix(matrix, dir) {
            // 행렬 전치 (Transpose)
            for (let y = 0; y < matrix.length; ++y) {
                for (let x = 0; x < y; ++x) {
                    [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]];
                }
            }

            // 행렬 뒤집기 (Reverse)
            if (dir > 0) { // 시계 방향 회전 (Reverse each row)
                matrix.forEach(row => row.reverse());
            } else { // 반시계 방향 회전 (Reverse each column)
                matrix.reverse();
            }

            return matrix;
        }

        /**
         * 블록을 회전시키고 충돌 시 위치 보정(Kick)을 시도합니다.
         */
        function rotatePiece(dir) {
            const originalShape = currentPiece.shape;
            const originalPos = { x: currentPiece.pos.x, y: currentPiece.pos.y };

            // 1. 회전 시도
            currentPiece.shape = rotateMatrix(currentPiece.shape, dir);

            // 2. 충돌 검사 및 킥 (간단한 킥 로직)
            let offset = 1;
            while (!isValidMove(0, 0, currentPiece.shape)) {
                currentPiece.pos.x += offset;
                offset = -(offset + (offset > 0 ? 1 : 0)); // 1, -2, 3, -4, ...
                
                // 너무 많이 킥을 시도하면 포기하고 원상 복구
                if (offset > currentPiece.shape.length) {
                    currentPiece.shape = originalShape; // 모양 복구
                    currentPiece.pos = originalPos; // 위치 복구
                    return;
                }
            }
        }

        /**
         * 라인을 지우고 점수를 업데이트합니다.
         */
        function clearLines() {
            let linesCleared = 0;

            outer: for (let y = GRID_HEIGHT - 1; y >= 0; --y) {
                for (let x = 0; x < GRID_WIDTH; ++x) {
                    if (board[y][x] === 0) {
                        continue outer; // 0이 하나라도 있으면 이 줄은 가득 차지 않음
                    }
                }
                
                // 이 줄(y)은 가득 찼음. 지우기
                const row = board.splice(y, 1)[0].fill(0);
                board.unshift(row); // 가장 위에 빈 줄 추가
                y++; // 줄이 아래로 이동했으므로 현재 줄을 다시 검사
                linesCleared++;
            }

            if (linesCleared > 0) {
                updateScore(linesCleared);
            }
        }

        /**
         * 점수와 레벨을 업데이트합니다.
         */
        function updateScore(linesCleared) {
            const baseScore = [0, 100, 300, 500, 800]; // 0, 1, 2, 3, 4줄 지웠을 때 점수
            
            // 점수 추가 (레벨을 곱하여 난이도 반영)
            score += baseScore[linesCleared] * level;
            scoreElement.textContent = score;

            // 10줄마다 레벨업 (간단한 레벨업 로직)
            if (score > level * 1000) {
                level++;
                levelElement.textContent = level;
                
                // 드롭 속도 증가
                dropInterval = 1000 - (level * 50);
                if (dropInterval < 100) dropInterval = 100; // 최소 속도 제한
            }
        }

        /**
         * 하드 드롭 (즉시 바닥에 떨구기)
         */
        function hardDrop() {
            while (isValidMove(0, 1, currentPiece.shape)) {
                currentPiece.pos.y++;
                score += 2; // 하드 드롭 점수
            }
            lockPiece();
        }

        /**
         * 블록을 이동시킵니다 (좌우, 소프트 드롭).
         */
        function movePiece(dir) {
            if (!isPaused && !isGameOver) {
                if (isValidMove(dir, 0, currentPiece.shape)) {
                    currentPiece.pos.x += dir;
                }
            }
        }

        /**
         * 소프트 드롭 (아래로 한 칸 이동)
         */
        function softDrop() {
            if (!isPaused && !isGameOver) {
                if (isValidMove(0, 1, currentPiece.shape)) {
                    currentPiece.pos.y++;
                    score += 1; // 소프트 드롭 점수
                    dropCounter = 0; // 즉시 드롭 카운터 초기화
                } else {
                    lockPiece();
                }
            }
        }

        /**
         * --- 게임 루프 및 컨트롤 ---
         */
        
        /**
         * 게임 루프 (중력, 업데이트)
         */
        function gameLoop(time = 0) {
            if (isPaused || isGameOver) {
                lastTime = time; // 일시정지/게임 오버 상태에서는 시간만 업데이트
                requestAnimationFrame(gameLoop);
                return;
            }

            const deltaTime = time - lastTime;
            lastTime = time;

            dropCounter += deltaTime;
            
            // 드롭 시간이 되면 블록을 한 칸 내립니다.
            if (dropCounter > dropInterval) {
                if (isValidMove(0, 1, currentPiece.shape)) {
                    currentPiece.pos.y++;
                } else {
                    lockPiece();
                }
                dropCounter = 0;
            }

            // 그리기
            drawBoard();
            drawPiece(currentPiece, ctx);

            requestAnimationFrame(gameLoop);
        }

        /**
         * 키보드 입력 처리
         */
        document.addEventListener('keydown', event => {
            if (isGameOver || isPaused || !currentPiece) return;

            switch (event.key) {
                case 'ArrowLeft':
                    movePiece(-1);
                    break;
                case 'ArrowRight':
                    movePiece(1);
                    break;
                case 'ArrowDown': // 소프트 드롭
                    softDrop();
                    break;
                case 'ArrowUp': // 시계 방향 회전
                    rotatePiece(1);
                    break;
                case 'z':
                case 'Z': // 반시계 방향 회전
                    rotatePiece(-1);
                    break;
                case ' ': // 스페이스바 (하드 드롭)
                    event.preventDefault(); // 페이지 스크롤 방지
                    hardDrop();
                    break;
            }
        });
        
        /**
         * 게임 일시정지/재개
         */
        function togglePause() {
            if (isGameOver) return;
            isPaused = !isPaused;
            if (isPaused) {
                statusDisplay.textContent = '일시정지';
                pauseButton.textContent = '재개';
            } else {
                statusDisplay.textContent = '게임 중...';
                pauseButton.textContent = '일시정지';
                // 재개 시 lastTime을 현재 시간으로 설정하여 deltaTime이 튀는 것을 방지
                lastTime = performance.now();
                requestAnimationFrame(gameLoop);
            }
        }

        /**
         * 게임 오버 처리
         */
        function gameOver() {
            isGameOver = true;
            statusDisplay.textContent = '게임 오버! 😭';
            cancelAnimationFrame(gameLoop); // 게임 루프 중지 (사실상 isGameOver 플래그로 처리됨)
            
            // 보드 전체를 회색으로 덮기
            ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 게임 오버 텍스트
            ctx.fillStyle = 'red';
            ctx.font = '48px Inter';
            ctx.textAlign = 'center';
            ctx.fillText('게임 오버', canvas.width / 2, canvas.height / 2 - 24);
            ctx.fillStyle = 'white';
            ctx.font = '24px Inter';
            ctx.fillText(`점수: ${score}`, canvas.width / 2, canvas.height / 2 + 24);

            startButton.textContent = '다시 시작';
            startButton.disabled = false;
            pauseButton.disabled = true;
        }

        /**
         * 게임 초기화
         */
        function initGame() {
            board = createBoard(GRID_WIDTH, GRID_HEIGHT);
            score = 0;
            level = 1;
            dropInterval = 1000; // 1초
            dropCounter = 0;
            lastTime = 0;
            isPaused = false;
            isGameOver = false;

            scoreElement.textContent = score;
            levelElement.textContent = level;
            statusDisplay.textContent = '게임 중...';
            
            // 시작 시 첫 번째 블록 스폰
            // nextPiece를 먼저 설정하고, spawnPiece()를 호출하여 nextPiece를 currentPiece로 가져오도록 합니다.
            const initialNextType = PIECES[Math.floor(Math.random() * PIECES.length)];
            const initialNextTetromino = TETROMINOES[initialNextType];
            nextPiece = {
                shape: initialNextTetromino.shape,
                color: initialNextTetromino.color,
                pos: { x: 0, y: 0 },
                type: initialNextType
            };
            
            spawnPiece(); // 첫 번째 블록 스폰 (다음 블록도 생성)
            drawBoard();
            
            // 게임 루프 시작
            cancelAnimationFrame(gameLoop);
            requestAnimationFrame(gameLoop);

            startButton.disabled = true;
            pauseButton.disabled = false;
            pauseButton.textContent = '일시정지';
        }

        // --- 이벤트 리스너 설정 ---

        startButton.addEventListener('click', initGame);
        pauseButton.addEventListener('click', togglePause);

        // 초기 화면 그리기
        drawBoard();
        statusDisplay.textContent = '시작 버튼을 누르세요';

    </script>
</body>
</html>

"""

# Streamlit에서 렌더링
st.components.v1.html(game_html, height=900, scrolling=True)