from flask import Blueprint, request, jsonify
import requests

chat_bp = Blueprint('chat', __name__)

# 腾讯混元大模型API配置
HUNYUAN_API_URL = "https://api.hunyuan.cloud.tencent.com/v1/chat/completions"
HUNYUAN_API_KEY = "sk-JNJEQDVpv205ZyecxSrySIHQqEov51R7SeB9g9jweE55aikC"

@chat_bp.route('/api/chat', methods=['POST'])
def chat_with_hunyuan():
    data = request.get_json()
    messages = data.get("messages", [])
    user_type = data.get("userType", "user")  # 获取用户类型
    if not messages:
        return jsonify({"success": False, "message": "消息不能为空"}), 400

    # 根据用户类型设置不同的系统提示词
    if user_type == "admin":
        system_prompt = """你是智慧园区停车场管理助手，专门为管理员提供服务。你可以：
1. 查询停车场每日收入、月收入、年收入等财务数据
2. 分析停车场使用率、车位占用情况等运营数据
3. 查看用户信息、用户活跃度、用户行为分析
4. 生成管理报表、统计图表、趋势分析
5. 提供管理建议、优化方案、运营策略
6. 回答停车场管理相关的专业问题

请用专业、准确的语言回答管理员的问题，并提供有价值的管理洞察。"""
    else:
        system_prompt = "你是智慧园区停车场助手，可以解答停车场相关问题、查询车位、预约车位。"

    payload = {
        "model": "hunyuan-turbos-latest",
        "messages": [
            {"role": "system", "content": system_prompt},
            *messages
        ],
        "enable_enhancement": True
    }
    headers = {
        "Authorization": f"Bearer {HUNYUAN_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        resp = requests.post(HUNYUAN_API_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        print('腾讯混元API返回:', resp.text)
        result = resp.json()
        # 腾讯混元返回格式可能不同，需根据实际API文档调整
        reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        return jsonify({"success": True, "reply": reply})
    except Exception as e:
        import traceback
        print('API异常:', e)
        traceback.print_exc()
        return jsonify({"success": False, "message": "对话服务异常", "error": str(e)}), 500 