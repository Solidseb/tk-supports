const url = 'pdf.pdf';  // PDFファイルのパスを指定
const container = document.getElementById('pdf-container');
const scale = 1.5;
const mosaicSize = 20; // モザイクのサイズ（ピクセル）
let pdfDoc = null;

// PDFをロードして処理を開始する
pdfjsLib.getDocument(url).promise.then((pdfDoc_) => {
    pdfDoc = pdfDoc_;
    const totalPages = pdfDoc.numPages;
    for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
        renderPage(pageNum);
    }
});

// 各ページをレンダリングする関数
function renderPage(num) {
    pdfDoc.getPage(num).then((page) => {
        const viewport = page.getViewport({ scale: scale });
        const canvas = document.createElement('canvas');
        canvas.className = 'pdf-page';
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        container.appendChild(canvas);
        const context = canvas.getContext('2d');

        // PDF.jsでページを描画
        const renderContext = {
            canvasContext: context,
            viewport: viewport
        };
        const renderTask = page.render(renderContext);

        renderTask.promise.then(() => {
            // 特定の条件（例えば5ページ以降）でモザイクをかける
            if (num >= 5) {
                applyMosaic(context);
            }
        });
    });
}

// ページにモザイクをかける関数
function applyMosaic(context) {
    const imageData = context.getImageData(0, 0, context.canvas.width, context.canvas.height);
    const data = imageData.data;

    const blockSize = mosaicSize;

    for (let y = 0; y < context.canvas.height; y += blockSize) {
        for (let x = 0; x < context.canvas.width; x += blockSize) {
            let totalRed = 0, totalGreen = 0, totalBlue = 0;
            let count = 0;

            // ブロック内の平均色を計算
            for (let blockY = y; blockY < Math.min(y + blockSize, context.canvas.height); blockY++) {
                for (let blockX = x; blockX < Math.min(x + blockSize, context.canvas.width); blockX++) {
                    const pixelIndex = (blockY * context.canvas.width + blockX) * 4;
                    totalRed += data[pixelIndex];
                    totalGreen += data[pixelIndex + 1];
                    totalBlue += data[pixelIndex + 2];
                    count++;
                }
            }

            const averageRed = totalRed / count;
            const averageGreen = totalGreen / count;
            const averageBlue = totalBlue / count;

            // ブロック内のピクセルを平均色で埋める
            for (let blockY = y; blockY < Math.min(y + blockSize, context.canvas.height); blockY++) {
                for (let blockX = x; blockX < Math.min(x + blockSize, context.canvas.width); blockX++) {
                    const pixelIndex = (blockY * context.canvas.width + blockX) * 4;
                    data[pixelIndex] = averageRed;
                    data[pixelIndex + 1] = averageGreen;
                    data[pixelIndex + 2] = averageBlue;
                }
            }
        }
    }

    context.putImageData(imageData, 0, 0);
}
