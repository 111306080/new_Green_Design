from flask import Flask, request, jsonify
from google.cloud import firestore
import os

# 設置 Google Cloud 認證環境變量
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-file.json"

app = Flask(__name__)
db = firestore.Client()

# 創建新設計
@app.route('/api/designs', methods=['POST'])
def create_design():
    design_info = request.json
    
    # 將設計信息添加到 Firestore 中
    designs_ref = db.collection('designs')
    new_design_ref = designs_ref.add(design_info)  # 添加設計信息

    # 自動抓取 Firestore 中的所有設計
    all_designs = []
    all_designs_stream = designs_ref.stream()  # 獲取所有設計
    for design in all_designs_stream:
        design_data = design.to_dict()
        all_designs.append({
            'id': design.id,  # 獲取設計的 ID
            'pic': design_data.get('pic', ''),  # 獲取 pic，默認為空字符串
            'score': design_data.get('score', 1),  # 獲取 score，默認為 1
            'description': design_data.get('description', '')  # 獲取 description，默認為空字符串
        })

    # 返回創建的設計的 ID 和所有設計
    return jsonify({
        'id': new_design_ref.id,  # 同一個設計下的單一 ID
        'all_designs': all_designs  # 所有設計
    }), 201

if __name__ == '__main__':
    app.run(debug=True)
