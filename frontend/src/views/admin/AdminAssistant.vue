<template>
  <div class="admin-assistant">
    <!-- 状态指示器 -->
    <header>
      <div class="status-indicator" :class="{ online: isOnline, offline: !isOnline }">
        <span class="dot"></span>
        {{ isOnline ? '管理助手在线' : '离线模式' }}
      </div>
    </header>

    <!-- 快捷操作 -->
    <div class="quick-actions">
      <el-button
        v-for="action in quickActions"
        :key="action.id"
        type="primary"
        size="small"
        @click="triggerAssistantAction(action.command)"
        :icon="action.icon"
        round
      >{{ action.label }}</el-button>
    </div>

    <!-- 消息流 -->
    <div class="message-flow">
      <transition-group name="fade" tag="div">
        <div
          v-for="(msg, idx) in messages"
          :key="idx"
          :class="['message-bubble', msg.role]"
        >
          <template v-if="msg.type === 'text'">
            <span v-if="msg.role === 'user'">管理员：</span>
            <span v-else>助手：</span>
            <span v-html="msg.content"></span>
          </template>
          <template v-else-if="msg.type === 'error'">
            <span class="error-msg">⚠️ {{ msg.content }}</span>
          </template>
        </div>
        <div v-if="loading" key="loading" class="message-bubble assistant loading">
          <span class="dot-pulse"></span> 思考中...
        </div>
      </transition-group>
    </div>

    <!-- 输入区 -->
    <div class="input-controller">
      <el-input
        v-model="input"
        placeholder="请输入您的问题..."
        @keyup.enter="sendMessage"
        :disabled="loading"
        clearable
      />
      <el-button
        type="primary"
        :disabled="loading || !input.trim()"
        @click="sendMessage"
        icon="el-icon-s-promotion"
      >发送</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { chatWithDeepSeek } from '@/api/chat'
import { Message, DataAnalysis, User, Money } from '@element-plus/icons-vue'

const isOnline = ref(true)
const input = ref('')
const loading = ref(false)
const messages = ref([
  {
    role: 'assistant',
    type: 'text',
    content: `您好！我是管理助手，可以帮您：<br>
      1. 查询停车场每日收入 💰<br>
      2. 查看停车场使用情况 📊<br>
      3. 分析用户信息和行为 👥<br>
      4. 生成管理报表和统计 📈<br>
      请问需要什么帮助？`
  }
])

const quickActions = [
  { id: 1, icon: Money, label: '今日收入', command: '查询今日停车场收入情况' },
  { id: 2, icon: DataAnalysis, label: '使用统计', command: '显示停车场使用率统计' },
  { id: 3, icon: User, label: '用户分析', command: '分析用户信息和活跃度' },
  { id: 4, icon: Message, label: '生成报表', command: '生成今日管理报表' }
]

function triggerAssistantAction(command) {
  input.value = command
  sendMessage()
}

async function sendMessage() {
  if (!input.value.trim()) return
  messages.value.push({ role: 'user', type: 'text', content: input.value })
  loading.value = true
  try {
    const reply = await chatWithDeepSeek(messages.value.map(m => ({
      role: m.role,
      content: m.content
    })), 'admin')
    messages.value.push({ role: 'assistant', type: 'text', content: reply })
    isOnline.value = true
  } catch (e) {
    messages.value.push({ role: 'assistant', type: 'error', content: '对话出错，请稍后再试。' })
    isOnline.value = false
  }
  input.value = ''
  loading.value = false
}
</script>

<style scoped>
.admin-assistant {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 80px);
  height: 100%;
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  background: #f5f7fa;
  border-radius: 16px;
  box-shadow: 0 2px 12px #0001;
  padding: 24px 24px 12px 24px;
  box-sizing: border-box;
}

header {
  margin-bottom: 12px;
}

.status-indicator {
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 15px;
  margin-bottom: 8px;
}

.status-indicator .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 8px;
  background: #43a047;
  animation: pulse 1.2s infinite;
}

.status-indicator.offline .dot {
  background: #e53935;
  animation: none;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 #43a04755; }
  70% { box-shadow: 0 0 0 8px #43a04700; }
  100% { box-shadow: 0 0 0 0 #43a04700; }
}

.quick-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.message-flow {
  flex: 1 1 0;
  min-height: 220px;
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 1px 4px #0001;
  max-height: 60vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.message-bubble {
  margin-bottom: 10px;
  padding: 8px 14px;
  border-radius: 16px;
  max-width: 90%;
  word-break: break-all;
  line-height: 1.7;
  transition: all 0.2s;
}

.message-bubble.user {
  background: #e3f2fd;
  color: #1976d2;
  align-self: flex-end;
  margin-left: auto;
  text-align: right;
}

.message-bubble.assistant {
  background: #fff;
  color: #333;
  align-self: flex-start;
  margin-right: auto;
  box-shadow: 0 1px 4px #0001;
}

.message-bubble.error-msg {
  color: #e53935;
  font-weight: bold;
}

.input-controller {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 8px;
  width: 100%;
}

.loading .dot-pulse {
  display: inline-block;
  width: 24px;
  height: 8px;
  position: relative;
}

.loading .dot-pulse:before, .loading .dot-pulse:after {
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  background: #43a047;
  border-radius: 50%;
  position: absolute;
  animation: dotPulse 1s infinite alternate;
}

.loading .dot-pulse:after {
  left: 12px;
  animation-delay: 0.5s;
}

@keyframes dotPulse {
  0% { opacity: 0.3; }
  100% { opacity: 1; }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 900px) {
  .admin-assistant {
    max-width: 100vw;
    padding: 8px 2vw 8px 2vw;
    border-radius: 0;
    box-shadow: none;
  }
  .message-flow {
    max-height: 50vh;
    padding: 8px;
  }
}

@media (max-width: 600px) {
  .admin-assistant {
    min-height: 100vh;
    padding: 0;
  }
  .quick-actions {
    gap: 6px;
    margin-bottom: 8px;
  }
  .input-controller {
    flex-direction: column;
    gap: 6px;
  }
  .message-bubble {
    font-size: 15px;
    padding: 6px 8px;
  }
}
</style> 