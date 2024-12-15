<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>사다리 타기</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .input-section {
            margin: 20px;
        }
        .ladder-section {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .ladder-column {
            margin: 0 10px;
        }
        .ladder-result {
            margin-top: 20px;
            display: none;
            background: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>사다리 타기</h1>
    <div class="input-section">
        <input type="text" id="item-input" placeholder="항목을 입력하세요">
        <button onclick="addItem()">추가</button>
    </div>
    <div id="item-list"></div>
    <button onclick="generateLadder()">사다리 생성</button>
    <div id="ladder" class="ladder-section"></div>
    <div id="results" class="ladder-result"></div>

    <script>
        let items = [];
        let results = [];

        function addItem() {
            const input = document.getElementById('item-input');
            const value = input.value.trim();
            if (value) {
                items.push(value);
                document.getElementById('item-list').innerText = `항목: ${items.join(", ")}`;
                input.value = '';
            }
        }

        function generateLadder() {
            const ladder = document.getElementById('ladder');
            ladder.innerHTML = '';
            results = items.map(() => `결과 ${Math.ceil(Math.random() * 10)}`); // 임시 결과
            items.forEach((item, index) => {
                const column = document.createElement('div');
                column.className = 'ladder-column';
                column.innerHTML = `<button onclick="showResult(${index})">${item}</button>`;
                ladder.appendChild(column);
            });
        }

        function showResult(index) {
            const resultDiv = document.getElementById('results');
            resultDiv.style.display = 'block';
            resultDiv.innerText = `${items[index]}의 결과는: ${results[index]}`;
        }
    </script>
</body>
</html>
