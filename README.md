# 使用CNN進行植物病害辨識 (準確率約95%)

## 專案簡介
本專案利用卷積神經網絡（CNN）建立一個植物病害辨識。透過對大量植物圖像資料的訓練，模型能夠自動辨識多種植物疾病，達到約 95% 的準確率。該系統旨在協助農業工作者及研究人員在早期發現植物病害，從而及時採取防治措施。

## 功能特色
- **自動疾病辨識**：通過 CNN 模型，自動分析並辨識輸入圖像中的植物疾病種類。
- **高準確率**：模型在測試集上達到約 95% 的準確率，提供可靠的預測結果。
- **直觀的數據展示**：訓練過程中的準確率、損失值變化等數據以圖表形式展示，便於用戶了解模型表現。
- **彈性擴展**：使用者可根據需求調整模型參數，或利用新資料進行再訓練。

## 系統需求
- **作業系統**：Windows / macOS / Linux
- **Python 版本**：3.6 以上
- **必要套件**：
  - TensorFlow 或 Keras
  - NumPy
  - Pandas
  - Matplotlib
  - Scikit-learn
  - Jupyter Notebook（若使用 Notebook 介面）
  
建議使用虛擬環境 (如 conda 或 venv) 來配置專案環境。

## 資料集說明
![image](https://github.com/user-attachments/assets/19a9d274-b933-41bf-bcff-0802cbfe80fb)
- **資料來源**：本專案使用的資料集包含各類植物的圖像，每張圖像皆標註相應的疾病種類。請依據實際應用情境更新資料來源（Kaggle）。
- **資料結構**：資料集應依照以下結構進行組織：
  - 根目錄
    - `train/`：訓練資料
    - `validation/`：驗證資料
    - `test/`：測試資料

## 使用方法

### 1. 環境配置
- 建立並啟動虛擬環境（例如使用 conda）：
  ```bash
  conda create -n plant-disease python=3.8
  conda activate plant-disease
  ```
- 安裝所需套件：
  ```bash
  pip install -r requirements.txt
  ```

### 2. 資料準備
- 下載並解壓縮資料集，確保資料集的資料夾結構與上述說明一致。
- 若有需要，可在 Notebook 中修改資料路徑參數，以匹配本地資料夾結構。

### 3. 模型訓練
- 開啟 Kaggle
- 依序執行 Notebook 中的各個程式區塊，進行資料預處理、模型建立、訓練及驗證。
- 根據資料集大小與硬體性能，適當調整 batch size 與 epochs 參數。

### 4. 模型測試與評估
![image](https://github.com/user-attachments/assets/ef90bc61-f02d-458f-ae1a-70ef7e1347e2)
- 完成模型訓練後，利用測試資料集對模型進行效能評估。

![image](https://github.com/user-attachments/assets/e1d005ac-2d23-4332-a10c-35456d7c30b1)
- 系統將生成訓練過程中準確率與損失值的圖表，以及測試結果的混淆矩陣，方便用戶直觀了解模型表現。

## 模型效能
![image](https://github.com/user-attachments/assets/8cb0317a-753e-4142-a594-2b145f993658)
- 本專案中建立的 CNN 模型在測試集上的準確率約為 95%。
- 詳細的模型架構、訓練參數及超參數設定可參考 Notebook 內部說明。

## 實驗環境
- **開發語言**：Python
- **開發工具**：Kaggle
- **硬體需求**：建議使用支援 GPU 加速的設備（例如 NVIDIA GPU）以加快模型訓練速度

## 如何貢獻
- 若您對本專案有改進建議或發現問題，歡迎提交 issue 或 pull request。

## 授權條款
- 本專案採用 MIT 授權協議，詳細內容請參考 [LICENSE](LICENSE) 文件。

## 聯絡資訊
- **專案維護者**：Andrew Chen

## 注意事項
- 模型訓練時間與資源需求會根據資料集大小與硬體配置有所不同，請合理調整訓練參數。
- 此專案主要供學術研究及學習參考使用，若用於商業應用，請確認相關授權與版權規定。
