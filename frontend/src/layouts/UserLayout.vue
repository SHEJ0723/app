<template>
  <el-container class="user-layout">
    <el-aside width="200px" v-show="!isMobile" class="sidebar">
      <el-menu :default-active="$route.path" router class="user-menu">
        <el-menu-item index="/user/home">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/user/dashboard">
          <el-icon><Monitor /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/user/profile">
          <el-icon><User /></el-icon>
          <span>个人信息设置</span>
        </el-menu-item>
        <el-menu-item index="/user/chat">
          <el-icon><ChatDotRound /></el-icon>
          <span>在线助手</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header height="60px">
        <div class="header-content">
          <h2>智慧停车场管理系统</h2>
          <el-dropdown>
            <span class="user-info">
              {{ maskedPhone }} <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main-gradient-bg">
        <router-view></router-view>
      </el-main>
    </el-container>
    <BottomNavAdmin />
  </el-container>
</template>

<script>
import { Monitor, User, Location, List, ArrowDown, ChatDotRound, House } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import BottomNavAdmin from '@/components/BottomNavAdmin.vue'

export default {
  name: 'UserLayout',
  components: {
    Monitor,
    User,
    Location,
    List,
    ArrowDown,
    ChatDotRound,
    House,
    BottomNavAdmin
  },
  setup() {
    const router = useRouter()
    const phone = ref('')
    const isMobile = ref(window.innerWidth < 600)
    onMounted(() => {
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo'))
        if (userInfo && userInfo.phone) {
          phone.value = userInfo.phone
        }
      } catch (e) {}
      window.addEventListener('resize', () => {
        isMobile.value = window.innerWidth < 600
      })
    })
    const maskedPhone = computed(() => {
      if (!phone.value) return ''
      return phone.value.slice(0, 3) + '****' + phone.value.slice(-4)
    })
    const handleLogout = () => {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      localStorage.removeItem('userType')
      router.push('/login')
    }
    return {
      handleLogout,
      maskedPhone,
      isMobile
    }
  }
}
</script>

<style scoped>
.user-layout {
  height: 100vh;
  min-height: 100vh;
  display: flex;
  flex-direction: row;
  background: #f5f7fa;
}
.user-menu {
  height: 100%;
  border-right: none;
}
.el-header {
  background-color: white;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 20px;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.header-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.el-main {
  background-color: #f5f7fa;
  padding: 20px;
  flex: 1 1 0;
  min-width: 0;
  min-height: 0;
  overflow: auto;
  display: flex;
  flex-direction: column;
}
@media (max-width: 900px) {
  .user-layout {
    flex-direction: column;
  }
  .el-aside {
    width: 100vw !important;
    min-width: 0 !important;
    max-width: 100vw !important;
    border-right: none;
  }
  .el-main {
    padding: 8px;
  }
}
@media (max-width: 600px) {
  .user-layout {
    flex-direction: column;
    min-height: 100vh;
  }
  .el-header {
    padding: 0 6px;
    min-height: 48px;
    font-size: 16px;
  }
  .el-main {
    padding: 2px;
  }
}
</style> 